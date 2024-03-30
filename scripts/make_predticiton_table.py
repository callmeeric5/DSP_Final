import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Prediction_Table(Base):
    __tablename__ = "Prediction_Table"
    id = Column(Integer, primary_key=True)
    occupation = Column(String)
    marital_status = Column(String)
    product_category_1 = Column(String)
    product_category_2 = Column(String)
    product_category_3 = Column(String)
    age = Column(String)
    gender = Column(String)
    city_category = Column(String)
    stay_in_current_city_years = Column(Integer)
    predicted_purchase = Column(Float)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
