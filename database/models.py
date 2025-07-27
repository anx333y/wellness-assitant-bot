from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    full_name = Column(String)
    username = Column(String)
    created_at = Column(DateTime)

class HealthData(Base):
    __tablename__ = 'health_data'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    gender = Column(String(1))
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    heart_rate = Column(Integer)
    blood_pressure_systolic = Column(Integer)
    blood_pressure_diastolic = Column(Integer)
    vital_capacity = Column(Integer)
    training_experience = Column(Integer)
    smoking = Column(Boolean)
    hardening = Column(Boolean)
    run_2km = Column(Float)
    recovery_heart_rate = Column(Float)
    strength_tests = Column(Integer)
    colds_frequency = Column(Integer)
    has_diseases = Column(Boolean)
    score = Column(Float)
    created_at = Column(DateTime)

class IMTData(Base):
    __tablename__ = 'imt_data'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    weight = Column(Integer)
    height = Column(Integer)
    imt = Column(Integer)
    created_at = Column(DateTime)