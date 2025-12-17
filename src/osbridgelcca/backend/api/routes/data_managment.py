from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime
from typing import Dict, Any, List
import sys

# Add the path to access the cost components
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))

from cost_component import (
    InitialConstructionCost, InitialCarbonEmissionCost, TimeCost,
    RoadUserCost, AdditionalCarbonEmissionCost, PeriodicMaintenanceCost,
    PeriodicMaintenanceCarbonCost, RoutineInspectionCost, RepairAndRehabilitationCost,
    DemolitionCost, RecyclingCost, ReconstructionCost
)

data_management_bp = Blueprint('data_management', __name__)

# In-memory storage for calculation results (you can replace with database)
calculation_results = []
project_data = {}

class LCCADataManager:
    """Manages LCCA calculation results in array/list format"""
    
    def __init__(self):
        self.results_array = []
        self.current_project = {}
    
    def add_calculation_result(self, calculation_type: str, result_data: Dict[str, Any]):
        """Add a calculation result to the results array"""
        result_entry = {
            'id': len(self.results_array) + 1,
            'calculation_type': calculation_type,
            'timestamp': datetime.now().isoformat(),
            'data': result_data
        }
        self.results_array.append(result_entry)
        return result_entry
    
    def get_all_results(self) -> List[Dict[str, Any]]:
        """Get all calculation results as array"""
        return self.results_array
    
    def get_results_by_type(self, calculation_type: str) -> List[Dict[str, Any]]:
        """Get results filtered by calculation type"""
        return [result for result in self.results_array if result['calculation_type'] == calculation_type]
    
    def get_latest_result(self, calculation_type: str = None) -> Dict[str, Any]:
        """Get the latest calculation result"""
        if calculation_type:
            filtered_results = self.get_results_by_type(calculation_type)
            return filtered_results[-1] if filtered_results else None
        return self.results_array[-1] if self.results_array else None
    
    def clear_results(self):
        """Clear all results"""
        self.results_array = []
    
    def get_complete_lcca_summary(self) -> Dict[str, Any]:
        """Get complete LCCA summary with all cost components"""
        summary = {
            'total_calculations': len(self.results_array),
            'cost_components': {},
            'complete_results_array': self.results_array
        }
        
        # Group results by type
        for result in self.results_array:
            calc_type = result['calculation_type']
            if calc_type not in summary['cost_components']:
                summary['cost_components'][calc_type] = []
            summary['cost_components'][calc_type].append(result)
        
        return summary

# Global data manager instance
data_manager = LCCADataManager()

