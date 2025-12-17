from flask import Blueprint, request, jsonify
import json
from datetime import datetime

# Import SQLAlchemy models - SAME as structure_works.py
from api.models.database import (
    get_db_session, 
    get_or_create_project, 
    CalculationResults
)

# Import cost component classes
from core.cost_component import (
    PeriodicMaintenanceCost,
    PeriodicMaintenanceCarbonCost,
    RoutineInspectionCost,
    RepairAndRehabilitationCost
)

maintenance_calculations_bp = Blueprint('maintenance_calculations', __name__)

def get_initial_construction_cost():
    """Retrieve initial construction cost from SQLAlchemy database"""
    session = None
    try:
        session = get_db_session()
        project = get_or_create_project(session, "default")
        
        # Query from SQLAlchemy database
        calc_result = session.query(CalculationResults).filter_by(
            project_id=project.id,
            calculation_type='initial_construction_cost_auto'
        ).order_by(CalculationResults.created_at.desc()).first()
        
        if calc_result and calc_result.result_data:
            cost = float(calc_result.result_data.get('total_initial_cost', 0))
            print(f"✓ Retrieved initial construction cost: ₹{cost:,.2f}")
            return cost
        else:
            print("✗ No initial construction cost found")
            return None
            
    except Exception as e:
        print(f"Error retrieving initial construction cost: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if session:
            session.close()

def get_financial_parameters():
    """Retrieve discount rate and design life from SQLAlchemy database"""
    session = None
    try:
        session = get_db_session()
        project = get_or_create_project(session, "default")
        
        # Get from financial_data calculation result
        calc_result = session.query(CalculationResults).filter_by(
            project_id=project.id,
            calculation_type='financial_data'
        ).order_by(CalculationResults.created_at.desc()).first()
        
        if calc_result and calc_result.result_data:
            data = calc_result.result_data
            discount_rate = float(data.get('realDiscountRate', 2.0)) / 100
            design_life = int(data.get('durationOfStudy', 50))
            print(f"✓ Retrieved financial parameters - Discount Rate: {discount_rate*100}%, Design Life: {design_life} years")
            return discount_rate, design_life
        else:
            print("✗ No financial data found, using defaults")
            return 0.02, 50
            
    except Exception as e:
        print(f"Error retrieving financial parameters: {e}")
        return 0.02, 50
    finally:
        if session:
            session.close()

def get_carbon_emission_data():
    """Retrieve concrete quantity and emission factor from SQLAlchemy database"""
    session = None
    try:
        session = get_db_session()
        project = get_or_create_project(session, "default")
        
        # Get from carbon_emission_materials
        calc_result = session.query(CalculationResults).filter_by(
            project_id=project.id,
            calculation_type='carbon_emission_materials'
        ).order_by(CalculationResults.created_at.desc()).first()
        
        if calc_result and calc_result.result_data:
            data = calc_result.result_data
            materials = data.get('materials', [])
            
            total_concrete_kg = 0
            concrete_emission_factor = 0
            
            for material in materials:
                material_type = material.get('material_type', '').lower()
                if 'concrete' in material_type:
                    quantity = float(material.get('quantity', 0))
                    unit = material.get('unit', '').lower()
                    
                    # Convert to kg if needed
                    if unit == 'cum':
                        quantity = quantity * 2549.25
                    
                    total_concrete_kg += quantity
                    concrete_emission_factor = float(material.get('carbon_emission_factor', 0))
            
            print(f"✓ Retrieved concrete data - Quantity: {total_concrete_kg:.2f} kg, Emission Factor: {concrete_emission_factor}")
            return total_concrete_kg, concrete_emission_factor
        else:
            print("✗ No carbon emission materials found")
            return 0, 0
            
    except Exception as e:
        print(f"Error retrieving carbon emission data: {e}")
        return 0, 0
    finally:
        if session:
            session.close()

def get_social_cost_of_carbon():
    """Retrieve social cost of carbon from SQLAlchemy database"""
    session = None
    try:
        session = get_db_session()
        project = get_or_create_project(session, "default")
        
        calc_result = session.query(CalculationResults).filter_by(
            project_id=project.id,
            calculation_type='carbon_cost_parameters'
        ).order_by(CalculationResults.created_at.desc()).first()
        
        if calc_result and calc_result.result_data:
            data = calc_result.result_data
            carbon_cost = float(data.get('socialCostOfCarbon', 6.3936))
            print(f"✓ Retrieved social cost of carbon: ₹{carbon_cost}/kgCO₂e")
            return carbon_cost
        else:
            print("✗ No carbon cost parameters found, using default")
            return 6.3936
            
    except Exception as e:
        print(f"Error retrieving social cost of carbon: {e}")
        return 6.3936
    finally:
        if session:
            session.close()

@maintenance_calculations_bp.route('/api/calculate-and-store-maintenance-costs', methods=['POST'])
def calculate_and_store_maintenance_costs():
    """
    Calculate all maintenance costs and store in SQLAlchemy database
    Expected input format:
    {
        "periodicMaintenanceCost": "0.5500",
        "annualRoutineInspectionCost": "1",
        "repairRehabilitationCost": "10",
        "frequencyOfPeriodicMaintenance": "5",
        "frequencyOfRoutineInspection": "1"
    }
    """
    session = None
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'periodicMaintenanceCost',
            'annualRoutineInspectionCost',
            'repairRehabilitationCost',
            'frequencyOfPeriodicMaintenance',
            'frequencyOfRoutineInspection'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Parse input rates (convert from percentage strings to decimals)
        periodic_maintenance_rate = float(data['periodicMaintenanceCost']) / 100
        routine_inspection_rate = float(data['annualRoutineInspectionCost']) / 100
        repair_rehabilitation_rate = float(data['repairRehabilitationCost']) / 100
        
        # Parse frequencies
        frequency_periodic = int(data['frequencyOfPeriodicMaintenance'])
        frequency_routine = int(data['frequencyOfRoutineInspection'])
        
        # Get required data from SQLAlchemy database
        initial_construction_cost = get_initial_construction_cost()
        if initial_construction_cost is None:
            return jsonify({
                'error': 'Initial construction cost not available. Please complete Structure Works forms first.'
            }), 400
        
        discount_rate, design_life = get_financial_parameters()
        concrete_kg, concrete_emission_factor = get_carbon_emission_data()
        carbon_cost = get_social_cost_of_carbon()
        
        print("\n=== CALCULATING MAINTENANCE COSTS ===")
        print(f"Initial Construction Cost: ₹{initial_construction_cost:,.2f}")
        print(f"Discount Rate: {discount_rate*100}%")
        print(f"Design Life: {design_life} years")
        print(f"Concrete Quantity: {concrete_kg:.2f} kg")
        print(f"Concrete Emission Factor: {concrete_emission_factor} kgCO₂e/kg")
        print(f"Social Cost of Carbon: ₹{carbon_cost}/kgCO₂e")
        
        # 1. Calculate Periodic Maintenance Cost
        periodic_maintenance_component = PeriodicMaintenanceCost(
            maintenance_cost_rate=periodic_maintenance_rate,
            construction_cost=initial_construction_cost,
            discount_rate=discount_rate,
            period=frequency_periodic,
            design_life=design_life
        )
        periodic_maintenance_cost = periodic_maintenance_component.calculate_cost()
        
        # 2. Calculate Periodic Maintenance Carbon Cost
        periodic_maintenance_carbon_component = PeriodicMaintenanceCarbonCost(
            material_quantity=concrete_kg,
            carbon_emission_factor=concrete_emission_factor,
            carbon_cost=carbon_cost,
            discount_rate=discount_rate,
            period=frequency_periodic,
            design_life=design_life
        )
        periodic_maintenance_carbon_cost = periodic_maintenance_carbon_component.calculate_cost()
        
        # 3. Calculate Routine Inspection Cost
        routine_inspection_component = RoutineInspectionCost(
            inspection_cost_rate=routine_inspection_rate,
            construction_cost=initial_construction_cost,
            discount_rate=discount_rate,
            design_life=design_life,
            period=frequency_routine
        )
        routine_inspection_cost = routine_inspection_component.calculate_cost()
        
        # 4. Calculate Repair & Rehabilitation Cost
        repair_frequency = 30  # Default value
        repair_rehabilitation_component = RepairAndRehabilitationCost(
            repair_cost_rate=repair_rehabilitation_rate,
            construction_cost=initial_construction_cost,
            discount_rate=discount_rate,
            period=repair_frequency,
            design_life=design_life
        )
        repair_rehabilitation_cost = repair_rehabilitation_component.calculate_cost()
        
        # Calculate total maintenance cost
        total_maintenance_cost = (
            periodic_maintenance_cost +
            periodic_maintenance_carbon_cost +
            routine_inspection_cost +
            repair_rehabilitation_cost
        )
        
        # Prepare result data
        result_data = {
            'periodic_maintenance_cost': periodic_maintenance_cost,
            'periodic_maintenance_carbon_cost': periodic_maintenance_carbon_cost,
            'routine_inspection_cost': routine_inspection_cost,
            'repair_rehabilitation_cost': repair_rehabilitation_cost,
            'total_maintenance_cost': total_maintenance_cost,
            'input_parameters': {
                'periodic_maintenance_rate': periodic_maintenance_rate,
                'routine_inspection_rate': routine_inspection_rate,
                'repair_rehabilitation_rate': repair_rehabilitation_rate,
                'frequency_periodic': frequency_periodic,
                'frequency_routine': frequency_routine,
                'repair_frequency': repair_frequency
            },
            'calculation_parameters': {
                'initial_construction_cost': initial_construction_cost,
                'discount_rate': discount_rate,
                'design_life': design_life,
                'concrete_kg': concrete_kg,
                'concrete_emission_factor': concrete_emission_factor,
                'carbon_cost': carbon_cost
            },
            'calculated_at': datetime.now().isoformat()
        }
        
        # Store in SQLAlchemy database
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            # Delete existing maintenance cost calculations
            session.query(CalculationResults).filter_by(
                project_id=project.id,
                calculation_type='maintenance_costs'
            ).delete()
            
            # Insert new calculation
            calc_result = CalculationResults(
                project_id=project.id,
                calculation_type='maintenance_costs',
                result_data=result_data
            )
            session.add(calc_result)
            session.commit()
            
            print("\n=== MAINTENANCE COSTS CALCULATED & STORED ===")
            print(f"Periodic Maintenance Cost: ₹{periodic_maintenance_cost:,.2f}")
            print(f"Periodic Maintenance Carbon Cost: ₹{periodic_maintenance_carbon_cost:,.2f}")
            print(f"Routine Inspection Cost: ₹{routine_inspection_cost:,.2f}")
            print(f"Repair & Rehabilitation Cost: ₹{repair_rehabilitation_cost:,.2f}")
            print(f"Total Maintenance Cost: ₹{total_maintenance_cost:,.2f}")
            print(f"Stored in SQLAlchemy database")
            print("=" * 45)
            
            return jsonify({
                'success': True,
                'message': 'Maintenance costs calculated and stored successfully',
                'results': result_data
            }), 200
            
        finally:
            if session:
                session.close()
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid numeric value: {str(e)}'
        }), 400
    except Exception as e:
        import traceback
        print(f"Error calculating maintenance costs: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@maintenance_calculations_bp.route('/api/get-stored-maintenance-costs', methods=['GET'])
def get_stored_maintenance_costs():
    """Retrieve stored maintenance costs from SQLAlchemy database"""
    session = None
    try:
        session = get_db_session()
        project = get_or_create_project(session, "default")
        
        calc_result = session.query(CalculationResults).filter_by(
            project_id=project.id,
            calculation_type='maintenance_costs'
        ).order_by(CalculationResults.created_at.desc()).first()
        
        if calc_result and calc_result.result_data:
            return jsonify({
                'success': True,
                'results': calc_result.result_data
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'No maintenance costs found in database'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        if session:
            session.close()

@maintenance_calculations_bp.route('/api/debug/maintenance-dependencies', methods=['GET'])
def debug_maintenance_dependencies():
    """Debug endpoint to check if all required data is available in SQLAlchemy database"""
    session = None
    try:
        session = get_db_session()
        project = get_or_create_project(session, "default")
        
        debug_info = {
            'database_type': 'SQLAlchemy (same as structure_works)',
            'project_id': project.id,
            'project_name': project.name,
            'dependencies': {}
        }
        
        # Check initial construction cost
        calc_result = session.query(CalculationResults).filter_by(
            project_id=project.id,
            calculation_type='initial_construction_cost_auto'
        ).order_by(CalculationResults.created_at.desc()).first()
        
        if calc_result and calc_result.result_data:
            cost = calc_result.result_data.get('total_initial_cost', 0)
            debug_info['dependencies']['initial_construction_cost'] = {
                'status': 'AVAILABLE',
                'value': cost,
                'calculated_at': calc_result.result_data.get('calculated_at')
            }
        else:
            debug_info['dependencies']['initial_construction_cost'] = {
                'status': 'MISSING',
                'message': 'Complete Structure Works forms first'
            }
        
        # Check financial data
        calc_result = session.query(CalculationResults).filter_by(
            project_id=project.id,
            calculation_type='financial_data'
        ).order_by(CalculationResults.created_at.desc()).first()
        
        if calc_result and calc_result.result_data:
            data = calc_result.result_data
            debug_info['dependencies']['financial_data'] = {
                'status': 'AVAILABLE',
                'discount_rate': data.get('realDiscountRate'),
                'design_life': data.get('durationOfStudy')
            }
        else:
            debug_info['dependencies']['financial_data'] = {
                'status': 'MISSING (using defaults)',
                'defaults': {'discount_rate': '2%', 'design_life': '50 years'}
            }
        
        # Check carbon emission materials
        calc_result = session.query(CalculationResults).filter_by(
            project_id=project.id,
            calculation_type='carbon_emission_materials'
        ).order_by(CalculationResults.created_at.desc()).first()
        
        if calc_result and calc_result.result_data:
            materials = calc_result.result_data.get('materials', [])
            debug_info['dependencies']['carbon_emission_materials'] = {
                'status': 'AVAILABLE',
                'materials_count': len(materials)
            }
        else:
            debug_info['dependencies']['carbon_emission_materials'] = {
                'status': 'MISSING (using defaults)'
            }
        
        # Check carbon cost parameters
        calc_result = session.query(CalculationResults).filter_by(
            project_id=project.id,
            calculation_type='carbon_cost_parameters'
        ).order_by(CalculationResults.created_at.desc()).first()
        
        if calc_result and calc_result.result_data:
            data = calc_result.result_data
            debug_info['dependencies']['carbon_cost_parameters'] = {
                'status': 'AVAILABLE',
                'social_cost_of_carbon': data.get('socialCostOfCarbon')
            }
        else:
            debug_info['dependencies']['carbon_cost_parameters'] = {
                'status': 'MISSING (using default)',
                'default': 6.3936
            }
        
        # Overall status
        initial_cost_ok = debug_info['dependencies']['initial_construction_cost']['status'] == 'AVAILABLE'
        
        debug_info['can_calculate'] = initial_cost_ok
        debug_info['message'] = 'Ready to calculate' if initial_cost_ok else 'Complete Structure Works forms first'
        
        return jsonify(debug_info), 200
        
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500
    finally:
        if session:
            session.close()