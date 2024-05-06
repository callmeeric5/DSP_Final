import datetime
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Logger(Base):
    __tablename__ = "Validation_Table"

    id = Column(Integer, primary_key=True)
    RunID = Column(String)
    meta = Column(String)
    errors = Column(String)
    created_at = Column(
        DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
