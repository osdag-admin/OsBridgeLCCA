# Add these routes to your existing traffic_analysis.py file or create a new route file

from flask import Blueprint, request, jsonify
import json
from datetime import datetime

# If adding to existing file, use your existing blueprint name
# If creating new file, create new blueprint
traffic_analysis_bp = Blueprint('traffic_analysis', __name__)

# Global storage for traffic data
traffic_data_storage = {}

# Predefined IRC Road Costs data (replacing database)
IRC_ROAD_COSTS_DATA = {
    # Format: (Vehicle_Type, Lane_Type, Roughness, RF): Grand_Cost
    ("Car", "2", "Good", "Rolling"): 15.50,
    ("Car", "2", "Good", "Hilly"): 18.20,
    ("Car", "2", "Fair", "Rolling"): 17.80,
    ("Car", "2", "Fair", "Hilly"): 20.90,
    ("Car", "2", "Poor", "Rolling"): 22.40,
    ("Car", "2", "Poor", "Hilly"): 26.10,
    ("Car", "4", "Good", "Rolling"): 14.20,
    ("Car", "4", "Good", "Hilly"): 16.80,
    ("Car", "4", "Fair", "Rolling"): 16.50,
    ("Car", "4", "Fair", "Hilly"): 19.40,
    ("Car", "4", "Poor", "Rolling"): 21.10,
    ("Car", "4", "Poor", "Hilly"): 24.70,
    
    ("Bus", "2", "Good", "Rolling"): 45.80,
    ("Bus", "2", "Good", "Hilly"): 52.30,
    ("Bus", "2", "Fair", "Rolling"): 48.90,
    ("Bus", "2", "Fair", "Hilly"): 55.80,
    ("Bus", "2", "Poor", "Rolling"): 56.20,
    ("Bus", "2", "Poor", "Hilly"): 64.10,
    ("Bus", "4", "Good", "Rolling"): 42.50,
    ("Bus", "4", "Good", "Hilly"): 48.70,
    ("Bus", "4", "Fair", "Rolling"): 45.60,
    ("Bus", "4", "Fair", "Hilly"): 52.10,
    ("Bus", "4", "Poor", "Rolling"): 53.80,
    ("Bus", "4", "Poor", "Hilly"): 61.40,
    
    ("HCV", "2", "Good", "Rolling"): 78.90,
    ("HCV", "2", "Good", "Hilly"): 89.20,
    ("HCV", "2", "Fair", "Rolling"): 84.50,
    ("HCV", "2", "Fair", "Hilly"): 95.60,
    ("HCV", "2", "Poor", "Rolling"): 96.80,
    ("HCV", "2", "Poor", "Hilly"): 109.50,
    ("HCV", "4", "Good", "Rolling"): 75.40,
    ("HCV", "4", "Good", "Hilly"): 85.30,
    ("HCV", "4", "Fair", "Rolling"): 81.20,
    ("HCV", "4", "Fair", "Hilly"): 91.80,
    ("HCV", "4", "Poor", "Rolling"): 93.70,
    ("HCV", "4", "Poor", "Hilly"): 106.00,
    
    ("MCV", "2", "Good", "Rolling"): 56.70,
    ("MCV", "2", "Good", "Hilly"): 64.80,
    ("MCV", "2", "Fair", "Rolling"): 61.20,
    ("MCV", "2", "Fair", "Hilly"): 69.90,
    ("MCV", "2", "Poor", "Rolling"): 70.50,
    ("MCV", "2", "Poor", "Hilly"): 80.40,
    ("MCV", "4", "Good", "Rolling"): 54.30,
    ("MCV", "4", "Good", "Hilly"): 62.10,
    ("MCV", "4", "Fair", "Rolling"): 58.80,
    ("MCV", "4", "Fair", "Hilly"): 67.20,
    ("MCV", "4", "Poor", "Rolling"): 68.20,
    ("MCV", "4", "Poor", "Hilly"): 77.90,
    
    ("LCV", "2", "Good", "Rolling"): 38.40,
    ("LCV", "2", "Good", "Hilly"): 44.10,
    ("LCV", "2", "Fair", "Rolling"): 41.60,
    ("LCV", "2", "Fair", "Hilly"): 47.70,
    ("LCV", "2", "Poor", "Rolling"): 48.30,
    ("LCV", "2", "Poor", "Hilly"): 55.40,
    ("LCV", "4", "Good", "Rolling"): 36.80,
    ("LCV", "4", "Good", "Hilly"): 42.30,
    ("LCV", "4", "Fair", "Rolling"): 40.10,
    ("LCV", "4", "Fair", "Hilly"): 46.00,
    ("LCV", "4", "Poor", "Rolling"): 46.90,
    ("LCV", "4", "Poor", "Hilly"): 53.80,
}

