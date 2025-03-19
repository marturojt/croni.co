from sqlalchemy import Column, DateTime, Integer, String, Text, Index
from sqlalchemy.ext.declarative import declarative_base
import bcrypt
import datetime

Base = declarative_base()

class Users(Base):
    __tablename__ = 'tb_users'

    idUser = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    email = Column(String(length=255))
    username = Column(String(length=255))
    password = Column(Text)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_url = Column(String(255), unique=True, index=True)
    long_url = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_used = Column(DateTime, default=datetime.datetime.utcnow) # Add the last_used column

    Index('short_url_index', short_url)
