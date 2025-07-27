from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from config import DATABASE_URL, POSTGRES_URL, DATABASE_NAME
from .models import Base, User, HealthData, IMTData
from typing import Optional
from datetime import datetime

def init_db():
    global engine, SessionLocal
    admin_engine = create_engine(POSTGRES_URL) 

    try:
      with admin_engine.connect() as conn:
        conn.execute(text("COMMIT"))

        result = conn.execute(
          text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
          {"dbname": DATABASE_NAME}
        ).scalar()
        
        if not result:
          conn.execute(text(f"CREATE DATABASE {DATABASE_NAME}"))
    except OperationalError as e:
      print(f"Ошибка создания базы данных: {e}")
      raise
    finally:
      admin_engine.dispose()

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)


async def save_user(tg_id: int, full_name: str, username: str):
    if not SessionLocal:
      return print(f"Ошибка при создании базы данных, нет сессии")

    db = SessionLocal()
    try:
        existing_user = db.execute(
            select(User).where(User.tg_id == tg_id)
        ).scalars().first()
        
        if existing_user:
            existing_user.full_name = full_name
            existing_user.username = username
        else:
            user = User(tg_id=tg_id, full_name=full_name, username=username)
            db.add(user)
        
        db.commit()
    finally:
        db.close()

async def save_health_data(user_id: int, data: dict):
    if not SessionLocal:
      return print(f"Ошибка при создании базы данных, нет сессии")

    db = SessionLocal()
    try:
        health_data = HealthData(
            user_id=user_id,
            gender=data.get("gender"),
            age=data.get("age"),
            weight=data.get("weight"),
            height=data.get("height"),
            heart_rate=data.get("heart_rate"),
            blood_pressure_systolic=data.get("blood_pressure_systolic"),
            blood_pressure_diastolic=data.get("blood_pressure_diastolic"),
            vital_capacity=data.get("vital_capacity") ,
            training_experience=data.get("training_experience"),
            smoking=data.get("smoking"),
            hardening=data.get("hardening"),
            run_2km=data.get("run_2km"),
            recovery_heart_rate=data.get("recovery_heart_rate"),
            strength_tests=data.get("strength_tests"),
            colds_frequency=data.get("colds_frequency"),
            has_diseases=data.get("has_diseases"),
            score=data.get("score"),
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.add(health_data)
        db.commit()
    finally:
        db.close()

async def get_last_health_data(user_id: int) -> Optional[HealthData]:
    if not SessionLocal:
      return print(f"Ошибка при создании базы данных, нет сессии")

    db = SessionLocal()
    try:
        result = db.execute(
            select(HealthData)
            .where(HealthData.user_id == user_id)
            .order_by(HealthData.created_at.desc())
            .limit(1)
        )
        return result.scalars().first()
    finally:
        db.close()

async def save_imt_data(user_id: int, data: dict):
    if not SessionLocal:
      return print(f"Ошибка при создании базы данных, нет сессии")

    db = SessionLocal()
    try:
        imt_data = IMTData(
            user_id=user_id,
            weight=data.get("weight"),
            height=data.get("height"),
            imt=data.get("imt"),
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.add(imt_data)
        db.commit()
    finally:
        db.close()

async def get_last_imt_data(user_id: int) -> Optional[IMTData]:
    if not SessionLocal:
      return print(f"Ошибка при создании базы данных, нет сессии")

    db = SessionLocal()
    try:
        result = db.execute(
            select(IMTData)
            .where(IMTData.user_id == user_id)
            .order_by(IMTData.created_at.desc())
            .limit(1)
        )
        return result.scalars().first()
    finally:
        db.close()