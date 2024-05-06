from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
DB_HOST = "localhost"
DB_NAME = "blackfriday"
DB_USER = "ericwindsor"

DB_PORT = "5432"


def db_engine():
    try:
        engine = create_engine(f"postgresql://{DB_USER}:@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        print("Database connection established")
        return {"engine": engine, "session": session, "status": 200}
    except Exception as e:
        print(e.args)
        return {"status": 500}
