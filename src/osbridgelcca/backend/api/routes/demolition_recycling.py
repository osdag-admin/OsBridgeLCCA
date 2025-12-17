from flask import Blueprint, request, jsonify
from datetime import datetime

# Import SQLAlchemy models - SAME as structure_works.py and maintenance_calculations.py
from api.models.database import (
    get_db_session, 
    get_or_create_project, 
    CalculationResults,
    FormData
)

# Import cost component classes
from core.cost_component import (
    DemolitionCost,
    RecyclingCost
)

demolition_recycling_calculations_bp = Blueprint('demolition_recycling_calculations', __name__)

def get_initial_construction_cost():
    """Retrieve initial construction cost from SQLAlchemy database"""
    session = None
    try:
        session = get_db_session()
        project = get_or_create_project(session, "default")
        
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

def get_steel_quantity():
    """Retrieve steel quantity from structure forms"""
    session = None
    try:
        session = get_db_session()
        project = get_or_create_project(session, "default")
        
        # Get all structure forms
        structure_forms = ['foundation', 'sub-structure', 'super-structure', 'miscellaneous']
        total_steel_kg = 0
        
        for form_name in structure_forms:
            form_data = session.query(FormData).filter_by(
                project_id=project.id, 
                form_name=form_name
            ).first()
            
            if form_data and form_data.materials:
                for material in form_data.materials:
                    material_type = material.get('materialType', '').lower()
                    if 'steel' in material_type or 'reinforcement' in material_type:
                        quantity = float(material.get('quantity', 0))
                        unit = material.get('unit', '').lower()
                        
                        # Convert to kg
                        if unit == 'mt' or unit == 'ton':
                            quantity = quantity * 1000  # MT to kg
                        elif unit == 'quintal':
                            quantity = quantity * 100  # Quintal to kg
                        
                        total_steel_kg += quantity
        
        # Convert kg to MT for output
        total_steel_mt = total_steel_kg / 1000
        
        if total_steel_mt > 0:
            print(f"✓ Retrieved steel quantity: {total_steel_mt:.2f} MT ({total_steel_kg:.2f} kg)")
        else:
            print("✗ No steel quantity found in forms")
        
        return total_steel_kg, total_steel_mt
        
    except Exception as e:
        print(f"Error retrieving steel quantity: {e}")
        return 0, 0
    finally:
        if session:
            session.close()

