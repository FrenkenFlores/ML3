"""
Database models for logs classification app using SQLAlchemy.
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Database configuration
import os
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')

# Create SQLAlchemy components
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rawdata = relationship('RawData', back_populates='user', cascade='all, delete-orphan')
    datasets = relationship('Dataset', back_populates='user', cascade='all, delete-orphan')

# RawData model
class RawData(Base):
    __tablename__ = 'rawdata'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    log_text = Column(Text, nullable=False)
    source = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('User', back_populates='rawdata')

# Labels model
class Label(Base):
    __tablename__ = 'labels'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    color = Column(String(7), default='#007bff')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Dataset model
class Dataset(Base):
    __tablename__ = 'dataset'
    
    id = Column(Integer, primary_key=True, index=True)
    rawdata_id = Column(Integer, ForeignKey('rawdata.id', ondelete='CASCADE'), nullable=False)
    label_id = Column(Integer, ForeignKey('labels.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (UniqueConstraint('rawdata_id', 'label_id', name='_rawdata_label_uc'),)
    
    rawdata = relationship('RawData')
    label = relationship('Label')
    user = relationship('User')