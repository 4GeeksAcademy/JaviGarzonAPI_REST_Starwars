
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

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

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username, 
            "full_name": self.full_name,    
            "email": self.email,
            "created": self.created,       
        }
    def serialize_favorite(self):
        return{
            "id": self.id,
            "username": self.username, 
            "email": self.email,
            "favorites": [favorite.serialize() for favorite in self.favorites]
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    films = Column(String(1000), nullable=False)
    affiliations = Column(String(100), nullable=False)
    species= Column(String(50), nullable=False)
    places = Column(String(1000), nullable=False)
    location = Column(String(80), nullable=False)
    climate = Column(String(100), nullable=False)
    terrain = Column(String(100), nullable=False)
    system = Column(String(100), nullable=False)
    vehicles = Column(String(100), nullable=False)
    weapons = Column(String(100), nullable=False)
    tool = Column(String(100), nullable=False)
    droids = Column(String(100), nullable=False)
    surface_water = Column(String(10), nullable=False)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    favorites = relationship('Favorite', backref='planet', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name, 
            "description": self.description,
            "films": self.films,       
            "affiliations": self.affiliations,
            "species": self.species, 
            "places": self.places,
            "location": self.location,    
            "climate": self.climate,
            "terrain": self.terrain, 
            "system": self.system,
            "vehicles": self.vehicles,  
            "weapons": self.weapons,
            "tool": self.tool,    
            "droids": self.droids,
            "surface_water": self.surface_water, 
            "created": self.created,
            "edited": self.edited,        
        }


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
    affiliations = Column(String(100), nullable=False)
    planetlocation = Column(String(80), nullable=False)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    favorites = relationship('Favorite', backref='vehicle', lazy=True)


    def serialize(self):
        return {
            "id": self.id,
           "name": self.name, 
            "model": self.model,
            "vehicle_class": self.vehicle_class, 
            "length": self.length,
            "cost_in_credits": self.cost_in_credits,    
            "drivers": self.drivers,
            "history": self.history, 
            "films": self.films,       
            "affiliations": self.affiliations,
            "planetlocation": self.planetlocation,
            "created": self.created,
            "edited": self.edited,                
        }

class People(db.Model):
    __tablename__ = 'people'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    height= Column(String(50), nullable=False)
    species= Column(String(50), nullable=False)
    history = Column(String(1000), nullable=False)
    films = Column(String(1000), nullable=False)
    affiliations = Column(String(100), nullable=False)
    planetlocation = Column(String(80), nullable=False)
    url = Column(String(100), nullable=False)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    favorites = relationship('Favorite', backref='people', lazy=True)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name, 
            "gender": self.gender,
            "height": self.height, 
            "species": self.species,
            "history": self.history, 
            "films": self.films,       
            "affiliations": self.affiliations,
            "planetlocation": self.planetlocation,
            "url": self.url,
            "created": self.created,
            "edited": self.edited,           
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    people_id = Column(Integer, ForeignKey('people.id'), nullable=True)
    vehicle_id = Column(Integer, ForeignKey('vehicle.id'), nullable=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), nullable=True)


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id, 
            "people_id": self.people_id,
            "vehicle_id": self.vehicle_id,
            "planet_id": self.planet_id,               
        }
