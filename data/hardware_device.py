from datetime import datetime
import enum
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from data.data_repository import DataRepository

class HardwareDevice(DataRepository.Base):
    """A database record representing a device that reports data"""

    class DeviceType(enum.IntEnum):
        UNDEFINED = 0
        RASPBERRY_PI = 1

    __tablename__ = 'HardwareDevices'

    id = Column('Id', BigInteger, primary_key=True)
    name = Column('Name', String)
    description = Column('Description', String)
    host = Column('Host', String)
    device_type = Column('DeviceType', Integer)
    last_update_received = Column('LastUpdateReceived', DateTime)
    # Tracked Entity Columns
    modified_by = Column('ModifiedBy', String)
    modified_datetime = Column('ModifiedDateTime', DateTime)
    created_by = Column('CreatedBy', String)
    created_datetime = Column('CreatedDateTime', DateTime)

    log_entries = relationship('LogEntry', back_populates='hardware_device')

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return ('HardwareDevice(id={0}, ' 
                'host={1}, '
                'device_type={2}, '
                'last_update_received={3})').format(
                    self.id, self.host, self.device_type, self.last_update_received)