@demolition_recycling_calculations_bp.route('/api/calculate-and-store-demolition-costs', methods=['POST'])
def calculate_and_store_demolition_costs():
    """
    Calculate demolition and recycling costs using cost components
    Expected input format:
    {
        "demolitionCostRate": "10",
        "scrapValueOfStructuralSteel": "50000",
        "structuralSteelScrap": "98"
    }
    """
    session = None
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['demolitionCostRate', 'scrapValueOfStructuralSteel', 'structuralSteelScrap']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Parse input values
        demolition_rate = float(data['demolitionCostRate']) / 100  # Convert % to decimal
        scrap_value = float(data['scrapValueOfStructuralSteel'])  # ₹ per MT
        scrap_rate = float(data['structuralSteelScrap']) / 100  # Convert % to decimal
        
        # Get required data from SQLAlchemy database
        initial_construction_cost = get_initial_construction_cost()
        if initial_construction_cost is None:
            return jsonify({
                'error': 'Initial construction cost not available. Please complete Structure Works forms first.'
            }), 400
        
        discount_rate, design_life = get_financial_parameters()
        steel_kg, steel_mt = get_steel_quantity()
        
        print("\n=== CALCULATING DEMOLITION & RECYCLING COSTS ===")
        print(f"Initial Construction Cost: ₹{initial_construction_cost:,.2f}")
        print(f"Demolition Rate: {demolition_rate*100}%")
        print(f"Steel Quantity: {steel_mt:.2f} MT")
        print(f"Scrap Value: ₹{scrap_value:,.2f} per MT")
        print(f"Scrap Rate: {scrap_rate*100}%")
        print(f"Discount Rate: {discount_rate*100}%")
        print(f"Design Life: {design_life} years")
        
        # 1. Calculate Demolition Cost
        demolition_component = DemolitionCost(
            demolition_rate=demolition_rate,
            construction_cost=initial_construction_cost,
            discount_rate=discount_rate,
            design_life=design_life
        )
        demolition_cost = demolition_component.calculate_cost()
        
        # 2. Calculate Recycling Cost (negative because it's revenue)
        # RecyclingCost component expects: scrap_value, quantity (MT), scrap_rate, discount_rate, design_life
        recycling_component = RecyclingCost(
            scrap_value=scrap_value,
            quantity=steel_mt,  # Pass MT directly
            scrap_rate=scrap_rate,
            discount_rate=discount_rate,
            design_life=design_life
        )
        recycling_cost = recycling_component.calculate_cost()  # This will be negative (revenue)
        
        # Calculate net demolition cost
        net_demolition_cost = demolition_cost + recycling_cost  # recycling_cost is negative
        
        # Calculate recoverable steel
        recoverable_steel_mt = steel_mt * scrap_rate
        
        # Prepare result data
        result_data = {
            'demolition_cost': demolition_cost,
            'recycling_revenue': abs(recycling_cost),  # Store as positive for display
            'recycling_cost': recycling_cost,  # Actual negative value
            'net_demolition_cost': net_demolition_cost,
            'input_parameters': {
                'demolition_rate': demolition_rate,
                'scrap_value_per_mt': scrap_value,
                'scrap_rate': scrap_rate
            },
            'calculation_parameters': {
                'initial_construction_cost': initial_construction_cost,
                'total_steel_mt': steel_mt,
                'total_steel_kg': steel_kg,
                'recoverable_steel_mt': recoverable_steel_mt,
                'discount_rate': discount_rate,
                'design_life': design_life
            },
            'calculated_at': datetime.now().isoformat()
        }
        
        # Store in SQLAlchemy database
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            # Delete existing demolition cost calculations
            session.query(CalculationResults).filter_by(
                project_id=project.id,
                calculation_type='demolition_recycling_costs'
            ).delete()
            
            # Insert new calculation
            calc_result = CalculationResults(
                project_id=project.id,
                calculation_type='demolition_recycling_costs',
                result_data=result_data
            )
            session.add(calc_result)
            session.commit()
            
            print("\n=== DEMOLITION & RECYCLING COSTS CALCULATED ===")
            print(f"Demolition Cost: ₹{demolition_cost:,.2f}")
            print(f"Recycling Revenue: ₹{abs(recycling_cost):,.2f}")
            print(f"Net Demolition Cost: ₹{net_demolition_cost:,.2f}")
            print(f"Recoverable Steel: {recoverable_steel_mt:.2f} MT")
            print(f"Stored in SQLAlchemy database")
            print("=" * 48)
            
            return jsonify({
                'success': True,
                'message': 'Demolition and recycling costs calculated and stored successfully',
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
        print(f"Error calculating demolition costs: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@demolition_recycling_calculations_bp.route('/api/get-stored-demolition-costs', methods=['GET'])
def get_stored_demolition_costs():
    """Retrieve stored demolition and recycling costs from SQLAlchemy database"""
    session = None
    try:
        session = get_db_session()
        project = get_or_create_project(session, "default")
        
        calc_result = session.query(CalculationResults).filter_by(
            project_id=project.id,
            calculation_type='demolition_recycling_costs'
        ).order_by(CalculationResults.created_at.desc()).first()
        
        if calc_result and calc_result.result_data:
            return jsonify({
                'success': True,
                'results': calc_result.result_data
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'No demolition costs found in database'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        if session:
            session.close()

@demolition_recycling_calculations_bp.route('/api/debug/demolition-dependencies', methods=['GET'])
def debug_demolition_dependencies():
    """Debug endpoint to check if all required data is available"""
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
                'value': cost
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
        
        # Check steel quantity
        steel_kg, steel_mt = get_steel_quantity()
        if steel_mt > 0:
            debug_info['dependencies']['steel_quantity'] = {
                'status': 'AVAILABLE',
                'steel_mt': steel_mt,
                'steel_kg': steel_kg
            }
        else:
            debug_info['dependencies']['steel_quantity'] = {
                'status': 'MISSING',
                'message': 'No steel found in structure forms'
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