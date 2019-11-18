#!/usr/bin/python3
# Create the database tables used by this project

from config import config
from data.data_repository import DataRepository
from data.log_entry import LogEntry
from data.hardware_device import HardwareDevice

def seed():
    repository = DataRepository()

    this_device = HardwareDevice(
        host=config["HttpHost"], 
        device_type=HardwareDevice.DeviceType.RASPBERRY_PI)
    repository.add(this_device)

    repository.close_session()

def main():
    DataRepository.set_connection_string(config["ConnectionString"])
    DataRepository.create_schema()
    seed()

if __name__ == "__main__":
    main()
