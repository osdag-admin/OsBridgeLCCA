from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime
import sqlite3

carbon_emission_bp = Blueprint('carbon_emission', __name__)

# In-memory storage for carbon emission data
carbon_emission_storage = {}

# Carbon emission factors database (expandable)
CARBON_EMISSION_FACTORS = {
    "Concrete": {
        "M10": {"embedded_carbon_energy": 1.2, "carbon_emission_factor": 0.45},
        "M15": {"embedded_carbon_energy": 1.4, "carbon_emission_factor": 0.48},
        "M20": {"embedded_carbon_energy": 1.6, "carbon_emission_factor": 0.52},
        "M25": {"embedded_carbon_energy": 1.8, "carbon_emission_factor": 0.55},
        "M30": {"embedded_carbon_energy": 2.0, "carbon_emission_factor": 0.58},
        "M35": {"embedded_carbon_energy": 2.2, "carbon_emission_factor": 0.62},
        "M40": {"embedded_carbon_energy": 2.4, "carbon_emission_factor": 0.65},
        "default": {"embedded_carbon_energy": 1.5, "carbon_emission_factor": 0.50}
    },
    "Steel": {
        "TMT Fe 415": {"embedded_carbon_energy": 20.1, "carbon_emission_factor": 1.85},
        "TMT Fe 500": {"embedded_carbon_energy": 21.5, "carbon_emission_factor": 1.92},
        "TMT Fe 550": {"embedded_carbon_energy": 22.8, "carbon_emission_factor": 1.98},
        "Mild Steel": {"embedded_carbon_energy": 19.2, "carbon_emission_factor": 1.77},
        "High Tensile Steel": {"embedded_carbon_energy": 23.5, "carbon_emission_factor": 2.05},
        "default": {"embedded_carbon_energy": 20.0, "carbon_emission_factor": 1.85}
    },
    "Aluminum": {
        "6061-T6": {"embedded_carbon_energy": 155.0, "carbon_emission_factor": 8.24},
        "1100-H14": {"embedded_carbon_energy": 145.0, "carbon_emission_factor": 7.95},
        "5052-H32": {"embedded_carbon_energy": 160.0, "carbon_emission_factor": 8.42},
        "default": {"embedded_carbon_energy": 150.0, "carbon_emission_factor": 8.00}
    },
    "Wood": {
        "Hardwood": {"embedded_carbon_energy": 0.1, "carbon_emission_factor": -0.9},
        "Softwood": {"embedded_carbon_energy": 0.08, "carbon_emission_factor": -0.7},
        "Engineered Wood": {"embedded_carbon_energy": 0.15, "carbon_emission_factor": -0.5},
        "default": {"embedded_carbon_energy": 0.1, "carbon_emission_factor": -0.8}
    },
    "Cement": {
        "OPC 43": {"embedded_carbon_energy": 4.6, "carbon_emission_factor": 0.87},
        "OPC 53": {"embedded_carbon_energy": 5.1, "carbon_emission_factor": 0.92},
        "PPC": {"embedded_carbon_energy": 3.8, "carbon_emission_factor": 0.72},
        "default": {"embedded_carbon_energy": 4.5, "carbon_emission_factor": 0.85}
    },
    "Brick": {
        "Clay Brick": {"embedded_carbon_energy": 2.5, "carbon_emission_factor": 0.22},
        "Fly Ash Brick": {"embedded_carbon_energy": 1.8, "carbon_emission_factor": 0.15},
        "AAC Block": {"embedded_carbon_energy": 1.2, "carbon_emission_factor": 0.12},
        "default": {"embedded_carbon_energy": 2.0, "carbon_emission_factor": 0.18}
    },
    "Aggregate": {
        "Coarse Aggregate": {"embedded_carbon_energy": 0.1, "carbon_emission_factor": 0.005},
        "Fine Aggregate": {"embedded_carbon_energy": 0.08, "carbon_emission_factor": 0.004},
        "default": {"embedded_carbon_energy": 0.09, "carbon_emission_factor": 0.005}
    }
}

# File paths for saving data
CARBON_EMISSION_DATA_FILE = "carbon_emission_data.json"
SAVED_FORMS_DATA_FILE = "saved_forms_data.json"

def load_saved_forms_data():
    """Load saved forms data from file"""
    try:
        if os.path.exists(SAVED_FORMS_DATA_FILE):
            with open(SAVED_FORMS_DATA_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading saved forms data: {e}")
    return {}

def save_carbon_emission_data_to_file(data):
    """Save carbon emission data to file"""
    try:
        with open(CARBON_EMISSION_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving carbon emission data: {e}")
        return False

def load_carbon_emission_data_from_file():
    """Load carbon emission data from file"""
    try:
        if os.path.exists(CARBON_EMISSION_DATA_FILE):
            with open(CARBON_EMISSION_DATA_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading carbon emission data: {e}")
    return {}



@carbon_emission_bp.route('/get-carbon-emission-factors/<material_name>', methods=['GET'])
def get_carbon_emission_factors(material_name):
    """Get carbon emission factors for a specific material"""
    try:
        material_factors = CARBON_EMISSION_FACTORS.get(material_name, {})
        if not material_factors:
            # If material not found, return default values
            return jsonify({
                'success': True,
                'factors': {
                    'default': {
                        'embedded_carbon_energy': 0.0,
                        'carbon_emission_factor': 0.0
                    }
                }
            })
        
        return jsonify({
            'success': True,
            'factors': material_factors
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# In emissions.py, modify save_carbon_emission_data function:
@carbon_emission_bp.route('/save-carbon-emission-data', methods=['POST'])
def save_carbon_emission_data():
    """Save carbon emission data to database"""
    try:
        data = request.get_json()
        
        if not data or 'materials' not in data:
            return jsonify({
                'success': False,
                'error': 'Invalid data format'
            }), 400
        
        # Add timestamp
        data['timestamp'] = datetime.now().isoformat()
        
        # Save to database instead of file
        db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
        db_path = os.path.abspath(db_path)
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO calculation_results (calculation_type, result_data, created_at)
                VALUES (?, ?, ?)
            ''', ('carbon_emission_data', json.dumps(data), datetime.now().isoformat()))
            conn.commit()
        
        print("Carbon emission data saved to database:", data)
        
        return jsonify({
            'success': True,
            'message': 'Carbon emission data saved to database successfully',
            'data': data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@carbon_emission_bp.route('/calculate-carbon-emissions', methods=['POST'])
def calculate_carbon_emissions():
    """Calculate carbon emissions for materials"""
    try:
        data = request.get_json()
        
        if not data or 'materials' not in data:
            return jsonify({
                'success': False,
                'error': 'Invalid data format'
            }), 400
        
        materials = data['materials']
        calculations = []
        total_carbon_emission = 0
        
        for material in materials:
            try:
                quantity = float(material.get('quantity', 0))
                embedded_carbon_energy = float(material.get('embedded_carbon_energy', 0))
                carbon_emission_factor = float(material.get('carbon_emission_factor', 0))
                
                # Calculate carbon emission (quantity × carbon_emission_factor)
                carbon_emission = quantity * carbon_emission_factor
                
                calculation = {
                    'material_type': material.get('material_type', ''),
                    'sub_material_type': material.get('sub_material_type', ''),
                    'quantity': quantity,
                    'unit': material.get('unit', ''),
                    'embedded_carbon_energy': embedded_carbon_energy,
                    'carbon_emission_factor': carbon_emission_factor,
                    'total_carbon_emission': carbon_emission,
                    'form_name': material.get('form_name', ''),
                    'component': material.get('component', '')
                }
                
                calculations.append(calculation)
                total_carbon_emission += carbon_emission
                
            except (ValueError, TypeError) as e:
                print(f"Error calculating for material {material}: {e}")
                continue
        
        result = {
            'success': True,
            'calculations': calculations,
            'total_carbon_emission': total_carbon_emission,
            'total_materials': len(calculations),
            'timestamp': datetime.now().isoformat()
        }
        
        # Save calculation results
        carbon_emission_storage['calculation_results'] = result
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@carbon_emission_bp.route('/get-carbon-emission-data', methods=['GET'])
def get_carbon_emission_data():
    """Get saved carbon emission data"""
    try:
        # Try to load from file first
        file_data = load_carbon_emission_data_from_file()
        
        if file_data:
            return jsonify({
                'success': True,
                'data': file_data
            })
        
        # If no file data, return memory data
        if 'current_data' in carbon_emission_storage:
            return jsonify({
                'success': True,
                'data': carbon_emission_storage['current_data']
            })
        
        return jsonify({
            'success': True,
            'data': {
                'materials': [],
                'total_carbon_emission': 0
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@carbon_emission_bp.route('/get-carbon-calculation-results', methods=['GET'])
def get_carbon_calculation_results():
    """Get carbon emission calculation results"""
    try:
        if 'calculation_results' in carbon_emission_storage:
            return jsonify(carbon_emission_storage['calculation_results'])
        
        return jsonify({
            'success': True,
            'calculations': [],
            'total_carbon_emission': 0,
            'total_materials': 0
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
@carbon_emission_bp.route('/save-carbon-emission-materials', methods=['POST'])
def save_carbon_emission_materials():
    """Save carbon emission materials data to database"""
    try:
        data = request.get_json()
        data['timestamp'] = datetime.now().isoformat()
        
        db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO calculation_results (calculation_type, result_data, created_at)
                VALUES (?, ?, ?)
            ''', ('carbon_emission_materials', json.dumps(data), datetime.now().isoformat()))
            conn.commit()
        
        return jsonify({'success': True, 'message': 'Materials saved to database'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@carbon_emission_bp.route('/save-carbon-cost-parameters', methods=['POST'])
def save_carbon_cost_parameters():
    """Save carbon cost parameters to database"""
    try:
        data = request.get_json()
        data['timestamp'] = datetime.now().isoformat()
        
        db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO calculation_results (calculation_type, result_data, created_at)
                VALUES (?, ?, ?)
            ''', ('carbon_cost_parameters', json.dumps(data), datetime.now().isoformat()))
            conn.commit()
        
        return jsonify({'success': True, 'message': 'Cost parameters saved to database'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@carbon_emission_bp.route('/update-carbon-emission-factors', methods=['POST'])
def update_carbon_emission_factors():
    """Update carbon emission factors for materials"""
    try:
        data = request.get_json()
        
        if not data or 'material_name' not in data or 'factors' not in data:
            return jsonify({
                'success': False,
                'error': 'Invalid data format'
            }), 400
        
        material_name = data['material_name']
        factors = data['factors']
        
        # Update global factors
        CARBON_EMISSION_FACTORS[material_name] = factors
        
        return jsonify({
            'success': True,
            'message': f'Carbon emission factors updated for {material_name}'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500