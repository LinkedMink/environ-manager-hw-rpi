from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, BigInteger, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from data.data_repository import DataRepository

class LogEntry(DataRepository.Base):
    """A database record representing data recorded by the hardware's sensors"""

    __tablename__ = 'LogEntries'

    id = Column('Id', BigInteger, primary_key=True)
    relative_humidity = Column('RelativeHumidity', Numeric(4, 1))
    temperature = Column('Temperature', Numeric(4, 1))
    recorded_on = Column('RecordedOn', DateTime)

    hardware_device_id = Column('HardwareDeviceId', BigInteger, ForeignKey('HardwareDevices.Id'))
    hardware_device = relationship("HardwareDevice", back_populates="log_entries")

    def __init__(self, hardware_device_id, relative_humidity, temperature):
        self.hardware_device_id = hardware_device_id
        self.relative_humidity = Decimal(str(round(relative_humidity, 1)))
        self.temperature = Decimal(str(round(temperature, 1)))
        self.recorded_on = datetime.now()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return ('LogEntry(id={0}, ' 
                'relative_humidity={1}, '
                'temperature={2}, '
                'recorded_on={3}, '
                'hardware_device_id={4})').format(
                    self.id, self.relative_humidity, self.temperature, self.recorded_on, self.hardware_device_id)
