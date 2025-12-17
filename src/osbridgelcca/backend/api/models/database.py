# src/osbridgelcca/backend/api/models/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from datetime import datetime
import os

Base = declarative_base()

class Project(Base):
    """Main project table"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

class FormData(Base):
    """Store form data for different construction components"""
    __tablename__ = "form_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=True)  # Can be null for default project
    form_name = Column(String(100), nullable=False)  # foundation, sub-structure, etc.
    materials = Column(JSON, nullable=False)  # Store materials as JSON
    timestamp = Column(DateTime, default=func.now())
    saved_at = Column(DateTime, default=func.now())

class FinancialData(Base):
    """Store financial parameters"""
    __tablename__ = "financial_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=True)
    real_discount_rate = Column(Float, default=4.25)
    interest_rate = Column(Float, default=10.0)
    investment_ratio = Column(Float, default=0.5)
    duration_of_study = Column(String(50), default="50 & 100")
    construction_time = Column(Float, default=1.0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class TrafficData(Base):
    """Store traffic analysis data"""
    __tablename__ = "traffic_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=True)
    lane_type = Column(String(100), default="Single Lane Roads")
    roughness = Column(Integer, default=2000)
    rf = Column(Integer, default=5)
    reroute_distance = Column(Float, default=1.0)
    vehicles = Column(JSON, nullable=False)  # Store vehicle data as JSON
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class MaintenanceData(Base):
    """Store maintenance parameters"""
    __tablename__ = "maintenance_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=True)
    periodic_maintenance_cost = Column(Float, default=0.55)
    annual_routine_inspection_cost = Column(Float, default=1.0)
    repair_rehabilitation_cost = Column(Float, default=10.0)
    frequency_of_periodic_maintenance = Column(Integer, default=5)
    frequency_of_routine_inspection = Column(Integer, default=1)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class DemolitionRecyclingData(Base):
    """Store demolition and recycling parameters"""
    __tablename__ = "demolition_recycling_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=True)
    demolition_cost_rate = Column(Float, default=10.0)
    scrap_value_of_structural_steel = Column(Float, default=50000.0)
    structural_steel_scrap = Column(Float, default=98.0)
    user_input_steel_quantity = Column(Float, default=0.0)
    user_input_steel_unit = Column(String(10), default="MT")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class CarbonEmissionData(Base):
    """Store carbon emission data and calculations"""
    __tablename__ = "carbon_emission_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=True)
    materials = Column(JSON, nullable=False)  # Store materials with carbon factors
    calculations = Column(JSON, nullable=True)  # Store calculation results
    total_carbon_emission = Column(Float, default=0.0)
    total_materials = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class CalculationResults(Base):
    """Store all LCC calculation results"""
    __tablename__ = "calculation_results"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=True)
    calculation_type = Column(String(100), nullable=False)  # initial_construction, time_cost, etc.
    result_data = Column(JSON, nullable=False)  # Store complete calculation results
    created_at = Column(DateTime, default=func.now())

# Database configuration
def get_database_url():
    """Get database URL from environment or use default SQLite"""
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        return db_url
    
    # Default to SQLite in data/databases directory
    db_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'databases')
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, 'lcca_project.db')
    return f"sqlite:///{db_path}"

# Create database engine and session
DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL, echo=False)

# Create all tables
Base.metadata.create_all(engine)

# Session factory
SessionLocal = sessionmaker(bind=engine)

def get_db_session():
    """Get database session"""
    session = SessionLocal()
    try:
        return session
    except Exception:
        session.close()
        raise

def get_or_create_project(session, project_name="default"):
    """Get existing project or create new one"""
    project = session.query(Project).filter_by(name=project_name).first()
    if not project:
        project = Project(name=project_name, description="Default LCCA Project")
        session.add(project)
        session.commit()
    return project