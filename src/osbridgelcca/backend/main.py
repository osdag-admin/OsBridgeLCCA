import sqlite3
from flask import Flask
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import existing blueprints
from api.routes.materials_dropdown import materials_dropdown_bp
from api.routes.structure_works import structure_works_bp
from api.routes.financial_data import financial_bp
from api.routes.traffic_analysis import traffic_analysis_bp

from api.routes.demolition_recycling import demolition_recycling_calculations_bp
from api.routes.cost_calculations import cost_calculations_bp
# Add this import at the top
from api.routes.carbon_emission import carbon_emission_bp
# Add this import with your other imports
from api.routes.maintenance_data import maintenance_calculations_bp

# Register it with other blueprints


# Add this registration with other blueprints

# Import database models and functions
from api.models.database import get_db_session, get_or_create_project, CalculationResults, FormData
def clear_database_on_startup():
    """Clear database calculations AND form data on server startup"""
    try:
        from api.models.database import get_db_session, get_or_create_project, CalculationResults, FormData
        
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            # Clear calculation results
            calc_deleted = session.query(CalculationResults).filter_by(project_id=project.id).count()
            session.query(CalculationResults).filter_by(project_id=project.id).delete()
            
            # Clear form data
            form_deleted = session.query(FormData).filter_by(project_id=project.id).count()
            session.query(FormData).filter_by(project_id=project.id).delete()
            
            # Clear specific calculation types from SQLite database
            db_path = os.path.join(os.path.dirname(__file__), 'data', 'databases', 'project_data.db')
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM calculation_results WHERE calculation_type IN (
                        'carbon_emission_data', 'traffic_data', 'road_user_cost', 
                        'time_cost', 'initial_construction_cost_auto',
                        'initial_carbon_emission_cost', 'additional_carbon_emission_cost',
                        'road_user_cost_calculated', 'carbon_emission_materials',
                        'carbon_cost_parameters'
                    )
                ''')
                conn.commit()

            session.commit()
            print(f"=== SERVER STARTUP: CLEARED {calc_deleted} CALCULATIONS & {form_deleted} FORM DATA ===")
        finally:
            session.close()
    except Exception as e:
        print(f"Error clearing database on startup: {e}")
def ensure_database_tables():
    """Ensure all required database tables exist"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'data', 'databases', 'project_data.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Create calculation_results table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS calculation_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    calculation_type TEXT NOT NULL,
                    result_data TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            
    except Exception as e:
        print(f"Error ensuring database tables: {e}")

app = Flask(__name__)

# Fix CORS configuration
# Replace the existing CORS configuration with this:
CORS(app, 
     origins=["http://localhost:5173", "http://127.0.0.1:5173"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)
# Initialize database on server start (call after app creation)
clear_database_on_startup()

ensure_database_tables()
# Register blueprints...
app.register_blueprint(materials_dropdown_bp, url_prefix='/api')
app.register_blueprint(structure_works_bp)
app.register_blueprint(financial_bp)
app.register_blueprint(traffic_analysis_bp)
app.register_blueprint(maintenance_calculations_bp)
app.register_blueprint(demolition_recycling_calculations_bp)
app.register_blueprint(carbon_emission_bp, url_prefix='/api')

# Register new cost calculations blueprint
app.register_blueprint(cost_calculations_bp)

# Health check endpoint
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'LCC Analysis API is running'}



# Update your main.py endpoints section to include the new validation endpoints:

@app.route('/')
def root():
    return {
        'message': 'Life Cycle Cost Analysis API',
        'version': '2.0',
        'endpoints': {
            # Form endpoints
            'forms': '/api/forms',
            'components': '/api/components/<form_name>',
            'form_data': '/api/form-data/<form_name>',
            
            # Material endpoints (independent)
            'all_materials': '/api/materials',
            'material_data': '/api/material-data/<material_name>',
            'sub_materials': '/api/sub-materials/<material_name>',
            'units': '/api/units/<material_name>',
            
            # Backward compatibility endpoints
            'materials_for_component': '/api/materials/<form_name>/<component_name>',
            'sub_materials_legacy': '/api/sub-materials/<form_name>/<component_name>/<material_name>',
            'units_legacy': '/api/units/<form_name>/<component_name>/<material_name>',
            
            # Data management endpoints
            'save_form': '/api/save-form-data/<form_name>',
            'get_form_data': '/api/get-form-data/<form_name>',  # NEW
            'get_carbon_materials': '/api/get-carbon-materials',
            'calculate_cost': '/api/calculate-initial-cost',
            'save_financial': '/api/save-financial-data',
            'calculate_time_cost': '/api/calculate-time-cost',
            'save_traffic': '/api/save-traffic-data',
            'calculate_road_user_cost': '/api/calculate-road-user-cost',
            'save_maintenance': '/api/save-maintenance-data',
            'calculate_maintenance_costs': '/api/calculate-maintenance-costs',
            'get_maintenance_data': '/api/get-maintenance-data',
            'save_demolition_recycling': '/api/save-demolition-recycling-data',
            'calculate_demolition_recycling_costs': '/api/calculate-demolition-recycling-costs',
            'get_demolition_recycling_data': '/api/get-demolition-recycling-data',
            
            # Form validation endpoints - NEW
            'check_form_completion': '/api/check-form-completion',
            'validate_form_sequence': '/api/validate-form-sequence',
            
            # LCC Cost Calculation endpoints
            'calculate_all_costs': '/api/calculate-all-costs',
            'calculate_initial_construction_cost': '/api/calculate-initial-construction-cost',
            'calculate_carbon_emission_cost': '/api/calculate-carbon-emission-cost',
            'calculate_time_cost_new': '/api/calculate-time-cost',
            'calculate_road_user_cost_new': '/api/calculate-road-user-cost',
            'calculate_maintenance_costs_new': '/api/calculate-maintenance-costs',
            'calculate_demolition_recycling_costs_new': '/api/calculate-demolition-recycling-costs',
            'get_calculation_results': '/api/get-calculation-results/<project_id>',
            'get_all_stored_results': '/api/get-all-stored-results',
            'clear_calculation_storage': '/api/clear-calculation-storage',
            
            # Debug endpoints
            'debug_form': '/api/debug/<form_name>',
            'debug_material': '/api/debug/material/<material_name>',
            'debug_form_storage': '/api/debug-form-storage',  # NEW
            # Add these lines in the endpoints dictionary
            'calculate_and_save_initial_cost' : '/api/calculate-and-save-initial-cost',
            'get_initial_construction_cost': '/api/get-initial-construction-cost',
            # In the endpoints dictionary inside root() function, add:
            'calculate_and_store_maintenance_costs': '/api/calculate-and-store-maintenance-costs',
            'get_stored_maintenance_costs': '/api/get-stored-maintenance-costs',
            'debug_maintenance_dependencies': '/api/debug/maintenance-dependencies',
            'calculate_and_store_demolition_costs': '/api/calculate-and-store-demolition-costs',
            'get_stored_demolition_costs': '/api/get-stored-demolition-costs',
            'debug_demolition_dependencies': '/api/debug/demolition-dependencies',
        }
    }

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)