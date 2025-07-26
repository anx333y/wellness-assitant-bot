from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from .models import Base, User, HealthData, IMTData
from typing import Optional
from datetime import datetime

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

async def save_user(tg_id: int, full_name: str, username: str):
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
    db = SessionLocal()
    try:
        health_data = HealthData(
            user_id=user_id,
            gender=data.get("gender"),
            age=data.get("age"),
            heart_rate=data.get("heart_rate"),
            blood_pressure=data.get("blood_pressure"),
            weight=data.get("weight"),
            height=data.get("height"),
            score=data.get("score"),
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.add(health_data)
        db.commit()
    finally:
        db.close()

async def get_last_health_data(user_id: int) -> Optional[HealthData]:
    """Получить последнюю оценку здоровья пользователя"""
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
    """Получить последнюю оценку здоровья пользователя"""
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