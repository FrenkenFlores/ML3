"""
Database models for logs classification app using SQLAlchemy.
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Database configuration
import os
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/logs_classification')

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
    
    # Relationships
    user = relationship('User', back_populates='rawdata')
    datasets = relationship('Dataset', back_populates='rawdata', cascade='all, delete-orphan')

# Label model
class Label(Base):
    __tablename__ = 'labels'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    color = Column(String(7), default='#007bff')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    datasets = relationship('Dataset', back_populates='label', cascade='all, delete-orphan')

# Dataset model
class Dataset(Base):
    __tablename__ = 'dataset'
    
    id = Column(Integer, primary_key=True, index=True)
    rawdata_id = Column(Integer, ForeignKey('rawdata.id', ondelete='CASCADE'), nullable=False)
    label_id = Column(Integer, ForeignKey('labels.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint to prevent duplicate rawdata-label pairs
    __table_args__ = (UniqueConstraint('rawdata_id', 'label_id', name='_rawdata_label_uc'),)
    
    # Relationships
    rawdata = relationship('RawData', back_populates='datasets')
    label = relationship('Label', back_populates='datasets')
    user = relationship('User', back_populates='datasets')

# Create all tables
Base.metadata.create_all(bind=engine)

# Helper functions

def create_user(db, username: str, email: str, password_hash: str):
    """Create a new user."""
    user = User(username=username, email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_label(db, name: str, description: str = None, color: str = '#007bff'):
    """Create a new label."""
    label = Label(name=name, description=description, color=color)
    db.add(label)
    db.commit()
    db.refresh(label)
    return label

def create_raw_data(db, user_id: int, log_text: str, source: str = None):
    """Create new raw data entry."""
    raw_data = RawData(user_id=user_id, log_text=log_text, source=source)
    db.add(raw_data)
    db.commit()
    db.refresh(raw_data)
    return raw_data

def create_dataset(db, rawdata_id: int, label_id: int, user_id: int):
    """Create a new dataset entry."""
    dataset = Dataset(rawdata_id=rawdata_id, label_id=label_id, user_id=user_id)
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset