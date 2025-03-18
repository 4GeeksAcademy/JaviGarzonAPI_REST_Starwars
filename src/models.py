
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine

from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(40), nullable=False, unique=True)
    password = Column(String(40), nullable=False)
    full_name = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    favorites = relationship('Favorite', backref='user', lazy=True)

class Planet(db.Model):
    __tablename__ = 'planet'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    films = Column(String(1000), nullable=False)
    Affiliations = Column(String(100), nullable=False)
    species= Column(String(50), nullable=False)
    places = Column(String(1000), nullable=False)
    films = Column(String(1000), nullable=False)
    Affiliations = Column(String(100), nullable=False)
    location = Column(String(80), nullable=False)
    climate = Column(String(100), nullable=False)
    terrain = Column(String(100), nullable=False)
    system = Column(String(100), nullable=False)
    vehicles = Column(String(100), nullable=False)
    Weapons = Column(String(100), nullable=False)
    Tool = Column(String(100), nullable=False)
    droids = Column(String(100), nullable=False)
    surface_water = Column(String(10), nullable=False)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    favorites = relationship('Favorite', backref='planet', lazy=True)

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    vehicle_class = Column(String(100), nullable=False)
    length = Column(String(100), nullable=False)
    cost_in_credits = Column(String(100), nullable=False)
    drivers= Column(String(500), nullable=False)
    history = Column(String(1000), nullable=False)
    films = Column(String(1000), nullable=False)
    Affiliations = Column(String(100), nullable=False)
    planetlocation = Column(String(80), nullable=False)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    favorites = relationship('Favorite', backref='vehicle', lazy=True)

class People(db.Model):
    __tablename__ = 'people'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    height= Column(String(50), nullable=False)
    species= Column(String(50), nullable=False)
    history = Column(String(1000), nullable=False)
    films = Column(String(1000), nullable=False)
    Affiliations = Column(String(100), nullable=False)
    planetlocation = Column(String(80), nullable=False)
    url = Column(String(100), nullable=False)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    favorites = relationship('Favorite', backref='people', lazy=True)

class Favorite(db.Model):
    __tablename__ = 'favorite'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    people_id = Column(Integer, ForeignKey('people.id'), nullable=True)
    vehicle_id = Column(Integer, ForeignKey('vehicle.id'), nullable=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), nullable=True)

