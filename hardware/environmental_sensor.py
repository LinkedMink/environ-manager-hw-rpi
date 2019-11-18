from decimal import Decimal
import logging
from time import sleep
from threading import Thread

from Adafruit_DHT import read_retry, DHT22                          #pylint: disable=import-error
from data.log_entry import LogEntry
from server.log_entry_request_handler import LogEntryRequestHandler
from shared.observable import Observable

class EnvironmentalSensor(Thread):
    """A seperate thread to read data from a temperature and humidity sensor
    on a regular interval
    """

    # Max on a DHT22 is 2 seconds, but give extra time to compensate for bad clock
    MAX_READ_INTERVAL = 2.5
    logger = logging.getLogger('EnvironmentalSensor')

    def __init__(self, sensor_pin, entry_queue):
        super(EnvironmentalSensor, self).__init__()
        self.sensor_pin = sensor_pin
        self.entry_queue = entry_queue
        self.latest_log_entry = Observable()
        self.is_running = False
        self.hardware_device_id = None

    def run(self):
        self.is_running = True
        while self.is_running:
            sleep(EnvironmentalSensor.MAX_READ_INTERVAL)

            relative_humidity, temperature = read_retry(DHT22, self.sensor_pin)

            if relative_humidity is not None or temperature is not None:
                entry = LogEntry(
                    self.hardware_device_id, 
                    relative_humidity, 
                    temperature)

                EnvironmentalSensor.logger.info(entry)
                self.latest_log_entry.set_value(entry)

                if self.entry_queue is not None:
                    EnvironmentalSensor.logger.debug('Enqueued Log Entry')
                    self.entry_queue.put(entry)
            else:
                EnvironmentalSensor.logger.warning('Failed to read from sensor')
                
    def stop(self):
        self.is_running = False
