import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO it probably makes sense to make a web service to abstract away storage details
# Keep direct DB access for simplicity, and so we don't need an app server to run
class DataRepository:
    """Contain saving entities to a database as a repository that supports
    CRUD operations. The DataRepository is generic and can accept any Entity
    object deriving from DataRepository.Base.
    """

    Base = declarative_base()
    logger = logging.getLogger('DataRepository')

    @classmethod
    def set_connection_string(cls, connection_string):
        cls.connection_string = connection_string
        cls.database_engine = create_engine(connection_string)
        cls.Session = sessionmaker(bind=cls.database_engine)

    @classmethod
    def create_schema(cls):
        cls.Base.metadata.create_all(cls.database_engine)

    def __init__(self):
        self.session = None
        self.are_transactions_atomic = True

    def __del__(self):
        self.close_session()

    def get_all(self, entityType):
        DataRepository.logger.debug('Getting All Entities: ')

        session = self.get_session()
        return session.query(entityType).all()

    def add(self, entities):
        DataRepository.logger.debug('Adding Entities: {0}'.format(entities))

        session = self.get_session()

        if type(entities) == list:
            session.add_all(entities)
        else:
            session.add(entities)

        if self.are_transactions_atomic:
            self.session.commit()
            self.close_session()

    def get_session(self):
        if self.session is None:
            self.session = DataRepository.Session()
            DataRepository.logger.info(
                'Started Database Session: {0}'.format(DataRepository.connection_string))
        
        return self.session

    def close_session(self):
        if self.session:
            self.session.close()
            self.session = None