@data_management_bp.route('/api/save-calculation-result', methods=['POST'])
def save_calculation_result():
    """Save any calculation result to the results array"""
    try:
        data = request.json
        calculation_type = data.get('calculation_type')
        result_data = data.get('result_data')
        
        if not calculation_type or not result_data:
            return jsonify({
                'error': 'calculation_type and result_data are required',
                'status': 'error'
            }), 400
        
        # Add to results array
        result_entry = data_manager.add_calculation_result(calculation_type, result_data)
        
        return jsonify({
            'message': 'Calculation result saved successfully',
            'result_entry': result_entry,
            'total_results': len(data_manager.results_array),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@data_management_bp.route('/api/get-all-calculation-results', methods=['GET'])
def get_all_calculation_results():
    """Get all calculation results as array"""
    try:
        results_array = data_manager.get_all_results()
        
        return jsonify({
            'results_array': results_array,
            'total_count': len(results_array),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@data_management_bp.route('/api/get-calculation-results/<calculation_type>', methods=['GET'])
def get_calculation_results_by_type(calculation_type):
    """Get calculation results filtered by type"""
    try:
        results = data_manager.get_results_by_type(calculation_type)
        
        return jsonify({
            'calculation_type': calculation_type,
            'results': results,
            'count': len(results),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@data_management_bp.route('/api/get-latest-calculation-result', methods=['GET'])
def get_latest_calculation_result():
    """Get the latest calculation result"""
    try:
        calculation_type = request.args.get('type')
        latest_result = data_manager.get_latest_result(calculation_type)
        
        if not latest_result:
            return jsonify({
                'message': 'No results found',
                'result': None,
                'status': 'success'
            })
        
        return jsonify({
            'latest_result': latest_result,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@data_management_bp.route('/api/get-complete-lcca-summary', methods=['GET'])
def get_complete_lcca_summary():
    """Get complete LCCA summary with all components"""
    try:
        summary = data_manager.get_complete_lcca_summary()
        
        return jsonify({
            'lcca_summary': summary,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@data_management_bp.route('/api/clear-calculation-results', methods=['DELETE'])
def clear_calculation_results():
    """Clear all calculation results"""
    try:
        data_manager.clear_results()
        
        return jsonify({
            'message': 'All calculation results cleared',
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

# Individual cost component getter methods
@data_management_bp.route('/api/get-initial-construction-cost', methods=['GET'])
def get_initial_construction_cost():
    """Get initial construction cost from results array"""
    try:
        results = data_manager.get_results_by_type('initial_construction_cost')
        latest = results[-1] if results else None
        
        return jsonify({
            'initial_construction_cost': latest['data'] if latest else None,
            'all_calculations': results,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@data_management_bp.route('/api/get-carbon-emission-cost', methods=['GET'])
def get_carbon_emission_cost():
    """Get carbon emission cost from results array"""
    try:
        results = data_manager.get_results_by_type('carbon_emission_cost')
        latest = results[-1] if results else None
        
        return jsonify({
            'carbon_emission_cost': latest['data'] if latest else None,
            'all_calculations': results,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@data_management_bp.route('/api/get-time-cost', methods=['GET'])
def get_time_cost():
    """Get time cost from results array"""
    try:
        results = data_manager.get_results_by_type('time_cost')
        latest = results[-1] if results else None
        
        return jsonify({
            'time_cost': latest['data'] if latest else None,
            'all_calculations': results,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@data_management_bp.route('/api/get-road-user-cost', methods=['GET'])
def get_road_user_cost():
    """Get road user cost from results array"""
    try:
        results = data_manager.get_results_by_type('road_user_cost')
        latest = results[-1] if results else None
        
        return jsonify({
            'road_user_cost': latest['data'] if latest else None,
            'all_calculations': results,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@data_management_bp.route('/api/get-maintenance-costs', methods=['GET'])
def get_maintenance_costs():
    """Get maintenance costs from results array"""
    try:
        results = data_manager.get_results_by_type('maintenance_costs')
        latest = results[-1] if results else None
        
        return jsonify({
            'maintenance_costs': latest['data'] if latest else None,
            'all_calculations': results,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@data_management_bp.route('/api/get-end-of-life-costs', methods=['GET'])
def get_end_of_life_costs():
    """Get end of life costs from results array"""
    try:
        results = data_manager.get_results_by_type('end_of_life_costs')
        latest = results[-1] if results else None
        
        return jsonify({
            'end_of_life_costs': latest['data'] if latest else None,
            'all_calculations': results,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@data_management_bp.route('/api/calculate-and-store-complete-lcca', methods=['POST'])
def calculate_and_store_complete_lcca():
    """Calculate complete LCCA and store all results in arrays"""
    try:
        data = request.json
        
        # This would call your existing complete LCCA calculation
        # and then store each component in the results array
        
        # Import the complete calculation logic here
        # ... (your existing calculation code)
        
        # For now, I'll create a placeholder structure
        complete_results = {
            'initial_construction_cost': 0,
            'carbon_emission_cost': 0,
            'time_cost': 0,
            'road_user_cost': 0,
            'additional_carbon_cost': 0,
            'maintenance_costs': 0,
            'end_of_life_costs': 0,
            'total_lcca': 0
        }
        
        # Store each component in the results array
        for cost_type, cost_value in complete_results.items():
            data_manager.add_calculation_result(cost_type, {
                'cost': cost_value,
                'input_parameters': data,
                'calculation_details': {}
            })
        
        # Get complete summary
        summary = data_manager.get_complete_lcca_summary()
        
        return jsonify({
            'message': 'Complete LCCA calculated and stored',
            'results_summary': summary,
            'total_lcca': complete_results['total_lcca'],
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400
