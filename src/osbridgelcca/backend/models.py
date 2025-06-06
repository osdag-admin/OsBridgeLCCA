from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, UTC

Base = declarative_base()

class MaterialRate(Base):
    """Regional schedule of rates for materials"""
    __tablename__ = 'material_rates'
    
    id = Column(Integer, primary_key=True)
    material_name = Column(String(100), nullable=False)
    region = Column(String(50), nullable=False)
    unit = Column(String(20), nullable=False)
    rate = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    last_updated = Column(DateTime, default=lambda: datetime.now(UTC))

class ScrapValue(Base):
    """Scrap values and recyclability percentages"""
    __tablename__ = 'scrap_values'
    
    id = Column(Integer, primary_key=True)
    material_name = Column(String(100), nullable=False)
    scrap_value = Column(Float, nullable=False)
    recyclability_percentage = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    last_updated = Column(DateTime, default=lambda: datetime.now(UTC))

class EnvironmentalImpact(Base):
    """Environmental impact data from EPDs"""
    __tablename__ = 'environmental_impacts'
    
    id = Column(Integer, primary_key=True)
    material_name = Column(String(100), nullable=False)
    epd_id = Column(String(50), nullable=False)
    global_warming_potential = Column(Float, nullable=False)  # kg CO2 eq
    water_consumption = Column(Float)  # m³
    energy_consumption = Column(Float)  # MJ
    waste_generation = Column(Float)  # kg
    last_updated = Column(DateTime, default=lambda: datetime.now(UTC))

class SocialCostOfCarbon(Base):
    """Country-specific social cost of carbon"""
    __tablename__ = 'social_cost_of_carbon'
    
    id = Column(Integer, primary_key=True)
    country = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    cost_per_ton = Column(Float, nullable=False)  # USD per ton CO2
    currency = Column(String, nullable=False)
    last_updated = Column(DateTime, default=lambda: datetime.now(UTC))

class TransportEmissionFactor(Base):
    """Road transport carbon emission factors"""
    __tablename__ = 'transport_emission_factors'
    
    id = Column(Integer, primary_key=True)
    vehicle_type = Column(String(50), nullable=False)
    emission_factor = Column(Float, nullable=False)  # kg CO2 per km
    load_factor = Column(Float)  # Average load factor
    last_updated = Column(DateTime, default=lambda: datetime.now(UTC))

class VehicleOperationCost(Base):
    """Vehicle operation costs"""
    __tablename__ = 'vehicle_operation_costs'
    
    id = Column(Integer, primary_key=True)
    vehicle_type = Column(String(50), nullable=False)
    fuel_cost_per_km = Column(Float, nullable=False)
    maintenance_cost_per_km = Column(Float, nullable=False)
    insurance_cost_per_year = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    last_updated = Column(DateTime, default=lambda: datetime.now(UTC))

class UserAnalysis(Base):
    """User analyses storage"""
    __tablename__ = 'user_analyses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    analysis_name = Column(String(100), nullable=False)
    analysis_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

def init_db(db_url):
    """Initialize the database"""
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine 