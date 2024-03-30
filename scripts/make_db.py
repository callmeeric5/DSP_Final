from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from scripts.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, DB_PORT


def db_engine():
    try:
        engine = create_engine(
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        Session = sessionmaker(bind=engine)
        session = Session()
        return {"session": session, "status": 200}
    except Exception as e:
        print(e.args)
        return {"status": 500}
