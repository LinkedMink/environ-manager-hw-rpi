#!/usr/bin/python3
# This will start a process that will run forever or until we receive a stop signal
# It's probably best to wrap this as a systemd process

import logging
from queue import Queue
import RPi.GPIO as GPIO                 #pylint: disable=import-error
from socketserver import TCPServer
import signal
import sys

from config import config
from data.batch_entity_persister import BatchEntityPersister
from data.data_repository import DataRepository
from data.hardware_device import HardwareDevice
from hardware.environmental_sensor import EnvironmentalSensor
from server.log_entry_request_handler import LogEntryRequestHandler
from server.service_status import ServiceStatus
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

def configure_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(config['PinWarningLed'], GPIO.OUT)

def set_warning_led_from_status(service_status):
    if service_status.should_show_warning_led():
        GPIO.output(config['PinWarningLed'], GPIO.HIGH)
    else:
        GPIO.output(config['PinWarningLed'], GPIO.LOW)

def main():
    log_entry_queue = None
    log_entry_persister = None
    environment_sensor = None
    httpd = None
    service_status = ServiceStatus(config['SensorWarningLimit']) 

    def cleanup_on_exit():
        nonlocal environment_sensor
        nonlocal log_entry_persister

        logging.info('Starting to cleanup')

        environment_sensor.stop()
        environment_sensor.join()

        if log_entry_persister:
            log_entry_persister.stop()
            log_entry_persister.join()
            log_entry_persister.dequeue_all()
            log_entry_persister.flush()

    # It's probably not recommended to do too much logging on SD cards
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    #logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logging.info('Starting Main: {0}'.format(config))

    # register the signals to be caught
    signal.signal(signal.SIGTERM, cleanup_on_exit)

    configure_gpio()
    
    if config["ConnectionString"]:
        DataRepository.set_connection_string(config["ConnectionString"])
        repository = DataRepository()

        log_entry_queue = Queue()

        log_entry_persister = BatchEntityPersister(repository, log_entry_queue, 'LogEntry') 
        log_entry_persister.start()

        service_status.is_database_connected = True

        logging.info('Started: Database persistence thread')
    else:
        logging.warning('No valid database configuration detected. Skip DB logging')

    environment_sensor = EnvironmentalSensor(config["PinHumidityTemperatureSensor"], log_entry_queue)
    environment_sensor.latest_log_entry.subscribe(service_status.update_from_log_entry)
    
    if repository is not None:
        try:
            device_type = HardwareDevice.DeviceType.RASPBERRY_PI.value
            matching_device = repository.get_session().query(HardwareDevice).filter(
                and_(HardwareDevice.device_type == device_type, 
                     HardwareDevice.host == config['HttpHost'])).one()

            environment_sensor.hardware_device_id = matching_device.id
        except (NoResultFound, MultipleResultsFound) as e:
            logging.critical(e)
            logging.error('Run Create Schema or correct HttpHost')
            sys.exit()

    environment_sensor.start()

    logging.info('Started: Environmental sensor thread')
    
    service_status.subscribe(LogEntryRequestHandler.update_service_status)
    service_status.subscribe(set_warning_led_from_status)
    httpd = TCPServer(("", config["HttpPort"]), LogEntryRequestHandler)
    
    logging.info('Starting: Main HTTP Server - Ctrl-C to Stop')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        cleanup_on_exit()

    logging.info('Stopped: Main Thread')

if __name__ == "__main__":
    main()