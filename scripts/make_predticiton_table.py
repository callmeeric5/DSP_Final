import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Prediction_Table(Base):
    __tablename__ = "Prediction_Table"
    id = Column(Integer, primary_key=True)
    occupation = Column(Float)
    marital_status = Column(Float)
    product_category_1 = Column(Float)
    product_category_2 = Column(Float)
    product_category_3 = Column(Float)
    age = Column(Float)
    gender = Column(Float)
    city_category = Column(Float)
    stay_in_current_city_years = Column(Float)
    purchase = Column(Float)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
