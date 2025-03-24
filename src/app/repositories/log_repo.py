from sqlalchemy.orm import Session
from src.app.entities.log import Log
from src.app.repositories.base_repository import BaseRepository


class LogRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_one(self, item_id: int) -> Log:
        """
        Retrieve a single log by its ID
        """
        return self.session.query(Log).filter_by(id=item_id).first()

    def get_all(self) -> list[Log]:
        """
        Retrieve all logs
        """
        return self.session.query(Log).all()

    def add(self, log: Log) -> Log:
        """
        Add a new log entry
        """
        self.session.add(log)
        self.session.commit()
        return log

    def update(self, log: Log) -> Log:
        """
        Update an existing log entry
        """
        existing_log = self.session.query(Log).filter_by(id=log.id).first()
        if existing_log:
            existing_log.message = log.message
            existing_log.timestamp = log.timestamp
            self.session.commit()
        return existing_log

    def delete(self, log_id: int) -> bool:
        """
        Delete a log entry
        """
        log = self.session.query(Log).filter_by(id=log_id).first()
        if log:
            self.session.delete(log)
            self.session.commit()
            return True
        return False
