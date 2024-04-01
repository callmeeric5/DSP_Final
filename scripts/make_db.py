from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from scripts.__init__ import DB_HOST, DB_NAME, DB_USER, DB_PORT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def db_engine():
    try:
        engine = create_engine(f"postgresql://{DB_USER}:@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        print("Database connection established")

        return {"engine": engine, "Session": session, "status": 200}
    except Exception as e:
        print(e.args)
        return {"status": 500}