@traffic_analysis_bp.route('/api/save-traffic-data', methods=['POST'])
def save_traffic_data():
    """Save traffic analysis data"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['road_user_inputs']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Validate road_user_inputs structure
        road_user_inputs = data['road_user_inputs']
        required_road_fields = ['Lane_Type', 'Roughness', 'RF', 'Vehicles']
        for field in required_road_fields:
            if field not in road_user_inputs:
                return jsonify({
                    'success': False,
                    'error': f'Missing required road_user_inputs field: {field}'
                }), 400
        
        # Store the data with timestamp
        timestamp = datetime.now().isoformat()
        traffic_data_storage[timestamp] = {
            'data': data,
            'timestamp': timestamp
        }
        
        print(f"Traffic data saved successfully at {timestamp}")
        print(f"Data: {json.dumps(data, indent=2)}")
        
        return jsonify({
            'success': True,
            'message': 'Traffic data saved successfully',
            'timestamp': timestamp,
            'data': data
        })
        
    except Exception as e:
        print(f"Error saving traffic data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@traffic_analysis_bp.route('/api/calculate-road-user-cost', methods=['POST'])
def calculate_road_user_cost():
    """Calculate road user cost based on traffic data using predefined data"""
    try:
        data = request.json
        
        # Extract data
        road_user_inputs = data.get('road_user_inputs', {})
        financial_inputs = data.get('financial_inputs', {})
        
        # Get construction time and reroute distance
        construction_time = financial_inputs.get('construction_time', 12)  # Default 12 months
        reroute_distance = financial_inputs.get('reroute_distance', 0)
        
        # Get road parameters
        lane_type = road_user_inputs.get('Lane_Type', '')
        roughness = road_user_inputs.get('Roughness', '')
        rf = road_user_inputs.get('RF', '')
        vehicles = road_user_inputs.get('Vehicles', [])
        
        print(f"=== ROAD USER COST CALCULATION START ===")
        print(f"Original Parameters: Lane_Type={lane_type}, Roughness={roughness}, RF={rf}")
        print(f"Construction Time: {construction_time}, Reroute Distance: {reroute_distance}")
        print(f"Vehicles: {vehicles}")
        
        if not vehicles:
            return jsonify({
                'success': False,
                'error': 'No vehicle data provided'
            }), 400
        
        # Handle empty parameters - set defaults if needed
        if not lane_type:
            lane_type = "2"  # Default to 2 lanes
            print(f"Warning: Lane_Type was empty, using default: {lane_type}")
        
        if not roughness:
            roughness = "Good"  # Default to Good
            print(f"Warning: Roughness was empty, using default: {roughness}")
        
        # FIX: Convert RF value to proper format
        if not rf or rf in ['', '0', 0]:
            rf = "Rolling"  # Default to Rolling
            print(f"Warning: RF was empty, using default: {rf}")
        else:
            # Convert numeric RF to text format
            try:
                rf_num = float(rf)
                if rf_num <= 3:
                    rf = "Rolling"
                else:
                    rf = "Hilly"
                print(f"Converted RF from {rf_num} to: {rf}")
            except (ValueError, TypeError):
                # If RF is already text, validate it
                if rf.lower() not in ['rolling', 'hilly']:
                    rf = "Rolling"  # Default fallback
                    print(f"Invalid RF value, using default: {rf}")
                else:
                    rf = rf.title()  # Capitalize first letter
                    print(f"Using RF: {rf}")
        
        print(f"Final Parameters: Lane_Type={lane_type}, Roughness={roughness}, RF={rf}")
        
        total_cost = 0
        calculation_details = []
        
        # Calculate cost for each vehicle type
        for vehicle in vehicles:
            vehicle_type = vehicle.get('Vehicle_Type', '')
            count = vehicle.get('Count', 0)
            
            if count <= 0:
                continue
            
            # Look up cost from predefined data
            lookup_key = (vehicle_type, lane_type, roughness, rf)
            print(f"Looking up key: {lookup_key}")
            
            if lookup_key in IRC_ROAD_COSTS_DATA:
                grand_cost = IRC_ROAD_COSTS_DATA[lookup_key]
                
                # Calculate cost: vehicles_affected * vehicle_operation_cost * construction_time
                ct = construction_time * reroute_distance if reroute_distance > 0 else construction_time
                vehicle_cost = count * grand_cost * ct
                
                total_cost += vehicle_cost
                
                calculation_details.append({
                    'vehicle_type': vehicle_type,
                    'count': count,
                    'grand_cost': grand_cost,
                    'construction_time': ct,
                    'vehicle_cost': vehicle_cost,
                    'lookup_key': lookup_key
                })
                
                print(f"✓ Vehicle: {vehicle_type}, Count: {count}, Grand Cost: {grand_cost}, CT: {ct}, Vehicle Cost: {vehicle_cost}")
            else:
                print(f"✗ No cost data found for vehicle: {vehicle_type} with parameters: Lane={lane_type}, Roughness={roughness}, RF={rf}")
                
                # Show available options for this vehicle type
                available_options = [key for key in IRC_ROAD_COSTS_DATA.keys() if key[0] == vehicle_type]
                print(f"Available options for {vehicle_type}: {available_options}")
                
                calculation_details.append({
                    'vehicle_type': vehicle_type,
                    'count': count,
                    'error': f'No cost data found for this vehicle with given parameters: {lookup_key}',
                    'available_options': available_options
                })
        
        # Store calculation result in memory
        calculation_result = {
            'total_road_user_cost': total_cost,
            'calculation_details': calculation_details,
            'parameters': {
                'lane_type': lane_type,
                'roughness': roughness,
                'rf': rf,
                'construction_time': construction_time,
                'reroute_distance': reroute_distance
            }
        }
        
        timestamp = datetime.now().isoformat()
        traffic_data_storage[f"calculation_{timestamp}"] = calculation_result
        
        # SAVE TO DATABASE
        try:
            import sqlite3
            import os
            
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
            db_path = os.path.abspath(db_path)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # Create table if it doesn't exist
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS calculation_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        calculation_type TEXT NOT NULL,
                        result_data TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )
                ''')
                
                # Delete existing road user cost calculation
                cursor.execute('''
                    DELETE FROM calculation_results 
                    WHERE calculation_type = 'road_user_cost_calculated'
                ''')
                
                # Save new calculation result
                result_data = {
                    'road_user_cost': total_cost,
                    'calculation_details': calculation_details,
                    'parameters': {
                        'lane_type': lane_type,
                        'roughness': roughness,
                        'rf': rf,
                        'construction_time': construction_time,
                        'reroute_distance': reroute_distance
                    },
                    'calculated_at': timestamp
                }
                
                cursor.execute('''
                    INSERT INTO calculation_results (calculation_type, result_data, created_at)
                    VALUES (?, ?, ?)
                ''', ('road_user_cost_calculated', json.dumps(result_data), timestamp))
                
                conn.commit()
                
                print(f"=== ROAD USER COST SAVED TO DATABASE ===")
                print(f"Total Cost: ₹{total_cost:.2f}")
                print(f"Database Path: {db_path}")
                print("=======================================")
                
        except Exception as db_error:
            print(f"Error saving road user cost to database: {db_error}")
            import traceback
            traceback.print_exc()
            # Don't fail the main operation if database save fails
        
        print(f"=== ROAD USER COST CALCULATION COMPLETE ===")
        print(f"Total Road User Cost: {total_cost}")
        print(f"Calculation Details: {json.dumps(calculation_details, indent=2)}")
        
        return jsonify({
            'success': True,
            'road_user_cost': total_cost,
            'calculation_details': calculation_details,
            'parameters': calculation_result['parameters'],
            'message': 'Road user cost calculated successfully'
        })
        
    except Exception as e:
        print(f"Error calculating road user cost: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@traffic_analysis_bp.route('/api/get-traffic-data', methods=['GET'])
def get_traffic_data():
    """Get all stored traffic data"""
    try:
        return jsonify({
            'success': True,
            'data': traffic_data_storage,
            'message': 'Traffic data retrieved successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
# In save_traffic_data function, add database storage:
def save_to_database(data):
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO calculation_results (calculation_type, result_data, created_at)
            VALUES (?, ?, ?)
        ''', ('traffic_data', json.dumps(data), datetime.now().isoformat()))
        
        # Also store road user cost calculation
        cursor.execute('''
            INSERT OR REPLACE INTO calculation_results (calculation_type, result_data, created_at)
            VALUES (?, ?, ?)
        ''', ('road_user_cost', json.dumps({'road_user_cost': total_cost}), datetime.now().isoformat()))
        
        conn.commit()

@traffic_analysis_bp.route('/api/clear-traffic-data', methods=['DELETE'])
def clear_traffic_data():
    """Clear all stored traffic data"""
    try:
        traffic_data_storage.clear()
        return jsonify({
            'success': True,
            'message': 'All traffic data cleared successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500