import datetime
from sqlalchemy import Column, Integer, Text, DateTime, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Logger(Base):
    __tablename__ = "data_logger"

    id = Column(Integer, primary_key=True)
    files = Column(VARCHAR(500))
    logs = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
