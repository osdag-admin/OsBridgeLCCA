# from flask import Blueprint, request, jsonify
# import sys
# import os
# import sqlite3
# from typing import Dict, Any, List

# # Add the path to access the cost components
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))

# # Import your cost components
# from cost_component import (
#     InitialConstructionCost, InitialCarbonEmissionCost, TimeCost, 
#     RoadUserCost, AdditionalCarbonEmissionCost, PeriodicMaintenanceCost,
#     PeriodicMaintenanceCarbonCost, RoutineInspectionCost, RepairAndRehabilitationCost,
#     DemolitionCost, RecyclingCost, ReconstructionCost, UserInputs
# )

# cost_calculations_bp = Blueprint('cost_calculations', __name__)

# @cost_calculations_bp.route('/api/calculate-initial-construction-cost', methods=['POST'])
# def calculate_initial_construction_cost():
#     """Calculate initial construction cost from materials data"""
#     try:
#         data = request.json
#         materials = data.get('materials', [])
        
#         total_cost = 0
#         cost_breakdown = []
        
#         for material in materials:
#             component = InitialConstructionCost(
#                 quantity=material.get('quantity', 0),
#                 rate=material.get('rate', 0)
#             )
#             cost = component.calculate_cost()
#             total_cost += cost
            
#             cost_breakdown.append({
#                 'material': material.get('material', ''),
#                 'grade': material.get('grade', ''),
#                 'quantity': material.get('quantity', 0),
#                 'unit': material.get('unit', ''),
#                 'rate': material.get('rate', 0),
#                 'cost': cost
#             })
        
#         return jsonify({
#             'total_initial_construction_cost': total_cost,
#             'cost_breakdown': cost_breakdown,
#             'status': 'success'
#         })
    
#     except Exception as e:
#         return jsonify({
#             'error': str(e),
#             'status': 'error'
#         }), 400

# @cost_calculations_bp.route('/api/calculate-carbon-emission-cost', methods=['POST'])
# def calculate_carbon_emission_cost():
#     """Calculate initial carbon emission cost"""
#     try:
#         data = request.json
#         materials = data.get('materials', [])
#         carbon_cost = data.get('carbon_cost', 6.3936)
#         concrete_emission_factor = data.get('concrete_emission_factor', 0.084)
#         steel_emission_factor = data.get('steel_emission_factor', 2.6)
        
#         total_concrete_kg = 0
#         total_steel_kg = 0
        
#         # Calculate concrete and steel quantities
#         for material in materials:
#             if material.get('material', '').lower() == 'concrete':
#                 qty = material.get('quantity', 0)
#                 unit = material.get('unit', '').lower()
#                 if unit == 'cum':
#                     qty = qty * 2549.25  # density: kg/cum
#                 total_concrete_kg += qty
#             elif material.get('material', '').lower() == 'steel':
#                 qty = material.get('quantity', 0)
#                 unit = material.get('unit', '').upper()
#                 if unit == 'MT':
#                     qty = qty * 1000  # 1 MT = 1000 kg
#                 total_steel_kg += qty
        
#         # Calculate total carbon emission cost
#         concrete_carbon_cost = total_concrete_kg * concrete_emission_factor * carbon_cost
#         steel_carbon_cost = total_steel_kg * steel_emission_factor * carbon_cost
#         total_carbon_cost = concrete_carbon_cost + steel_carbon_cost
        
#         return jsonify({
#             'total_carbon_emission_cost': total_carbon_cost,
#             'concrete_carbon_cost': concrete_carbon_cost,
#             'steel_carbon_cost': steel_carbon_cost,
#             'total_concrete_kg': total_concrete_kg,
#             'total_steel_kg': total_steel_kg,
#             'status': 'success'
#         })
    
#     except Exception as e:
#         return jsonify({
#             'error': str(e),
#             'status': 'error'
#         }), 400

# @cost_calculations_bp.route('/api/calculate-time-cost', methods=['POST'])
# def calculate_time_cost():
#     """Calculate time cost due to construction delays"""
#     try:
#         data = request.json
#         construction_cost = data.get('construction_cost', 0)
#         interest_rate = data.get('interest_rate', 0.1)
#         construction_time = data.get('construction_time', 0.75)
#         investment_ratio = data.get('investment_ratio', 0.5)
        
#         time_cost_component = TimeCost(
#             construction_cost=construction_cost,
#             interest_rate=interest_rate,
#             time=construction_time,
#             investment_ratio=investment_ratio
#         )
        
#         time_cost = time_cost_component.calculate_cost()
        
#         return jsonify({
#             'time_cost': time_cost,
#             'construction_cost': construction_cost,
#             'interest_rate': interest_rate,
#             'construction_time': construction_time,
#             'investment_ratio': investment_ratio,
#             'status': 'success'
#         })
    
#     except Exception as e:
#         return jsonify({
#             'error': str(e),
#             'status': 'error'
#         }), 400

# @cost_calculations_bp.route('/api/calculate-road-user-cost', methods=['POST'])
# def calculate_road_user_cost():
#     """Calculate road user cost from traffic data"""
#     try:
#         data = request.json
#         vehicles = data.get('vehicles', [])
#         lane_type = data.get('lane_type', 'Single Lane Roads')
#         roughness = data.get('roughness', 2000)
#         rf = data.get('rf', 5)
#         construction_time = data.get('construction_time', 0.75)
#         reroute_distance = data.get('reroute_distance', 1.0)
        
#         # Database path
#         db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'IRC_Road_Costs.db')
#         db_path = os.path.abspath(db_path)
        
#         total_road_user_cost = 0
#         calculation_details = []
        
#         with sqlite3.connect(db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#             table_name = cursor.fetchone()[0]
            
#             for vehicle in vehicles:
#                 vehicle_type = vehicle.get('type', '')
#                 count = vehicle.get('count', 0)
                
#                 cursor.execute(f'''
#                     SELECT Grand_Cost FROM {table_name} WHERE 
#                         Vehicle_Type = ? AND Lane_Type = ? AND Roughness = ? AND RF = ?
#                 ''', (vehicle_type, lane_type, roughness, rf))
                
#                 result = cursor.fetchone()
#                 if result:
#                     grand_cost = result[0]
#                     ct = construction_time * reroute_distance
                    
#                     road_user_cost_component = RoadUserCost(
#                         vehicles_affected=count,
#                         vehicle_operation_cost=grand_cost,
#                         construction_time=ct
#                     )
                    
#                     vehicle_cost = road_user_cost_component.calculate_cost()
#                     total_road_user_cost += vehicle_cost
                    
#                     calculation_details.append({
#                         'vehicle_type': vehicle_type,
#                         'count': count,
#                         'grand_cost': grand_cost,
#                         'vehicle_cost': vehicle_cost
#                     })
        
#         return jsonify({
#             'total_road_user_cost': total_road_user_cost,
#             'calculation_details': calculation_details,
#             'status': 'success'
#         })
    
#     except Exception as e:
#         return jsonify({
#             'error': str(e),
#             'status': 'error'
#         }), 400

# @cost_calculations_bp.route('/api/calculate-additional-carbon-cost', methods=['POST'])
# def calculate_additional_carbon_cost():
#     """Calculate additional carbon emission cost from rerouted traffic"""
#     try:
#         data = request.json
#         vehicles = data.get('vehicles', [])
#         reroute_distance = data.get('reroute_distance', 1.0)
#         co2_emission_per_km = data.get('co2_emission_per_km', 0.1213)
#         carbon_cost = data.get('carbon_cost', 6.3936)
        
#         total_vehicles = sum(v.get('count', 0) for v in vehicles)
        
#         additional_carbon_component = AdditionalCarbonEmissionCost(
#             vehicles_affected=total_vehicles,
#             reroute_distance=reroute_distance,
#             co2_emission_per_km=co2_emission_per_km,
#             carbon_cost=carbon_cost
#         )
        
#         additional_carbon_cost = additional_carbon_component.calculate_cost()
        
#         return jsonify({
#             'additional_carbon_emission_cost': additional_carbon_cost,
#             'total_vehicles': total_vehicles,
#             'reroute_distance': reroute_distance,
#             'co2_emission_per_km': co2_emission_per_km,
#             'carbon_cost': carbon_cost,
#             'status': 'success'
#         })
    
#     except Exception as e:
#         return jsonify({
#             'error': str(e),
#             'status': 'error'
#         }), 400

# @cost_calculations_bp.route('/api/calculate-maintenance-costs', methods=['POST'])
# def calculate_maintenance_costs():
#     """Calculate all maintenance-related costs"""
#     try:
#         data = request.json
#         construction_cost = data.get('construction_cost', 0)
#         materials = data.get('materials', [])
        
#         # Maintenance parameters
#         maintenance_cost_rate = data.get('maintenance_cost_rate', 0.0055)
#         maintenance_period = data.get('maintenance_period', 5.0)
#         discount_rate = data.get('discount_rate', 0.0425)
#         design_life = data.get('design_life', 50.0)
        
#         # Inspection parameters
#         inspection_rate = data.get('inspection_rate', 0.01)
#         inspection_period = data.get('inspection_period', 1.0)
        
#         # Repair parameters
#         repair_cost_rate = data.get('repair_cost_rate', 0.10)
#         repair_period = data.get('repair_period', 30.0)
        
#         # Carbon parameters
#         concrete_co2_emission_factor = data.get('concrete_co2_emission_factor', 0.487032864540167)
#         carbon_cost = data.get('carbon_cost', 6.3936)
        
#         # Calculate periodic maintenance cost
#         periodic_maintenance_component = PeriodicMaintenanceCost(
#             maintenance_cost_rate=maintenance_cost_rate,
#             construction_cost=construction_cost,
#             discount_rate=discount_rate,
#             period=maintenance_period,
#             design_life=design_life
#         )
#         periodic_maintenance_cost = periodic_maintenance_component.calculate_cost()
        
#         # Calculate maintenance carbon cost (concrete only)
#         maintenance_concrete_kg = 0
#         for material in materials:
#             if material.get('material', '').lower() == 'concrete':
#                 qty = material.get('quantity', 0)
#                 unit = material.get('unit', '').lower()
#                 if unit == 'cum':
#                     qty = qty * 2549.25  # density: kg/cum
#                 maintenance_concrete_kg += qty
        
#         maintenance_carbon_component = PeriodicMaintenanceCarbonCost(
#             material_quantity=maintenance_concrete_kg,
#             carbon_emission_factor=concrete_co2_emission_factor,
#             carbon_cost=carbon_cost,
#             discount_rate=discount_rate,
#             period=maintenance_period,
#             design_life=design_life
#         )
#         maintenance_carbon_cost = maintenance_carbon_component.calculate_cost()
        
#         # Calculate routine inspection cost
#         inspection_component = RoutineInspectionCost(
#             inspection_cost_rate=inspection_rate,
#             construction_cost=construction_cost,
#             discount_rate=discount_rate,
#             design_life=design_life,
#             period=inspection_period
#         )
#         inspection_cost = inspection_component.calculate_cost()
        
#         # Calculate repair and rehabilitation cost
#         repair_component = RepairAndRehabilitationCost(
#             repair_cost_rate=repair_cost_rate,
#             construction_cost=construction_cost,
#             discount_rate=discount_rate,
#             period=repair_period,
#             design_life=design_life
#         )
#         repair_cost = repair_component.calculate_cost()
        
#         return jsonify({
#             'periodic_maintenance_cost': periodic_maintenance_cost,
#             'maintenance_carbon_cost': maintenance_carbon_cost,
#             'routine_inspection_cost': inspection_cost,
#             'repair_rehabilitation_cost': repair_cost,
#             'total_maintenance_cost': periodic_maintenance_cost + maintenance_carbon_cost + inspection_cost + repair_cost,
#             'status': 'success'
#         })
    
#     except Exception as e:
#         return jsonify({
#             'error': str(e),
#             'status': 'error'
#         }), 400

# @cost_calculations_bp.route('/api/calculate-end-of-life-costs', methods=['POST'])
# def calculate_end_of_life_costs():
#     """Calculate demolition and recycling costs"""
#     try:
#         data = request.json
#         construction_cost = data.get('construction_cost', 0)
#         discount_rate = data.get('discount_rate', 0.0425)
#         design_life = data.get('design_life', 50.0)
        
#         # Demolition parameters
#         demolition_rate = data.get('demolition_rate', 0.10)
        
#         # Recycling parameters
#         steel_quantity = data.get('steel_quantity', 0)
#         steel_unit = data.get('steel_unit', 'MT')
#         scrap_value = data.get('scrap_value', 50000.0)
#         scrap_rate = data.get('scrap_rate', 0.98)
        
#         # Calculate demolition cost
#         demolition_component = DemolitionCost(
#             demolition_rate=demolition_rate,
#             construction_cost=construction_cost,
#             discount_rate=discount_rate,
#             design_life=design_life
#         )
#         demolition_cost = demolition_component.calculate_cost()
        
#         # Calculate recycling cost
#         if steel_unit.lower() == "kg":
#             steel_quantity_mt = steel_quantity / 1000
#         else:
#             steel_quantity_mt = steel_quantity
        
#         recycling_component = RecyclingCost(
#             scrap_value=scrap_value,
#             quantity=steel_quantity_mt,
#             scrap_rate=scrap_rate,
#             discount_rate=discount_rate,
#             design_life=design_life
#         )
#         recycling_cost = recycling_component.calculate_cost()
        
#         return jsonify({
#             'demolition_cost': demolition_cost,
#             'recycling_cost': recycling_cost,
#             'net_end_of_life_cost': demolition_cost - recycling_cost,
#             'status': 'success'
#         })
    
#     except Exception as e:
#         return jsonify({
#             'error': str(e),
#             'status': 'error'
#         }), 400

# @cost_calculations_bp.route('/api/calculate-complete-lcca', methods=['POST'])
# def calculate_complete_lcca():
#     """Calculate complete Life Cycle Cost Analysis"""
#     try:
#         data = request.json
        
#         # Extract all required parameters
#         materials = data.get('materials', [])
#         vehicles = data.get('vehicles', [])
        
#         # Financial parameters
#         discount_rate = data.get('discount_rate', 0.0425)
#         design_life = data.get('design_life', 50.0)
#         analysis_period = data.get('analysis_period', 50.0)
        
#         # Construction parameters
#         construction_time = data.get('construction_time', 0.75)
#         interest_rate = data.get('interest_rate', 0.1)
#         investment_ratio = data.get('investment_ratio', 0.5)
        
#         # Traffic parameters
#         lane_type = data.get('lane_type', 'Single Lane Roads')
#         roughness = data.get('roughness', 2000)
#         rf = data.get('rf', 5)
#         reroute_distance = data.get('reroute_distance', 1.0)
        
#         # Environmental parameters
#         carbon_cost = data.get('carbon_cost', 6.3936)
#         concrete_emission_factor = data.get('concrete_emission_factor', 0.084)
#         steel_emission_factor = data.get('steel_emission_factor', 2.6)
#         concrete_co2_emission_factor = data.get('concrete_co2_emission_factor', 0.487032864540167)
#         co2_emission_per_km = data.get('co2_emission_per_km', 0.1213)
        
#         # Maintenance parameters
#         maintenance_cost_rate = data.get('maintenance_cost_rate', 0.0055)
#         maintenance_period = data.get('maintenance_period', 5.0)
#         inspection_rate = data.get('inspection_rate', 0.01)
#         inspection_period = data.get('inspection_period', 1.0)
#         repair_cost_rate = data.get('repair_cost_rate', 0.10)
#         repair_period = data.get('repair_period', 30.0)
        
#         # End of life parameters
#         demolition_rate = data.get('demolition_rate', 0.10)
#         steel_quantity = data.get('steel_quantity', 0)
#         steel_unit = data.get('steel_unit', 'MT')
#         scrap_value = data.get('scrap_value', 50000.0)
#         scrap_rate = data.get('scrap_rate', 0.98)
        
#         # 1. Calculate Initial Construction Cost
#         total_construction_cost = 0
#         for material in materials:
#             component = InitialConstructionCost(
#                 quantity=material.get('quantity', 0),
#                 rate=material.get('rate', 0)
#             )
#             total_construction_cost += component.calculate_cost()
        
#         # 2. Calculate Initial Carbon Emission Cost
#         total_concrete_kg = 0
#         total_steel_kg = 0
#         for material in materials:
#             if material.get('material', '').lower() == 'concrete':
#                 qty = material.get('quantity', 0)
#                 if material.get('unit', '').lower() == 'cum':
#                     qty = qty * 2549.25
#                 total_concrete_kg += qty
#             elif material.get('material', '').lower() == 'steel':
#                 qty = material.get('quantity', 0)
#                 if material.get('unit', '').upper() == 'MT':
#                     qty = qty * 1000
#                 total_steel_kg += qty
        
#         carbon_emission_cost = (
#             (total_concrete_kg * concrete_emission_factor) + 
#             (total_steel_kg * steel_emission_factor)
#         ) * carbon_cost
        
#         # 3. Calculate Time Cost
#         time_cost_component = TimeCost(
#             construction_cost=total_construction_cost,
#             interest_rate=interest_rate,
#             time=construction_time,
#             investment_ratio=investment_ratio
#         )
#         time_cost = time_cost_component.calculate_cost()
        
#         # 4. Calculate Road User Cost
#         total_road_user_cost = 0
#         db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'IRC_Road_Costs.db')
#         db_path = os.path.abspath(db_path)
        
#         with sqlite3.connect(db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#             table_name = cursor.fetchone()[0]
            
#             for vehicle in vehicles:
#                 vehicle_type = vehicle.get('type', '')
#                 count = vehicle.get('count', 0)
                
#                 cursor.execute(f'''
#                     SELECT Grand_Cost FROM {table_name} WHERE 
#                         Vehicle_Type = ? AND Lane_Type = ? AND Roughness = ? AND RF = ?
#                 ''', (vehicle_type, lane_type, roughness, rf))
                
#                 result = cursor.fetchone()
#                 if result:
#                     grand_cost = result[0]
#                     ct = construction_time * reroute_distance
                    
#                     road_user_cost_component = RoadUserCost(
#                         vehicles_affected=count,
#                         vehicle_operation_cost=grand_cost,
#                         construction_time=ct
#                     )
#                     total_road_user_cost += road_user_cost_component.calculate_cost()
        
#         # 5. Calculate Additional Carbon Emission Cost
#         total_vehicles = sum(v.get('count', 0) for v in vehicles)
#         additional_carbon_component = AdditionalCarbonEmissionCost(
#             vehicles_affected=total_vehicles,
#             reroute_distance=reroute_distance,
#             co2_emission_per_km=co2_emission_per_km,
#             carbon_cost=carbon_cost
#         )
#         additional_carbon_cost = additional_carbon_component.calculate_cost()
        
#         # 6. Calculate Maintenance Costs
#         periodic_maintenance_component = PeriodicMaintenanceCost(
#             maintenance_cost_rate=maintenance_cost_rate,
#             construction_cost=total_construction_cost,
#             discount_rate=discount_rate,
#             period=maintenance_period,
#             design_life=design_life
#         )
#         periodic_maintenance_cost = periodic_maintenance_component.calculate_cost()
        
#         # 7. Calculate Maintenance Carbon Cost
#         maintenance_concrete_kg = 0
#         for material in materials:
#             if material.get('material', '').lower() == 'concrete':
#                 qty = material.get('quantity', 0)
#                 if material.get('unit', '').lower() == 'cum':
#                     qty = qty * 2549.25
#                 maintenance_concrete_kg += qty
        
#         maintenance_carbon_component = PeriodicMaintenanceCarbonCost(
#             material_quantity=maintenance_concrete_kg,
#             carbon_emission_factor=concrete_co2_emission_factor,
#             carbon_cost=carbon_cost,
#             discount_rate=discount_rate,
#             period=maintenance_period,
#             design_life=design_life
#         )
#         maintenance_carbon_cost = maintenance_carbon_component.calculate_cost()
        
#         # 8. Calculate Inspection Cost
#         inspection_component = RoutineInspectionCost(
#             inspection_cost_rate=inspection_rate,
#             construction_cost=total_construction_cost,
#             discount_rate=discount_rate,
#             design_life=design_life,
#             period=inspection_period
#         )
#         inspection_cost = inspection_component.calculate_cost()
        
#         # 9. Calculate Repair Cost
#         repair_component = RepairAndRehabilitationCost(
#             repair_cost_rate=repair_cost_rate,
#             construction_cost=total_construction_cost,
#             discount_rate=discount_rate,
#             period=repair_period,
#             design_life=design_life
#         )
#         repair_cost = repair_component.calculate_cost()
        
#         # 10. Calculate Demolition Cost
#         demolition_component = DemolitionCost(
#             demolition_rate=demolition_rate,
#             construction_cost=total_construction_cost,
#             discount_rate=discount_rate,
#             design_life=design_life
#         )
#         demolition_cost = demolition_component.calculate_cost()
        
#         # 11. Calculate Recycling Cost
#         if steel_unit.lower() == "kg":
#             steel_quantity_mt = steel_quantity / 1000
#         else:
#             steel_quantity_mt = steel_quantity
        
#         recycling_component = RecyclingCost(
#             scrap_value=scrap_value,
#             quantity=steel_quantity_mt,
#             scrap_rate=scrap_rate,
#             discount_rate=discount_rate,
#             design_life=design_life
#         )
#         recycling_cost = recycling_component.calculate_cost()
        
#         # 12. Calculate Reconstruction Cost (if analysis_period > design_life)
#         reconstruction_cost = 0
#         if analysis_period > design_life:
#             reconstruction_component = ReconstructionCost(
#                 demolition_cost=demolition_cost,
#                 reconstruction_cost=total_construction_cost,
#                 reconstruction_carbon_cost=carbon_emission_cost,
#                 reconstruction_time_cost=time_cost,
#                 reconstruction_roaduser_cost=total_road_user_cost,
#                 reconstruction_rerouting_carbon_cost=additional_carbon_cost,
#                 design_life=design_life,
#                 discount_rate=discount_rate
#             )
#             reconstruction_cost = reconstruction_component.calculate_cost()
        
#         # Calculate total LCCA
#         total_lcca = (
#             total_construction_cost +
#             carbon_emission_cost +
#             time_cost +
#             total_road_user_cost +
#             additional_carbon_cost +
#             periodic_maintenance_cost +
#             maintenance_carbon_cost +
#             inspection_cost +
#             repair_cost +
#             demolition_cost -
#             recycling_cost +
#             reconstruction_cost
#         )
        
#         # Prepare results
#         results = {
#             'total_lcca': total_lcca,
#             'cost_breakdown': {
#                 'initial_construction_cost': total_construction_cost,
#                 'initial_carbon_emission_cost': carbon_emission_cost,
#                 'time_cost': time_cost,
#                 'road_user_cost': total_road_user_cost,
#                 'additional_carbon_emission_cost': additional_carbon_cost,
#                 'periodic_maintenance_cost': periodic_maintenance_cost,
#                 'maintenance_carbon_cost': maintenance_carbon_cost,
#                 'routine_inspection_cost': inspection_cost,
#                 'repair_rehabilitation_cost': repair_cost,
#                 'demolition_cost': demolition_cost,
#                 'recycling_cost': recycling_cost,
#                 'reconstruction_cost': reconstruction_cost
#             },
#             'cost_categories': {
#                 'economic_costs': total_construction_cost + time_cost + total_road_user_cost + periodic_maintenance_cost + inspection_cost + repair_cost + demolition_cost - recycling_cost + reconstruction_cost,
#                 'environmental_costs': carbon_emission_cost + additional_carbon_cost + maintenance_carbon_cost,
#                 'social_costs': 0  # Add social costs if any
#             },
#             'status': 'success'
#         }
        
#         return jsonify(results)
    
#     except Exception as e:
#         return jsonify({
#             'error': str(e),
#             'status': 'error'
#         }), 400

#----- END OF SOLUTION -----#
from flask import Blueprint, request, jsonify
import os
import sqlite3
from typing import Dict, Any, List
import traceback
import json

from datetime import datetime

# Import your cost component classes
from core.cost_component import (
    InitialConstructionCost, InitialCarbonEmissionCost, TimeCost,
    RoadUserCost, AdditionalCarbonEmissionCost, PeriodicMaintenanceCost,
    PeriodicMaintenanceCarbonCost, RoutineInspectionCost, 
    RepairAndRehabilitationCost, DemolitionCost, RecyclingCost,
    ReconstructionCost, UserInputs
)

cost_calculations_bp = Blueprint('cost_calculations', __name__)

# Global storage for calculations (you can replace with database later)
calculation_storage = {}

class LCCCalculator:
    """Life Cycle Cost Calculator class to handle all calculations"""
    
    def __init__(self, inputs: UserInputs):
        self.inputs = inputs
        self.results = {}
        
    def calculate_initial_carbon_emission_cost(self) -> float:
        """Calculate initial carbon emission cost using the imported component"""
        try:
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
            
            total_concrete_emissions = 0
            total_steel_emissions = 0
            social_cost_of_carbon = 6.3936  # Default value
            
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # Get carbon cost parameters (Social Cost of Carbon)
                cursor.execute('''
                    SELECT result_data FROM calculation_results 
                    WHERE calculation_type = 'carbon_cost_parameters' 
                    ORDER BY created_at DESC LIMIT 1
                ''')
                params_result = cursor.fetchone()
                if params_result:
                    params_data = json.loads(params_result[0])
                    social_cost_of_carbon = float(params_data.get('socialCostOfCarbon', 6.3936))
                
                # Get carbon emission materials data and calculate totals
                cursor.execute('''
                    SELECT result_data FROM calculation_results 
                    WHERE calculation_type = 'carbon_emission_materials' 
                    ORDER BY created_at DESC LIMIT 1
                ''')
                materials_result = cursor.fetchone()
                
                if materials_result:
                    materials_data = json.loads(materials_result[0])
                    materials = materials_data.get('materials', [])
                    
                    for material in materials:
                        material_type = material.get('material_type', '').lower()
                        quantity = float(material.get('quantity', 0))
                        unit = material.get('unit', '').lower()
                        carbon_emission_factor = float(material.get('carbon_emission_factor', 0))
                        
                        # Calculate carbon emission for each material
                        if 'concrete' in material_type:
                            if unit == 'cum':
                                quantity = quantity * 2549.25  # density: kg/cum
                            total_concrete_emissions += quantity * carbon_emission_factor
                        elif 'steel' in material_type:
                            if unit.upper() == 'MT':
                                quantity = quantity * 1000  # 1 MT = 1000 kg
                            total_steel_emissions += quantity * carbon_emission_factor
            
            # Calculate total carbon emissions in kgCO2e
            total_emissions = total_concrete_emissions + total_steel_emissions
            
            # Calculate total cost using the InitialCarbonEmissionCost component
            # Based on your cost component signature: material_quantity, carbon_emission_factor, carbon_cost
            component = InitialCarbonEmissionCost(
                material_quantity=1,  # We'll multiply by 1 since we pre-calculated emissions
                carbon_emission_factor=total_emissions,  # Use total emissions as the factor
                carbon_cost=social_cost_of_carbon
            )
            
            total_cost = component.calculate_cost()
            
            # Store result in database
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM calculation_results 
                    WHERE calculation_type = 'initial_carbon_emission_cost'
                ''')
                
                result_data = {
                    'initial_carbon_emission_cost': total_cost,
                    'total_concrete_emissions': total_concrete_emissions,
                    'total_steel_emissions': total_steel_emissions,
                    'total_emissions': total_emissions,
                    'social_cost_of_carbon': social_cost_of_carbon,
                    'calculated_at': datetime.now().isoformat()
                }
                
                cursor.execute('''
                    INSERT INTO calculation_results (calculation_type, result_data, created_at)
                    VALUES (?, ?, ?)
                ''', ('initial_carbon_emission_cost', json.dumps(result_data), datetime.now().isoformat()))
                
                conn.commit()
            
            print(f"=== INITIAL CARBON EMISSION COST CALCULATION ===")
            print(f"Total Concrete Emissions: {total_concrete_emissions:.2f} kgCO₂e")
            print(f"Total Steel Emissions: {total_steel_emissions:.2f} kgCO₂e") 
            print(f"Total Emissions: {total_emissions:.2f} kgCO₂e")
            print(f"Social Cost of Carbon: ₹{social_cost_of_carbon}/kgCO₂e")
            print(f"Total Initial Carbon Emission Cost: ₹{total_cost:.2f}")
            
            return total_cost
            
        except Exception as e:
            print(f"Error calculating initial carbon emission cost: {e}")
            import traceback
            traceback.print_exc()
            return 0
    def calculate_additional_carbon_emission_cost(self) -> float:
        """Calculate additional carbon emission cost from traffic data"""
        try:
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
            
            vehicles_affected = 0
            reroute_distance = 0
            construction_time = 12  # Default
            social_cost_of_carbon = 6.3936
            
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # Get traffic data
                cursor.execute('''
                    SELECT result_data FROM calculation_results 
                    WHERE calculation_type = 'traffic_data' 
                    ORDER BY created_at DESC LIMIT 1
                ''')
                traffic_result = cursor.fetchone()
                
                if traffic_result:
                    traffic_data = json.loads(traffic_result[0])
                    road_user_inputs = traffic_data.get('data', {}).get('road_user_inputs', {})
                    financial_inputs = traffic_data.get('data', {}).get('financial_inputs', {})
                    
                    vehicles = road_user_inputs.get('Vehicles', [])
                    vehicles_affected = sum(v.get('Count', 0) for v in vehicles)
                    reroute_distance = financial_inputs.get('reroute_distance', 0)
                    construction_time = financial_inputs.get('construction_time', 12)
                
                # Get carbon cost parameters
                cursor.execute('''
                    SELECT result_data FROM calculation_results 
                    WHERE calculation_type = 'carbon_cost_parameters' 
                    ORDER BY created_at DESC LIMIT 1
                ''')
                params_result = cursor.fetchone()
                if params_result:
                    params_data = json.loads(params_result[0])
                    social_cost_of_carbon = float(params_data.get('socialCostOfCarbon', 6.3936))
            
            # Use the imported AdditionalCarbonEmissionCost component
            component = AdditionalCarbonEmissionCost(
                vehicles_affected=vehicles_affected,
                reroute_distance=reroute_distance,
                co2_emission_per_km=0.2,  # Default value from UserInputs
                carbon_cost=social_cost_of_carbon
            )
            
            total_cost = component.calculate_cost()
            
            # Store result in database
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM calculation_results 
                    WHERE calculation_type = 'additional_carbon_emission_cost'
                ''')
                
                result_data = {
                    'additional_carbon_emission_cost': total_cost,
                    'vehicles_affected': vehicles_affected,
                    'reroute_distance': reroute_distance,
                    'construction_time': construction_time,
                    'social_cost_of_carbon': social_cost_of_carbon,
                    'calculated_at': datetime.now().isoformat()
                }
                
                cursor.execute('''
                    INSERT INTO calculation_results (calculation_type, result_data, created_at)
                    VALUES (?, ?, ?)
                ''', ('additional_carbon_emission_cost', json.dumps(result_data), datetime.now().isoformat()))
                
                conn.commit()
            
            print(f"=== ADDITIONAL CARBON EMISSION COST CALCULATION ===")
            print(f"Vehicles Affected: {vehicles_affected}")
            print(f"Reroute Distance: {reroute_distance} km")
            print(f"Total Additional Carbon Emission Cost: ₹{total_cost:.2f}")
            
            return total_cost
            
        except Exception as e:
            print(f"Error calculating additional carbon emission cost: {e}")
            return 0
    def calculate_time_cost(self, construction_cost: float) -> float:
        """Calculate time cost"""
        component = TimeCost(
            construction_cost=construction_cost,
            interest_rate=self.inputs.interest_rate,
            time=self.inputs.construction_time,
            investment_ratio=self.inputs.investment_ratio
        )
        time_cost = component.calculate_cost()
        
        # Store time cost result in database
        try:
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
            db_path = os.path.abspath(db_path)
            
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # Delete existing time cost calculations
                cursor.execute('''
                    DELETE FROM calculation_results 
                    WHERE calculation_type = 'time_cost'
                ''')
                
                # Insert new calculation
                result_data = {
                    'time_cost': time_cost,
                    'construction_cost': construction_cost,
                    'interest_rate': self.inputs.interest_rate,
                    'construction_time': self.inputs.construction_time,
                    'investment_ratio': self.inputs.investment_ratio,
                    'calculated_at': datetime.now().isoformat()
                }
                
                cursor.execute('''
                    INSERT INTO calculation_results (calculation_type, result_data, created_at)
                    VALUES (?, ?, ?)
                ''', ('time_cost', json.dumps(result_data), datetime.now().isoformat()))
                
                conn.commit()
                
                print(f"=== TIME COST STORED IN DATABASE ===")
                print(f"Time Cost: ₹{time_cost:,.2f}")
                print(f"Construction Cost: ₹{construction_cost:,.2f}")
                print("===================================")
                
        except Exception as e:
            print(f"Error storing time cost in database: {e}")
        
        return time_cost
    
    @cost_calculations_bp.route('/api/calculate-initial-carbon-emission-cost', methods=['POST'])
    def calculate_initial_carbon_cost_new():
        """Calculate initial carbon emission cost using stored data"""
        try:
            inputs = UserInputs()
            calculator = LCCCalculator(inputs)
            cost = calculator.calculate_initial_carbon_emission_cost()
            
            return jsonify({
                'success': True,
                'initial_carbon_emission_cost': cost,
                'message': 'Initial carbon emission cost calculated successfully'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    def get_stored_time_cost():
        """Retrieve stored time cost from database"""
        try:
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
            db_path = os.path.abspath(db_path)
            
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT result_data FROM calculation_results 
                    WHERE calculation_type = 'time_cost' 
                    ORDER BY created_at DESC LIMIT 1
                ''')
                result = cursor.fetchone()
                
                if result:
                    result_data = json.loads(result[0])
                    return result_data['time_cost']
                else:
                    return 0
                    
        except Exception as e:
            print(f"Error retrieving time cost from database: {e}")
            return 0
    
    def calculate_road_user_cost(self) -> float:
        """Calculate road user cost using traffic data from database"""
        try:
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
            total_cost = 0
            
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # Get traffic data
                cursor.execute('''
                    SELECT result_data FROM calculation_results 
                    WHERE calculation_type = 'traffic_data' 
                    ORDER BY created_at DESC LIMIT 1
                ''')
                traffic_result = cursor.fetchone()
                
                if not traffic_result:
                    print("No traffic data found")
                    return 0
                    
                traffic_data = json.loads(traffic_result[0])
                road_user_inputs = traffic_data.get('data', {}).get('road_user_inputs', {})
                financial_inputs = traffic_data.get('data', {}).get('financial_inputs', {})
                
                vehicles = road_user_inputs.get('Vehicles', [])
                lane_type = road_user_inputs.get('Lane_Type', '2')
                roughness = road_user_inputs.get('Roughness', 'Good')
                rf = road_user_inputs.get('RF', 'Rolling')
                construction_time = financial_inputs.get('construction_time', 12)
                reroute_distance = financial_inputs.get('reroute_distance', 0)
                
                # FIX: Convert RF value to proper format
                print(f"Original RF value: {rf}")
                try:
                    rf_num = float(rf)
                    if rf_num <= 3:
                        rf = "Rolling"
                    else:
                        rf = "Hilly"
                    print(f"Converted RF from {rf_num} to: {rf}")
                except (ValueError, TypeError):
                    # If RF is already text, validate it
                    if str(rf).lower() not in ['rolling', 'hilly']:
                        rf = "Rolling"  # Default fallback
                        print(f"Invalid RF value, using default: {rf}")
                    else:
                        rf = str(rf).title()  # Capitalize first letter
                        print(f"Using RF: {rf}")
                
                print(f"Final parameters: Lane={lane_type}, Roughness={roughness}, RF={rf}")
                
                # Use the predefined IRC_ROAD_COSTS_DATA from traffic_analysis.py
                from api.routes.traffic_analysis import IRC_ROAD_COSTS_DATA
                
                for vehicle in vehicles:
                    vehicle_type = vehicle.get('Vehicle_Type', '')
                    count = vehicle.get('Count', 0)
                    
                    if count <= 0:
                        continue
                        
                    lookup_key = (vehicle_type, lane_type, roughness, rf)
                    print(f"Looking up key: {lookup_key}")
                    
                    if lookup_key in IRC_ROAD_COSTS_DATA:
                        grand_cost = IRC_ROAD_COSTS_DATA[lookup_key]
                        ct = construction_time * reroute_distance if reroute_distance > 0 else construction_time
                        
                        component = RoadUserCost(
                            vehicles_affected=count,
                            vehicle_operation_cost=grand_cost,
                            construction_time=ct
                        )
                        vehicle_cost = component.calculate_cost()
                        total_cost += vehicle_cost
                        
                        print(f"✓ Vehicle: {vehicle_type}, Count: {count}, Grand Cost: {grand_cost}, CT: {ct}, Cost: ₹{vehicle_cost:.2f}")
                    else:
                        print(f"✗ No cost data found for vehicle: {vehicle_type} with lookup key: {lookup_key}")
                        # Show available options
                        available = [k for k in IRC_ROAD_COSTS_DATA.keys() if k[0] == vehicle_type]
                        print(f"Available options for {vehicle_type}: {available[:3]}...")  # Show first 3
            
            # Store result in database
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM calculation_results 
                    WHERE calculation_type = 'road_user_cost_calculated'
                ''')
                
                result_data = {
                    'road_user_cost': total_cost,
                    'lane_type': lane_type,
                    'roughness': roughness,
                    'rf': rf,
                    'construction_time': construction_time,
                    'reroute_distance': reroute_distance,
                    'calculated_at': datetime.now().isoformat()
                }
                
                cursor.execute('''
                    INSERT INTO calculation_results (calculation_type, result_data, created_at)
                    VALUES (?, ?, ?)
                ''', ('road_user_cost_calculated', json.dumps(result_data), datetime.now().isoformat()))
                
                conn.commit()
            
            print(f"=== ROAD USER COST CALCULATION (LCC) ===")
            print(f"Total Road User Cost: ₹{total_cost:.2f}")
            print("=====================================")
            
            return total_cost
            
        except Exception as e:
            print(f"Error calculating road user cost: {e}")
            import traceback
            traceback.print_exc()
            return 0
    def calculate_additional_carbon_emission_cost(self) -> float:
        """Calculate additional carbon emission cost"""
        vehicles_affected = sum(v["Count"] for v in self.inputs.road_user_inputs["Vehicles"])
        
        component = AdditionalCarbonEmissionCost(
            vehicles_affected=vehicles_affected,
            reroute_distance=self.inputs.reroute_distance,
            co2_emission_per_km=self.inputs.co2_emission_per_km,
            carbon_cost=self.inputs.carbon_cost
        )
        return component.calculate_cost()
    
    def calculate_periodic_maintenance_cost(self, construction_cost: float) -> float:
        """Calculate periodic maintenance cost"""
        component = PeriodicMaintenanceCost(
            maintenance_cost_rate=self.inputs.maintenance_cost_rate,
            construction_cost=construction_cost,
            discount_rate=self.inputs.discount_rate,
            period=self.inputs.maintenance_period,
            design_life=self.inputs.design_life
        )
        return component.calculate_cost()
    
    def calculate_periodic_maintenance_carbon_cost(self) -> float:
        """Calculate periodic maintenance carbon cost"""
        maintenance_concrete_kg = 0
        
        for item in self.inputs.user_materials:
            if item["material"].lower() == "concrete":
                qty = item["quantity"]
                unit = item["unit"].lower()
                if unit == "cum":
                    qty = qty * 2549.25  # density: kg/cum
                maintenance_concrete_kg += qty
        
        component = PeriodicMaintenanceCarbonCost(
            material_quantity=maintenance_concrete_kg,
            carbon_emission_factor=self.inputs.concrete_co2_emission_factor,
            carbon_cost=self.inputs.carbon_cost,
            discount_rate=self.inputs.discount_rate,
            period=self.inputs.maintenance_period,
            design_life=self.inputs.design_life
        )
        return component.calculate_cost()
    
    def calculate_routine_inspection_cost(self, construction_cost: float) -> float:
        """Calculate routine inspection cost"""
        component = RoutineInspectionCost(
            inspection_cost_rate=self.inputs.inspection_rate,
            construction_cost=construction_cost,
            discount_rate=self.inputs.discount_rate,
            design_life=self.inputs.design_life,
            period=self.inputs.inspection_period
        )
        return component.calculate_cost()
    
    def calculate_repair_rehabilitation_cost(self, construction_cost: float) -> float:
        """Calculate repair and rehabilitation cost"""
        component = RepairAndRehabilitationCost(
            repair_cost_rate=self.inputs.repair_cost_rate,
            construction_cost=construction_cost,
            discount_rate=self.inputs.discount_rate,
            period=self.inputs.repair_period,
            design_life=self.inputs.design_life
        )
        return component.calculate_cost()
    
    def calculate_demolition_cost(self, construction_cost: float) -> float:
        """Calculate demolition cost"""
        component = DemolitionCost(
            demolition_rate=self.inputs.demolition_rate,
            construction_cost=construction_cost,
            discount_rate=self.inputs.discount_rate,
            design_life=self.inputs.design_life
        )
        return component.calculate_cost()
    
    def calculate_recycling_cost(self) -> float:
        """Calculate recycling cost"""
        user_input_steel_quantity = self.inputs.user_input_steel_quantity
        user_input_steel_unit = self.inputs.user_input_steel_unit
        
        if user_input_steel_unit.lower() == "kg":
            user_input_steel_quantity_mt = user_input_steel_quantity / 1000
        else:
            user_input_steel_quantity_mt = user_input_steel_quantity
        
        component = RecyclingCost(
            scrap_value=self.inputs.scrap_value,
            quantity=user_input_steel_quantity_mt,
            scrap_rate=self.inputs.scrap_rate,
            discount_rate=self.inputs.discount_rate,
            design_life=self.inputs.design_life
        )
        return component.calculate_cost()
    
    def calculate_reconstruction_cost(self, demolition_cost: float, construction_cost: float, 
                                   carbon_cost: float, time_cost: float, road_user_cost: float, 
                                   additional_carbon_cost: float) -> float:
        """Calculate reconstruction cost"""
        if self.inputs.analysis_period <= self.inputs.design_life:
            return 0
        
        component = ReconstructionCost(
            demolition_cost=demolition_cost,
            reconstruction_cost=construction_cost,
            reconstruction_carbon_cost=carbon_cost,
            reconstruction_time_cost=time_cost,
            reconstruction_roaduser_cost=road_user_cost,
            reconstruction_rerouting_carbon_cost=additional_carbon_cost,
            design_life=self.inputs.design_life,
            discount_rate=self.inputs.discount_rate
        )
        return component.calculate_cost()
    
    def calculate_all_costs(self) -> Dict[str, float]:
        """Calculate all costs and return as dictionary"""
        # Calculate initial construction cost first as it's needed for other calculations
        initial_construction_cost = self.calculate_initial_construction_cost()
        initial_carbon_cost = self.calculate_initial_carbon_emission_cost()
        time_cost = self.calculate_time_cost(initial_construction_cost)
        road_user_cost = self.calculate_road_user_cost()
        additional_carbon_cost = self.calculate_additional_carbon_emission_cost()
        periodic_maintenance_cost = self.calculate_periodic_maintenance_cost(initial_construction_cost)
        periodic_maintenance_carbon_cost = self.calculate_periodic_maintenance_carbon_cost()
        routine_inspection_cost = self.calculate_routine_inspection_cost(initial_construction_cost)
        repair_rehabilitation_cost = self.calculate_repair_rehabilitation_cost(initial_construction_cost)
        demolition_cost = self.calculate_demolition_cost(initial_construction_cost)
        recycling_cost = self.calculate_recycling_cost()
        reconstruction_cost = self.calculate_reconstruction_cost(
            demolition_cost, initial_construction_cost, initial_carbon_cost, 
            time_cost, road_user_cost, additional_carbon_cost
        )
        
        results = {
            "initial_construction_cost": initial_construction_cost,
            "initial_carbon_emission_cost": initial_carbon_cost,
            "time_cost": time_cost,
            "road_user_cost": road_user_cost,
            "additional_carbon_emission_cost": additional_carbon_cost,
            "periodic_maintenance_cost": periodic_maintenance_cost,
            "periodic_maintenance_carbon_cost": periodic_maintenance_carbon_cost,
            "routine_inspection_cost": routine_inspection_cost,
            "repair_rehabilitation_cost": repair_rehabilitation_cost,
            "demolition_cost": demolition_cost,
            "recycling_cost": recycling_cost,
            "reconstruction_cost": reconstruction_cost,
            "total_lcc": (
                initial_construction_cost + initial_carbon_cost + time_cost + 
                road_user_cost + additional_carbon_cost + periodic_maintenance_cost + 
                periodic_maintenance_carbon_cost + routine_inspection_cost + 
                repair_rehabilitation_cost + demolition_cost + recycling_cost + 
                reconstruction_cost
            )
        }
        
        self.results = results
        return results

@cost_calculations_bp.route('/api/calculate-additional-carbon-cost', methods=['POST'])
def calculate_additional_carbon_cost():
    """Calculate additional carbon emission cost endpoint"""
    try:
        inputs = UserInputs()
        calculator = LCCCalculator(inputs)
        cost = calculator.calculate_additional_carbon_emission_cost()
        
        return jsonify({
            'success': True,
            'additional_carbon_emission_cost': cost,
            'message': 'Additional carbon emission cost calculated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
@cost_calculations_bp.route('/api/get-initial-construction-cost', methods=['GET'])
def get_initial_construction_cost():
    """Get stored initial construction cost from database"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
        db_path = os.path.abspath(db_path)
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT result_data FROM calculation_results 
                WHERE calculation_type = 'initial_construction_cost_auto' 
                ORDER BY created_at DESC LIMIT 1
            ''')
            result = cursor.fetchone()
            
            if result:
                result_data = json.loads(result[0])
                cost = result_data.get('total_initial_cost', 0)
                print(f"Retrieved initial construction cost: ₹{cost}")
                return jsonify({
                    'success': True,
                    'cost': cost
                })
            else:
                print("No initial construction cost found in database")
                return jsonify({'success': False, 'cost': 0})
                    
    except Exception as e:
        print(f"Error getting initial construction cost: {e}")
        return jsonify({'success': False, 'error': str(e), 'cost': 0}), 500
    
@cost_calculations_bp.route('/api/calculate-road-user-cost-stored', methods=['POST'])
def calculate_road_user_cost_stored():
    """Calculate road user cost using stored traffic data"""
    try:
        inputs = UserInputs()
        calculator = LCCCalculator(inputs)
        cost = calculator.calculate_road_user_cost()
        
        return jsonify({
            'success': True,
            'road_user_cost': cost,
            'message': 'Road user cost calculated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
# Route functions
@cost_calculations_bp.route('/api/calculate-all-costs', methods=['POST'])
def calculate_all_costs():
    """Calculate all LCC costs at once"""
    try:
        data = request.json
        
        # Create UserInputs object from the received data
        inputs = UserInputs()
        
        # Update inputs with received data
        if 'user_materials' in data:
            inputs.user_materials = data['user_materials']
        if 'road_user_inputs' in data:
            inputs.road_user_inputs = data['road_user_inputs']
        if 'financial_inputs' in data:
            financial = data['financial_inputs']
            inputs.analysis_period = financial.get('analysis_period', inputs.analysis_period)
            inputs.design_life = financial.get('design_life', inputs.design_life)
            inputs.discount_rate = financial.get('discount_rate', inputs.discount_rate)
            inputs.construction_time = financial.get('construction_time', inputs.construction_time)
            inputs.interest_rate = financial.get('interest_rate', inputs.interest_rate)
            inputs.investment_ratio = financial.get('investment_ratio', inputs.investment_ratio)
        if 'maintenance_inputs' in data:
            maintenance = data['maintenance_inputs']
            inputs.maintenance_cost_rate = maintenance.get('maintenance_cost_rate', inputs.maintenance_cost_rate)
            inputs.maintenance_period = maintenance.get('maintenance_period', inputs.maintenance_period)
            inputs.inspection_rate = maintenance.get('inspection_rate', inputs.inspection_rate)
            inputs.repair_cost_rate = maintenance.get('repair_cost_rate', inputs.repair_cost_rate)
            inputs.repair_period = maintenance.get('repair_period', inputs.repair_period)
        if 'demolition_recycling_inputs' in data:
            demolition = data['demolition_recycling_inputs']
            inputs.demolition_rate = demolition.get('demolition_rate', inputs.demolition_rate)
            inputs.scrap_value = demolition.get('scrap_value', inputs.scrap_value)
            inputs.scrap_rate = demolition.get('scrap_rate', inputs.scrap_rate)
            inputs.user_input_steel_quantity = demolition.get('user_input_steel_quantity', inputs.user_input_steel_quantity)
            inputs.user_input_steel_unit = demolition.get('user_input_steel_unit', inputs.user_input_steel_unit)
        
        # Create calculator and calculate all costs
        calculator = LCCCalculator(inputs)
        results = calculator.calculate_all_costs()
        
        # Store results for later retrieval
        project_id = data.get('project_id', 'default')
        calculation_storage[project_id] = results
        
        return jsonify({
            'success': True,
            'results': results,
            'message': 'All costs calculated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@cost_calculations_bp.route('/api/calculate-initial-construction-cost', methods=['POST'])
def calculate_initial_construction_cost():
    """Calculate only initial construction cost"""
    try:
        data = request.json
        inputs = UserInputs()
        if 'user_materials' in data:
            inputs.user_materials = data['user_materials']
        
        calculator = LCCCalculator(inputs)
        cost = calculator.calculate_initial_construction_cost()
        
        return jsonify({
            'success': True,
            'initial_construction_cost': cost,
            'message': 'Initial construction cost calculated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
@cost_calculations_bp.route('/api/get-stored-time-cost', methods=['GET'])
def get_stored_time_cost():
    """Get stored time cost from database"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
        db_path = os.path.abspath(db_path)
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT result_data FROM calculation_results 
                WHERE calculation_type = 'time_cost' 
                ORDER BY created_at DESC LIMIT 1
            ''')
            result = cursor.fetchone()
            
            if result:
                result_data = json.loads(result[0])
                time_cost = result_data.get('time_cost', 0)
                print(f"Retrieved time cost: ₹{time_cost}")
                return jsonify({
                    'success': True,
                    'time_cost': time_cost
                })
            else:
                print("No time cost found in database")
                return jsonify({'success': False, 'time_cost': 0})
                
    except Exception as e:
        print(f"Error getting time cost: {e}")
        return jsonify({'success': False, 'error': str(e), 'time_cost': 0}), 500
@cost_calculations_bp.route('/api/calculate-carbon-emission-cost', methods=['POST'])
def calculate_carbon_emission_cost():
    """Calculate initial carbon emission cost"""
    try:
        data = request.json
        inputs = UserInputs()
        if 'user_materials' in data:
            inputs.user_materials = data['user_materials']
        
        calculator = LCCCalculator(inputs)
        cost = calculator.calculate_initial_carbon_emission_cost()
        
        return jsonify({
            'success': True,
            'initial_carbon_emission_cost': cost,
            'message': 'Carbon emission cost calculated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cost_calculations_bp.route('/api/get-stored-road-user-cost', methods=['GET'])
def get_stored_road_user_cost():
    """Get stored road user cost from database"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
        db_path = os.path.abspath(db_path)
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT result_data FROM calculation_results 
                WHERE calculation_type = 'road_user_cost_calculated' 
                ORDER BY created_at DESC LIMIT 1
            ''')
            result = cursor.fetchone()
            
            if result:
                result_data = json.loads(result[0])
                cost = result_data.get('road_user_cost', 0)
                print(f"Retrieved road user cost: ₹{cost}")
                return jsonify({
                    'success': True,
                    'road_user_cost': cost
                })
            else:
                print("No road user cost found in database")
                return jsonify({'success': False, 'road_user_cost': 0})
                
    except Exception as e:
        print(f"Error getting road user cost: {e}")
        return jsonify({'success': False, 'error': str(e), 'road_user_cost': 0}), 500

@cost_calculations_bp.route('/api/calculate-time-cost', methods=['POST'])
def calculate_time_cost():
    """Calculate time cost"""
    try:
        data = request.json
        inputs = UserInputs()
        
        # Update inputs with received data
        if 'user_materials' in data:
            inputs.user_materials = data['user_materials']
        if 'financial_inputs' in data:
            financial = data['financial_inputs']
            inputs.construction_time = financial.get('construction_time', inputs.construction_time)
            inputs.interest_rate = financial.get('interest_rate', inputs.interest_rate)
            inputs.investment_ratio = financial.get('investment_ratio', inputs.investment_ratio)
        
        calculator = LCCCalculator(inputs)
        construction_cost = calculator.calculate_initial_construction_cost()
        time_cost = calculator.calculate_time_cost(construction_cost)
        
        return jsonify({
            'success': True,
            'time_cost': time_cost,
            'construction_cost': construction_cost,
            'message': 'Time cost calculated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@cost_calculations_bp.route('/api/calculate-road-user-cost', methods=['POST'])
def calculate_road_user_cost():
    """Calculate road user cost"""
    try:
        data = request.json
        inputs = UserInputs()
        
        if 'road_user_inputs' in data:
            inputs.road_user_inputs = data['road_user_inputs']
        if 'financial_inputs' in data:
            financial = data['financial_inputs']
            inputs.construction_time = financial.get('construction_time', inputs.construction_time)
            inputs.reroute_distance = financial.get('reroute_distance', inputs.reroute_distance)
        
        calculator = LCCCalculator(inputs)
        cost = calculator.calculate_road_user_cost()
        
        return jsonify({
            'success': True,
            'road_user_cost': cost,
            'message': 'Road user cost calculated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@cost_calculations_bp.route('/api/calculate-maintenance-costs', methods=['POST'])
def calculate_maintenance_costs():
    """Calculate all maintenance related costs"""
    try:
        data = request.json
        inputs = UserInputs()
        
        # Update inputs with received data
        if 'user_materials' in data:
            inputs.user_materials = data['user_materials']
        if 'financial_inputs' in data:
            financial = data['financial_inputs']
            inputs.discount_rate = financial.get('discount_rate', inputs.discount_rate)
            inputs.design_life = financial.get('design_life', inputs.design_life)
        if 'maintenance_inputs' in data:
            maintenance = data['maintenance_inputs']
            inputs.maintenance_cost_rate = maintenance.get('maintenance_cost_rate', inputs.maintenance_cost_rate)
            inputs.maintenance_period = maintenance.get('maintenance_period', inputs.maintenance_period)
            inputs.inspection_rate = maintenance.get('inspection_rate', inputs.inspection_rate)
            inputs.repair_cost_rate = maintenance.get('repair_cost_rate', inputs.repair_cost_rate)
            inputs.repair_period = maintenance.get('repair_period', inputs.repair_period)
        
        calculator = LCCCalculator(inputs)
        construction_cost = calculator.calculate_initial_construction_cost()
        
        results = {
            'periodic_maintenance_cost': calculator.calculate_periodic_maintenance_cost(construction_cost),
            'periodic_maintenance_carbon_cost': calculator.calculate_periodic_maintenance_carbon_cost(),
            'routine_inspection_cost': calculator.calculate_routine_inspection_cost(construction_cost),
            'repair_rehabilitation_cost': calculator.calculate_repair_rehabilitation_cost(construction_cost),
            'construction_cost': construction_cost
        }
        
        return jsonify({
            'success': True,
            'results': results,
            'message': 'Maintenance costs calculated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@cost_calculations_bp.route('/api/calculate-demolition-recycling-costs', methods=['POST'])
def calculate_demolition_recycling_costs():
    """Calculate demolition and recycling costs"""
    try:
        data = request.json
        inputs = UserInputs()
        
        # Update inputs with received data
        if 'user_materials' in data:
            inputs.user_materials = data['user_materials']
        if 'financial_inputs' in data:
            financial = data['financial_inputs']
            inputs.discount_rate = financial.get('discount_rate', inputs.discount_rate)
            inputs.design_life = financial.get('design_life', inputs.design_life)
        if 'demolition_recycling_inputs' in data:
            demolition = data['demolition_recycling_inputs']
            inputs.demolition_rate = demolition.get('demolition_rate', inputs.demolition_rate)
            inputs.scrap_value = demolition.get('scrap_value', inputs.scrap_value)
            inputs.scrap_rate = demolition.get('scrap_rate', inputs.scrap_rate)
            inputs.user_input_steel_quantity = demolition.get('user_input_steel_quantity', inputs.user_input_steel_quantity)
            inputs.user_input_steel_unit = demolition.get('user_input_steel_unit', inputs.user_input_steel_unit)
        
        calculator = LCCCalculator(inputs)
        construction_cost = calculator.calculate_initial_construction_cost()
        
        results = {
            'demolition_cost': calculator.calculate_demolition_cost(construction_cost),
            'recycling_cost': calculator.calculate_recycling_cost(),
            'construction_cost': construction_cost
        }
        
        return jsonify({
            'success': True,
            'results': results,
            'message': 'Demolition and recycling costs calculated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@cost_calculations_bp.route('/api/get-calculation-results/<project_id>', methods=['GET'])
def get_calculation_results(project_id):
    """Get stored calculation results"""
    try:
        if project_id in calculation_storage:
            return jsonify({
                'success': True,
                'results': calculation_storage[project_id],
                'message': 'Results retrieved successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No calculation results found for this project'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@cost_calculations_bp.route('/api/get-all-stored-results', methods=['GET'])
def get_all_stored_results():
    """Get all stored calculation results"""
    try:
        return jsonify({
            'success': True,
            'results': calculation_storage,
            'message': 'All results retrieved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cost_calculations_bp.route('/api/calculate-initial-carbon-emission-cost', methods=['POST'])
def calculate_initial_carbon_emission_cost_endpoint():
    """Calculate initial carbon emission cost endpoint"""
    try:
        inputs = UserInputs()
        calculator = LCCCalculator(inputs)
        cost = calculator.calculate_initial_carbon_emission_cost()
        
        return jsonify({
            'success': True,
            'initial_carbon_emission_cost': cost,
            'message': 'Initial carbon emission cost calculated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cost_calculations_bp.route('/api/calculate-additional-carbon-emission-cost', methods=['POST'])
def calculate_additional_carbon_emission_cost_endpoint():
    """Calculate additional carbon emission cost endpoint"""
    try:
        inputs = UserInputs()
        calculator = LCCCalculator(inputs)
        cost = calculator.calculate_additional_carbon_emission_cost()
        
        return jsonify({
            'success': True,
            'additional_carbon_emission_cost': cost,
            'message': 'Additional carbon emission cost calculated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cost_calculations_bp.route('/api/calculate-road-user-cost-new', methods=['POST'])
def calculate_road_user_cost_new():
    """Calculate road user cost using stored traffic data"""
    try:
        inputs = UserInputs()
        calculator = LCCCalculator(inputs)
        cost = calculator.calculate_road_user_cost()
        
        return jsonify({
            'success': True,
            'road_user_cost': cost,
            'message': 'Road user cost calculated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
@cost_calculations_bp.route('/api/clear-calculation-storage', methods=['DELETE'])
def clear_calculation_storage():
    """Clear all stored calculation results"""
    try:
        calculation_storage.clear()
        return jsonify({
            'success': True,
            'message': 'All calculation results cleared successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
@cost_calculations_bp.route('/api/calculate-and-save-initial-cost', methods=['POST'])
def calculate_and_save_initial_cost():
    """Calculate initial construction cost from ALL saved structure forms and store in database"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'databases', 'project_data.db')
        db_path = os.path.abspath(db_path)
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            structure_forms = ['Foundation', 'Sub-Structure', 'Super-Structure', 'Miscellaneous']
            
            all_materials = []
            forms_processed = []
            
            print(f"=== CALCULATING INITIAL CONSTRUCTION COST FROM ALL FORMS ===")
            
            for form_name in structure_forms:
                cursor.execute('''
                    SELECT materials FROM form_data 
                    WHERE form_name = ? 
                    ORDER BY saved_at DESC LIMIT 1
                ''', (form_name,))
                result = cursor.fetchone()
                
                if result and result[0]:
                    materials = json.loads(result[0])
                    if materials:
                        all_materials.extend(materials)
                        forms_processed.append(form_name)
                        print(f"✓ Loaded {len(materials)} materials from {form_name}")
            
            if not all_materials:
                print("✗ No materials found in any structure forms")
                return jsonify({
                    'success': False,
                    'error': 'No materials found in structure forms'
                })
            
            total_cost = 0
            cost_breakdown = []
            
            print(f"\nProcessing {len(all_materials)} total materials...")
            
            for material in all_materials:
                try:
                    quantity = float(material.get('quantity', 0))
                    rate = float(material.get('rate', 0))
                    material_cost = quantity * rate
                    total_cost += material_cost
                    
                    cost_item = {
                        'component': material.get('component', ''),
                        'material': material.get('materialType', ''),
                        'grade': material.get('subMaterialType', ''),
                        'quantity': quantity,
                        'unit': material.get('unit', ''),
                        'rate': rate,
                        'total_cost': material_cost
                    }
                    cost_breakdown.append(cost_item)
                    
                    print(f"  - {material.get('materialType', 'Unknown')}: {quantity} {material.get('unit', '')} @ ₹{rate} = ₹{material_cost:.2f}")
                    
                except (ValueError, TypeError) as e:
                    print(f"  ✗ Error processing material: {str(e)}")
                    continue
            
            print(f"\n=== CALCULATION COMPLETE ===")
            print(f"Forms Processed: {', '.join(forms_processed)}")
            print(f"Total Materials: {len(all_materials)}")
            print(f"Total Initial Construction Cost: ₹{total_cost:,.2f}")
            print("============================\n")
            
            cursor.execute('''
                DELETE FROM calculation_results 
                WHERE calculation_type = 'initial_construction_cost_auto'
            ''')
            
            result_data = {
                'total_initial_cost': total_cost,
                'cost_breakdown': cost_breakdown,
                'forms_processed': forms_processed,
                'materials_count': len(all_materials),
                'calculated_at': datetime.now().isoformat()
            }
            
            cursor.execute('''
                INSERT INTO calculation_results (calculation_type, result_data, created_at)
                VALUES (?, ?, ?)
            ''', ('initial_construction_cost_auto', json.dumps(result_data), datetime.now().isoformat()))
            
            conn.commit()
            
            print("✓ Calculation saved to database")
            
            return jsonify({
                'success': True,
                'total_initial_cost': total_cost,
                'cost_breakdown': cost_breakdown,
                'forms_processed': forms_processed,
                'materials_count': len(all_materials),
                'message': 'Initial construction cost calculated and saved successfully'
            })
            
    except Exception as e:
        print(f"✗ Error calculating initial cost: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500