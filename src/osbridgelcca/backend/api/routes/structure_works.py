

# from flask import Blueprint, request, jsonify
# import json
# import os
# from datetime import datetime
# from sqlalchemy.exc import SQLAlchemyError

# # Import database models and session
# from ..models.database import (
#     get_db_session, get_or_create_project, 
#     FormData, CarbonEmissionData, CalculationResults
# )

# structure_works_bp = Blueprint('structure_works', __name__)

# @structure_works_bp.route('/api/save-form-data/<form_name>', methods=['POST'])
# def save_form_data(form_name):
#     """Save form data to database for a specific form"""
#     session = None
#     try:
#         data = request.json
#         session = get_db_session()
        
#         # Get or create project (defaults to "default" project)
#         project_name = data.get('project_name', 'default')
#         project = get_or_create_project(session, project_name)
        
#         # Check if form data already exists for this project and form
#         existing_form = session.query(FormData).filter_by(
#             project_id=project.id,
#             form_name=form_name
#         ).first()
        
#         if existing_form:
#             # Update existing form data
#             existing_form.materials = data.get('materials', [])
#             existing_form.saved_at = datetime.utcnow()
#         else:
#             # Create new form data entry
#             form_data_entry = FormData(
#                 project_id=project.id,
#                 form_name=form_name,
#                 materials=data.get('materials', []),
#                 timestamp=datetime.utcnow(),
#                 saved_at=datetime.utcnow()
#             )
#             session.add(form_data_entry)
        
#         session.commit()
        
#         print(f"=== FORM DATA SAVED TO DATABASE ===")
#         print(f"Project: {project.name} (ID: {project.id})")
#         print(f"Form: {form_name}")
#         print(f"Materials count: {len(data.get('materials', []))}")
#         print(f"Timestamp: {datetime.utcnow().isoformat()}")
#         print("===================================")
        
#         return jsonify({
#             'success': True,
#             'message': f'Form data saved successfully for {form_name}',
#             'project_id': project.id,
#             'project_name': project.name,
#             'form_name': form_name,
#             'materials_count': len(data.get('materials', []))
#         })
        
#     except SQLAlchemyError as e:
#         if session:
#             session.rollback()
#         print(f"Database error saving form data: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': f'Database error: {str(e)}'
#         }), 500
#     except Exception as e:
#         if session:
#             session.rollback()
#         print(f"Error saving form data: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#     finally:
#         if session:
#             session.close()

# @structure_works_bp.route('/api/get-carbon-materials', methods=['GET'])
# def get_carbon_materials():
#     """Get all materials from saved forms for carbon emission calculation"""
#     session = None
#     try:
#         session = get_db_session()
#         project_name = request.args.get('project_name', 'default')
        
#         # Get project
#         project = get_or_create_project(session, project_name)
        
#         # Get all form data for this project
#         form_data_entries = session.query(FormData).filter_by(
#             project_id=project.id
#         ).all()
        
#         all_materials = []
#         forms_found = []
        
#         for form_entry in form_data_entries:
#             forms_found.append(form_entry.form_name)
#             materials = form_entry.materials if form_entry.materials else []
            
#             for i, material in enumerate(materials):
#                 # Add form name and create unique ID for each material
#                 material_with_form = {
#                     'id': f"{form_entry.form_name}_{material.get('id', i)}",
#                     'form_name': form_entry.form_name,
#                     'component': material.get('component', ''),
#                     'material_type': material.get('materialType', ''),
#                     'sub_material_type': material.get('subMaterialType', ''),
#                     'quantity': material.get('quantity', ''),
#                     'unit': material.get('unit', ''),
#                     'rate': material.get('rate', ''),
#                     'embedded_carbon_energy': material.get('embedded_carbon_energy', ''),
#                     'carbon_emission_factor': material.get('carbon_emission_factor', '')
#                 }
#                 all_materials.append(material_with_form)
        
#         # Save to carbon emission data table for tracking
#         try:
#             existing_carbon_data = session.query(CarbonEmissionData).filter_by(
#                 project_id=project.id
#             ).first()
            
#             if existing_carbon_data:
#                 existing_carbon_data.materials = all_materials
#                 existing_carbon_data.total_materials = len(all_materials)
#                 existing_carbon_data.updated_at = datetime.utcnow()
#             else:
#                 carbon_data = CarbonEmissionData(
#                     project_id=project.id,
#                     materials=all_materials,
#                     total_materials=len(all_materials)
#                 )
#                 session.add(carbon_data)
            
#             session.commit()
#         except Exception as carbon_error:
#             print(f"Warning: Could not save carbon emission data: {carbon_error}")
#             # Don't fail the main operation if carbon data save fails
#             session.rollback()
        
#         print(f"=== CARBON MATERIALS RETRIEVED FROM DATABASE ===")
#         print(f"Project: {project.name}")
#         print(f"Total materials: {len(all_materials)}")
#         print(f"From forms: {forms_found}")
#         print("=================================================")
        
#         return jsonify({
#             'success': True,
#             'project_id': project.id,
#             'project_name': project.name,
#             'materials': all_materials,
#             'total_count': len(all_materials),
#             'forms': forms_found
#         })
        
#     except SQLAlchemyError as e:
#         print(f"Database error getting carbon materials: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': f'Database error: {str(e)}'
#         }), 500
#     except Exception as e:
#         print(f"Error getting carbon materials: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#     finally:
#         if session:
#             session.close()

# @structure_works_bp.route('/api/calculate-initial-cost', methods=['POST'])
# def calculate_initial_cost():
#     """Calculate initial construction cost for submitted materials and save to database"""
#     session = None
#     try:
#         data = request.json
#         form_name = data.get('form_name', 'unknown')
#         materials = data.get('materials', [])
#         project_name = data.get('project_name', 'default')
        
#         if not materials:
#             return jsonify({
#                 'success': False,
#                 'error': 'No materials provided for calculation'
#             })
        
#         session = get_db_session()
#         project = get_or_create_project(session, project_name)
        
#         total_cost = 0
#         cost_breakdown = []
        
#         print(f"=== CALCULATING INITIAL COST ===")
#         print(f"Project: {project.name}")
#         print(f"Form: {form_name}")
#         print(f"Materials to calculate: {len(materials)}")
        
#         for material in materials:
#             try:
#                 quantity = float(material.get('quantity', 0))
#                 rate = float(material.get('rate', 0))
#                 material_cost = quantity * rate
#                 total_cost += material_cost
                
#                 cost_item = {
#                     'material': material.get('material', ''),
#                     'grade': material.get('grade', ''),
#                     'quantity': quantity,
#                     'unit': material.get('unit', ''),
#                     'rate': rate,
#                     'total_cost': material_cost,
#                     'component': material.get('component', ''),
#                     'material_type': material.get('materialType', ''),
#                     'sub_material_type': material.get('subMaterialType', '')
#                 }
#                 cost_breakdown.append(cost_item)
                
#                 print(f"  - {material.get('material', 'Unknown')} ({material.get('grade', 'N/A')}): {quantity} {material.get('unit', '')} @ ₹{rate} = ₹{material_cost:.2f}")
                
#             except (ValueError, TypeError) as e:
#                 print(f"  - Error processing material {material.get('material', 'Unknown')}: {str(e)}")
#                 continue
        
#         print(f"Total Initial Construction Cost: ₹{total_cost:.2f}")
#         print("================================")
        
#         # Store calculation result in database
#         calculation_data = {
#             'form_name': form_name,
#             'total_initial_cost': total_cost,
#             'cost_breakdown': cost_breakdown,
#             'materials': materials,
#             'calculated_at': datetime.utcnow().isoformat()
#         }
        
#         # Save to CalculationResults table
#         try:
#             existing_calc = session.query(CalculationResults).filter_by(
#                 project_id=project.id,
#                 calculation_type=f'initial_construction_{form_name}'
#             ).first()
            
#             if existing_calc:
#                 existing_calc.result_data = calculation_data
#             else:
#                 calculation_result = CalculationResults(
#                     project_id=project.id,
#                     calculation_type=f'initial_construction_{form_name}',
#                     result_data=calculation_data
#                 )
#                 session.add(calculation_result)
            
#             session.commit()
#         except Exception as calc_error:
#             print(f"Warning: Could not save calculation results: {calc_error}")
#             session.rollback()
        
#         return jsonify({
#             'success': True,
#             'project_id': project.id,
#             'project_name': project.name,
#             'form_name': form_name,
#             'total_initial_cost': total_cost,
#             'cost_breakdown': cost_breakdown,
#             'materials': materials,
#             'calculated_at': datetime.utcnow().isoformat()
#         })
        
#     except SQLAlchemyError as e:
#         if session:
#             session.rollback()
#         print(f"Database error calculating initial cost: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': f'Database error: {str(e)}'
#         }), 500
#     except Exception as e:
#         if session:
#             session.rollback()
#         print(f"Error calculating initial cost: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#     finally:
#         if session:
#             session.close()

# @structure_works_bp.route('/api/calculate-initial-cost', methods=['GET'])
# def get_calculated_cost():
#     """Get calculated cost for a specific form from database"""
#     session = None
#     try:
#         form_name = request.args.get('form')
#         project_name = request.args.get('project_name', 'default')
        
#         if not form_name:
#             return jsonify({
#                 'success': False,
#                 'error': 'Form name is required'
#             })
        
#         session = get_db_session()
#         project = get_or_create_project(session, project_name)
        
#         # Get calculation result from database
#         calculation = session.query(CalculationResults).filter_by(
#             project_id=project.id,
#             calculation_type=f'initial_construction_{form_name}'
#         ).first()
        
#         if calculation and calculation.result_data:
#             result = calculation.result_data
#             return jsonify({
#                 'success': True,
#                 'project_id': project.id,
#                 'project_name': project.name,
#                 'form_name': form_name,
#                 'total_initial_cost': result.get('total_initial_cost', 0),
#                 'cost_breakdown': result.get('cost_breakdown', []),
#                 'materials': result.get('materials', []),
#                 'calculated_at': result.get('calculated_at')
#             })
#         else:
#             return jsonify({
#                 'success': True,
#                 'project_id': project.id,
#                 'project_name': project.name,
#                 'form_name': form_name,
#                 'total_initial_cost': 0,
#                 'cost_breakdown': [],
#                 'materials': [],
#                 'message': 'No calculation data found for this form'
#             })
            
#     except SQLAlchemyError as e:
#         print(f"Database error getting calculated cost: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': f'Database error: {str(e)}'
#         }), 500
#     except Exception as e:
#         print(f"Error getting calculated cost: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#     finally:
#         if session:
#             session.close()

# @structure_works_bp.route('/api/get-form-data/<form_name>', methods=['GET'])
# def get_form_data(form_name):
#     """Get saved form data for a specific form from database"""
#     session = None
#     try:
#         project_name = request.args.get('project_name', 'default')
#         session = get_db_session()
#         project = get_or_create_project(session, project_name)
        
#         # Get form data from database
#         form_data = session.query(FormData).filter_by(
#             project_id=project.id,
#             form_name=form_name
#         ).first()
        
#         if form_data:
#             return jsonify({
#                 'success': True,
#                 'project_id': project.id,
#                 'project_name': project.name,
#                 'form_name': form_name,
#                 'data': {
#                     'form_name': form_data.form_name,
#                     'materials': form_data.materials,
#                     'timestamp': form_data.timestamp.isoformat() if form_data.timestamp else None,
#                     'saved_at': form_data.saved_at.isoformat() if form_data.saved_at else None
#                 }
#             })
#         else:
#             return jsonify({
#                 'success': True,
#                 'project_id': project.id,
#                 'project_name': project.name,
#                 'form_name': form_name,
#                 'data': None,
#                 'message': 'No data found for this form'
#             })
            
#     except SQLAlchemyError as e:
#         print(f"Database error getting form data: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': f'Database error: {str(e)}'
#         }), 500
#     except Exception as e:
#         print(f"Error getting form data: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#     finally:
#         if session:
#             session.close()

# @structure_works_bp.route('/api/get-all-form-data', methods=['GET'])
# def get_all_form_data():
#     """Get all saved form data from database"""
#     session = None
#     try:
#         project_name = request.args.get('project_name', 'default')
#         session = get_db_session()
#         project = get_or_create_project(session, project_name)
        
#         # Get all form data for this project
#         form_data_entries = session.query(FormData).filter_by(
#             project_id=project.id
#         ).all()
        
#         all_form_data = {}
#         for form_entry in form_data_entries:
#             all_form_data[form_entry.form_name] = {
#                 'form_name': form_entry.form_name,
#                 'materials': form_entry.materials,
#                 'timestamp': form_entry.timestamp.isoformat() if form_entry.timestamp else None,
#                 'saved_at': form_entry.saved_at.isoformat() if form_entry.saved_at else None
#             }
        
#         return jsonify({
#             'success': True,
#             'project_id': project.id,
#             'project_name': project.name,
#             'data': all_form_data,
#             'forms_count': len(all_form_data)
#         })
        
#     except SQLAlchemyError as e:
#         print(f"Database error getting all form data: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': f'Database error: {str(e)}'
#         }), 500
#     except Exception as e:
#         print(f"Error getting all form data: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#     finally:
#         if session:
#             session.close()

# @structure_works_bp.route('/api/clear-form-data', methods=['DELETE'])
# def clear_form_data():
#     """Clear form data (optionally for specific project)"""
#     session = None
#     try:
#         project_name = request.args.get('project_name', 'default')
#         session = get_db_session()
#         project = get_or_create_project(session, project_name)
        
#         # Delete all form data for this project
#         deleted_forms = session.query(FormData).filter_by(
#             project_id=project.id
#         ).delete()
        
#         # Also delete related calculation results
#         deleted_calcs = session.query(CalculationResults).filter_by(
#             project_id=project.id
#         ).delete()
        
#         # Delete carbon emission data
#         deleted_carbon = session.query(CarbonEmissionData).filter_by(
#             project_id=project.id
#         ).delete()
        
#         session.commit()
        
#         return jsonify({
#             'success': True,
#             'project_id': project.id,
#             'project_name': project.name,
#             'message': f'Form data cleared successfully',
#             'deleted_forms': deleted_forms,
#             'deleted_calculations': deleted_calcs,
#             'deleted_carbon_data': deleted_carbon
#         })
        
#     except SQLAlchemyError as e:
#         if session:
#             session.rollback()
#         print(f"Database error clearing form data: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': f'Database error: {str(e)}'
#         }), 500
#     except Exception as e:
#         if session:
#             session.rollback()
#         print(f"Error clearing form data: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#     finally:
#         if session:
#             session.close()

# @structure_works_bp.route('/api/debug-form-storage', methods=['GET'])
# def debug_form_storage():
#     """Debug endpoint to check what's stored in database"""
#     session = None
#     try:
#         project_name = request.args.get('project_name', 'default')
#         session = get_db_session()
#         project = get_or_create_project(session, project_name)
        
#         # Get all form data
#         form_data_entries = session.query(FormData).filter_by(
#             project_id=project.id
#         ).all()
        
#         debug_data = {
#             'project_id': project.id,
#             'project_name': project.name,
#             'forms': []
#         }
        
#         for form_entry in form_data_entries:
#             debug_data['forms'].append({
#                 'form_name': form_entry.form_name,
#                 'materials_count': len(form_entry.materials) if form_entry.materials else 0,
#                 'timestamp': form_entry.timestamp.isoformat() if form_entry.timestamp else None,
#                 'saved_at': form_entry.saved_at.isoformat() if form_entry.saved_at else None
#             })
        
#         return jsonify({
#             'success': True,
#             'debug_data': debug_data
#         })
        
#     except SQLAlchemyError as e:
#         print(f"Database error in debug: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': f'Database error: {str(e)}'
#         }), 500
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#     finally:
#         if session:
#             session.close()

# # New endpoint to get projects
# @structure_works_bp.route('/api/get-projects', methods=['GET'])
# def get_projects():
#     """Get all projects from database"""
#     session = None
#     try:
#         session = get_db_session()
#         from ..models.database import Project
        
#         projects = session.query(Project).filter_by(is_active=True).all()
        
#         project_list = []
#         for project in projects:
#             project_list.append({
#                 'id': project.id,
#                 'name': project.name,
#                 'description': project.description,
#                 'created_at': project.created_at.isoformat() if project.created_at else None,
#                 'updated_at': project.updated_at.isoformat() if project.updated_at else None
#             })
        
#         return jsonify({
#             'success': True,
#             'projects': project_list,
#             'count': len(project_list)
#         })
        
#     except SQLAlchemyError as e:
#         print(f"Database error getting projects: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': f'Database error: {str(e)}'
#         }), 500
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#     finally:
#         if session:
#             session.close()

from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Import database models
from api.models.database import get_db_session, get_or_create_project, FormData, CalculationResults
def initialize_database():
    """Initialize/reset the database - called manually or on server restart"""
    try:
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            # Clear all existing calculation results
            session.query(CalculationResults).filter_by(project_id=project.id).delete()
            session.commit()
            print("=== DATABASE CALCULATIONS CLEARED ===")
        finally:
            session.close()
    except Exception as e:
        print(f"Error clearing database calculations: {e}")

# Call this when the blueprint is loaded

structure_works_bp = Blueprint('structure_works', __name__)

@structure_works_bp.route('/api/save-form-data/<form_name>', methods=['POST'])
def save_form_data(form_name):
    """Save form data for a specific form to database"""
    try:
        data = request.json
        session = get_db_session()
        
        try:
            # Get or create project
            project = get_or_create_project(session, "default")
            
            # Check if form data already exists
            existing_form = session.query(FormData).filter_by(
                project_id=project.id, 
                form_name=form_name
            ).first()
            
            if existing_form:
                # Update existing form data
                existing_form.materials = data.get('materials', [])
                existing_form.saved_at = datetime.now()
            else:
                # Create new form data
                form_data = FormData(
                    project_id=project.id,
                    form_name=form_name,
                    materials=data.get('materials', [])
                )
                session.add(form_data)
            
            session.commit()
            
            print(f"=== FORM DATA SAVED TO DATABASE ===")
            print(f"Form: {form_name}")
            print(f"Materials count: {len(data.get('materials', []))}")
            print(f"Project ID: {project.id}")
            print("===================================")
            
            return jsonify({
                'success': True,
                'message': f'Form data saved successfully for {form_name}',
                'form_name': form_name,
                'materials_count': len(data.get('materials', []))
            })
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"Error saving form data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@structure_works_bp.route('/api/get-carbon-materials', methods=['GET'])
def get_carbon_materials():
    """Get all materials from saved forms for carbon emission calculation"""
    try:
        session = get_db_session()
        
        try:
            project = get_or_create_project(session, "default")
            
            # CHANGE FROM lowercase to Title Case
            structure_forms = ['Foundation', 'Sub-Structure', 'Super-Structure', 'Miscellaneous']
            
            # Get form data only for structure forms
            form_data_list = session.query(FormData).filter(
                FormData.project_id == project.id,
                FormData.form_name.in_(structure_forms)
            ).all()
            
            all_materials = []
            forms_found = []
            processed_materials = set()
            
            for form_data in form_data_list:
                forms_found.append(form_data.form_name)
                materials = form_data.materials or []
                
                print(f"Processing form: {form_data.form_name} with {len(materials)} materials")
                
                for material_index, material in enumerate(materials):
                    material_key = (
                        form_data.form_name,
                        material.get('component', ''),
                        material.get('materialType', ''),
                        material.get('subMaterialType', ''),
                        material.get('quantity', ''),
                        material.get('unit', ''),
                        material_index
                    )
                    
                    if material_key in processed_materials:
                        continue
                    
                    processed_materials.add(material_key)
                    
                    material_with_form = {
                        'id': f"{form_data.form_name}_{material_index}_{len(all_materials)}",
                        'form_name': form_data.form_name,
                        'component': material.get('component', ''),
                        'material_type': material.get('materialType', ''),
                        'sub_material_type': material.get('subMaterialType', ''),
                        'quantity': material.get('quantity', ''),
                        'unit': material.get('unit', ''),
                        'rate': material.get('rate', ''),
                        'embedded_carbon_energy': material.get('embedded_carbon_energy', ''),
                        'carbon_emission_factor': material.get('carbon_emission_factor', '')
                    }
                    all_materials.append(material_with_form)
            
            print(f"=== CARBON MATERIALS RETRIEVED FROM DATABASE ===")
            print(f"Structure forms processed: {forms_found}")
            print(f"Total unique materials: {len(all_materials)}")
            print("===============================================")
            
            return jsonify({
                'success': True,
                'materials': all_materials,
                'total_count': len(all_materials),
                'forms': forms_found
            })
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"Error getting carbon materials: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@structure_works_bp.route('/api/calculate-initial-cost', methods=['POST'])
def calculate_initial_cost():
    """Calculate initial construction cost for submitted materials and save to database"""
    try:
        data = request.json
        form_name = data.get('form_name', 'unknown')
        materials = data.get('materials', [])
        
        if not materials:
            return jsonify({
                'success': False,
                'error': 'No materials provided for calculation'
            })
        
        total_cost = 0
        cost_breakdown = []
        
        print(f"=== CALCULATING INITIAL COST ===")
        print(f"Form: {form_name}")
        print(f"Materials to calculate: {len(materials)}")
        
        for material in materials:
            try:
                quantity = float(material.get('quantity', 0))
                rate = float(material.get('rate', 0))
                material_cost = quantity * rate
                total_cost += material_cost
                
                cost_item = {
                    'material': material.get('materialType', ''),
                    'grade': material.get('subMaterialType', ''),
                    'quantity': quantity,
                    'unit': material.get('unit', ''),
                    'rate': rate,
                    'total_cost': material_cost,
                    'component': material.get('component', '')
                }
                cost_breakdown.append(cost_item)
                
                print(f"  - {material.get('materialType', 'Unknown')} ({material.get('subMaterialType', 'N/A')}): {quantity} {material.get('unit', '')} @ ₹{rate} = ₹{material_cost:.2f}")
                
            except (ValueError, TypeError) as e:
                print(f"  - Error processing material {material.get('materialType', 'Unknown')}: {str(e)}")
                continue
        
        print(f"Total Initial Construction Cost: ₹{total_cost:.2f}")
        print("================================")
        
        # Save calculation result to database
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            calculation_result = {
                'form_name': form_name,
                'total_initial_cost': total_cost,
                'cost_breakdown': cost_breakdown,
                'materials': materials,
                'calculated_at': datetime.now().isoformat()
            }
            
            # Save to CalculationResults table
            calc_result = CalculationResults(
                project_id=project.id,
                calculation_type='initial_construction_cost',
                result_data=calculation_result
            )
            session.add(calc_result)
            session.commit()
            
        finally:
            session.close()
        
        return jsonify({
            'success': True,
            'form_name': form_name,
            'total_initial_cost': total_cost,
            'cost_breakdown': cost_breakdown,
            'materials': materials,
            'calculated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error calculating initial cost: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@structure_works_bp.route('/api/calculate-initial-cost', methods=['GET'])
def get_calculated_cost():
    """Get calculated cost for a specific form from database"""
    try:
        form_name = request.args.get('form')
        
        if not form_name:
            return jsonify({
                'success': False,
                'error': 'Form name is required'
            })
        
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            # Get the latest calculation result for this form
            calc_result = session.query(CalculationResults).filter_by(
                project_id=project.id,
                calculation_type='initial_construction_cost'
            ).order_by(CalculationResults.created_at.desc()).first()
            
            if calc_result and calc_result.result_data.get('form_name') == form_name:
                result = calc_result.result_data
                return jsonify({
                    'success': True,
                    'form_name': form_name,
                    'total_initial_cost': result.get('total_initial_cost', 0),
                    'cost_breakdown': result.get('cost_breakdown', []),
                    'materials': result.get('materials', []),
                    'calculated_at': result.get('calculated_at')
                })
            else:
                return jsonify({
                    'success': True,
                    'form_name': form_name,
                    'total_initial_cost': 0,
                    'cost_breakdown': [],
                    'materials': [],
                    'message': 'No calculation data found for this form'
                })
                
        finally:
            session.close()
            
    except Exception as e:
        print(f"Error getting calculated cost: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@structure_works_bp.route('/api/get-form-data/<form_name>', methods=['GET'])
def get_form_data(form_name):
    """Get saved form data for a specific form from database"""
    try:
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            form_data = session.query(FormData).filter_by(
                project_id=project.id, 
                form_name=form_name
            ).first()
            
            if form_data:
                return jsonify({
                    'success': True,
                    'form_name': form_name,
                    'data': {
                        'form_name': form_data.form_name,
                        'materials': form_data.materials,
                        'saved_at': form_data.saved_at.isoformat() if form_data.saved_at else None
                    }
                })
            else:
                return jsonify({
                    'success': True,
                    'form_name': form_name,
                    'data': None,
                    'message': 'No data found for this form'
                })
                
        finally:
            session.close()
            
    except Exception as e:
        print(f"Error getting form data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@structure_works_bp.route('/api/check-form-completion', methods=['GET'])
def check_form_completion():
    """Check which structure forms have been completed"""
    try:
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            structure_forms = ['Foundation', 'Sub-Structure', 'Super-Structure', 'Miscellaneous']
            completed_forms = []
            
            for form_name in structure_forms:
                form_data = session.query(FormData).filter_by(
                    project_id=project.id, 
                    form_name=form_name
                ).first()
                
                if form_data and form_data.materials and len(form_data.materials) > 0:
                    # Check if form has materials with required fields
                    has_valid_materials = any(
                        material.get('materialType') and 
                        material.get('subMaterialType') and 
                        material.get('quantity') and 
                        material.get('rate') and 
                        material.get('unit')
                        for material in form_data.materials
                    )
                    if has_valid_materials:
                        completed_forms.append(form_name)
            
            return jsonify({
                'success': True,
                'completed_forms': completed_forms,
                'total_structure_forms': len(structure_forms),
                'completed_count': len(completed_forms)
            })
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"Error checking form completion: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@structure_works_bp.route('/api/validate-form-sequence', methods=['POST'])
def validate_form_sequence():
    """Validate if user can navigate to a specific form"""
    try:
        data = request.json
        target_form = data.get('target_form', '')  # NOW COMES IN TITLE CASE
        current_form = data.get('current_form', '')  # NOW COMES IN TITLE CASE
        
        # Define the structure forms sequence (Title Case to match database)
        structure_forms = ['Foundation', 'Sub-Structure', 'Super-Structure', 'Miscellaneous']
        form_sequence = [
            'Foundation', 'Sub-Structure', 'Super-Structure', 'Miscellaneous',
            'Economic Parameter', 'Carbon Emission Data', 'Carbon Emission Cost Data',
            'Bridge And Traffic', 'Maintenance And Repair Data', 'Demolition And Recycling'
        ]
        
        if target_form not in form_sequence:
            return jsonify({
                'success': True,
                'can_navigate': True,
                'message': ''
            })
        
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            # Check CURRENT form completion (BLOCKING)
            current_form_incomplete = False
            if current_form in structure_forms:
                current_form_data = session.query(FormData).filter_by(
                    project_id=project.id,
                    form_name=current_form  # Now matches Title Case
                ).first()
                
                print(f"=== VALIDATION CHECK ===")
                print(f"Current form: {current_form}")
                print(f"Form data found: {current_form_data is not None}")
                if current_form_data:
                    print(f"Materials count: {len(current_form_data.materials) if current_form_data.materials else 0}")
                
                if not current_form_data or not current_form_data.materials or len(current_form_data.materials) == 0:
                    current_form_incomplete = True
                    print("Form incomplete: No materials")
                else:
                    # Check if ALL materials in current form are complete
                    all_materials_complete = all(
                        material.get('materialType') and 
                        material.get('materialType').strip() != '' and
                        material.get('subMaterialType') and 
                        material.get('subMaterialType').strip() != '' and
                        material.get('quantity') and 
                        str(material.get('quantity')).strip() != '' and
                        material.get('rate') and 
                        str(material.get('rate')).strip() != '' and
                        material.get('unit') and 
                        material.get('unit').strip() != ''
                        for material in current_form_data.materials
                    )
                    
                    print(f"All materials complete: {all_materials_complete}")
                    
                    if not all_materials_complete:
                        current_form_incomplete = True
                        print("Form incomplete: Some materials missing fields")
            
            # If current form is incomplete, BLOCK navigation
            if current_form_incomplete:
                return jsonify({
                    'success': True,
                    'can_navigate': False,
                    'is_current_form_incomplete': True,
                    'message': f'Please complete the {current_form.replace("-", " ")} form before proceeding. All fields marked with * are required.'
                })
            
            # Check PREVIOUS forms completion (WARNING only)
            target_index = form_sequence.index(target_form)
            
            # Determine which previous forms to check
            if target_form in structure_forms:
                target_structure_index = structure_forms.index(target_form)
                required_forms = structure_forms[:target_structure_index]
            else:
                # For non-structure forms, check all structure forms
                required_forms = structure_forms
            
            missing_forms = []
            
            for required_form in required_forms:
                form_data = session.query(FormData).filter_by(
                    project_id=project.id,
                    form_name=required_form  # Now matches Title Case
                ).first()
                
                # Check if form exists and has materials
                if not form_data or not form_data.materials or len(form_data.materials) == 0:
                    missing_forms.append(required_form.replace('-', ' '))
                    continue
                
                # Check if ALL materials have ALL required fields filled
                all_materials_complete = all(
                    material.get('materialType') and 
                    material.get('materialType').strip() != '' and
                    material.get('subMaterialType') and 
                    material.get('subMaterialType').strip() != '' and
                    material.get('quantity') and 
                    str(material.get('quantity')).strip() != '' and
                    material.get('rate') and 
                    str(material.get('rate')).strip() != '' and
                    material.get('unit') and 
                    material.get('unit').strip() != ''
                    for material in form_data.materials
                )
                
                # If ANY material is incomplete, mark form as incomplete
                if not all_materials_complete:
                    missing_forms.append(required_form.replace('-', ' '))
            
            # Previous forms incomplete = WARNING (not blocking)
            warning_message = ''
            if len(missing_forms) > 0:
                if len(missing_forms) == 1:
                    warning_message = f'Warning: {missing_forms[0]} form is incomplete. Please complete it for accurate calculations.'
                else:
                    warning_message = f'Warning: The following forms are incomplete: {", ".join(missing_forms)}. Please complete them for accurate calculations.'
            
            return jsonify({
                'success': True,
                'can_navigate': True,
                'is_current_form_incomplete': False,
                'has_incomplete_previous_forms': len(missing_forms) > 0,
                'missing_forms': missing_forms,
                'message': warning_message
            })
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"Error validating form sequence: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@structure_works_bp.route('/api/get-all-form-data', methods=['GET'])
def get_all_form_data():
    """Get all saved form data from database"""
    try:
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            form_data_list = session.query(FormData).filter_by(project_id=project.id).all()
            
            all_data = {}
            for form_data in form_data_list:
                all_data[form_data.form_name] = {
                    'form_name': form_data.form_name,
                    'materials': form_data.materials,
                    'saved_at': form_data.saved_at.isoformat() if form_data.saved_at else None
                }
            
            return jsonify({
                'success': True,
                'data': all_data,
                'forms_count': len(all_data)
            })
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"Error getting all form data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@structure_works_bp.route('/api/clear-form-data', methods=['DELETE'])
def clear_form_data():
    """Clear all saved form data from database"""
    try:
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            # Delete all form data for this project
            session.query(FormData).filter_by(project_id=project.id).delete()
            session.query(CalculationResults).filter_by(project_id=project.id).delete()
            
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'All form data cleared successfully'
            })
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"Error clearing form data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
@structure_works_bp.route('/api/calculate-and-save-initial-cost', methods=['POST'])
def calculate_and_save_initial_cost():
    """Calculate initial construction cost from all saved forms and save result"""
    try:
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            # Get all form data for structure forms
            structure_forms = ['Foundation', 'Sub-Structure', 'Super-Structure', 'Miscellaneous']
            all_materials = []
            forms_included = []
            
            for form_name in structure_forms:
                form_data = session.query(FormData).filter_by(
                    project_id=project.id, 
                    form_name=form_name
                ).first()
                
                if form_data and form_data.materials:
                    valid_materials = [
                        material for material in form_data.materials 
                        if all([
                            material.get('quantity'),
                            material.get('rate'),
                            material.get('materialType'),
                            material.get('subMaterialType'),
                            material.get('unit')
                        ])
                    ]
                    
                    if valid_materials:
                        all_materials.extend(valid_materials)
                        forms_included.append(form_name)
            
            if not all_materials:
                print("=== NO VALID MATERIALS FOUND FOR CALCULATION ===")
                return jsonify({
                    'success': False,
                    'error': 'No valid materials found for calculation'
                })
            
            # Calculate total cost
            total_cost = 0
            cost_breakdown = []
            
            print(f"")
            print(f"=== CALCULATING INITIAL CONSTRUCTION COST FROM DATABASE ===")
            print(f"Server restart: Database cleared and recalculating...")
            print(f"Forms included: {', '.join(forms_included)}")
            print(f"Total materials to process: {len(all_materials)}")
            print(f"")
            
            for i, material in enumerate(all_materials, 1):
                try:
                    quantity = float(material.get('quantity', 0))
                    rate = float(material.get('rate', 0))
                    material_cost = quantity * rate
                    total_cost += material_cost
                    
                    cost_item = {
                        'form': material.get('form_name', 'unknown'),
                        'component': material.get('component', ''),
                        'material': material.get('materialType', ''),
                        'grade': material.get('subMaterialType', ''),
                        'quantity': quantity,
                        'unit': material.get('unit', ''),
                        'rate': rate,
                        'total_cost': material_cost
                    }
                    cost_breakdown.append(cost_item)
                    
                    print(f"  {i:2d}. {material.get('materialType', 'Unknown'):20} ({material.get('subMaterialType', 'N/A'):15})")
                    print(f"      {quantity:8.2f} {material.get('unit', ''):6} @ ₹{rate:10.2f} = ₹{material_cost:12.2f}")
                    
                except (ValueError, TypeError) as e:
                    print(f"  ERROR processing material {i}: {str(e)}")
                    continue
            
            print(f"")
            print(f"TOTAL INITIAL CONSTRUCTION COST: ₹{total_cost:,.2f}")
            print(f"Cost saved to database successfully")
            print(f"===============================================================")
            print(f"")
            
            # Save calculation result (remove previous auto calculations first)
            session.query(CalculationResults).filter_by(
                project_id=project.id,
                calculation_type='initial_construction_cost_auto'
            ).delete()
            
            calculation_result = {
                'calculation_type': 'initial_construction_cost_auto',
                'total_initial_cost': total_cost,
                'cost_breakdown': cost_breakdown,
                'forms_included': forms_included,
                'materials_count': len(all_materials),
                'calculated_at': datetime.now().isoformat()
            }
            
            calc_result = CalculationResults(
                project_id=project.id,
                calculation_type='initial_construction_cost_auto',
                result_data=calculation_result
            )
            session.add(calc_result)
            session.commit()
            
            return jsonify({
                'success': True,
                'total_initial_cost': total_cost,
                'cost_breakdown': cost_breakdown,
                'forms_included': forms_included,
                'materials_count': len(all_materials),
                'calculated_at': datetime.now().isoformat()
            })
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"ERROR calculating initial construction cost: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
@structure_works_bp.route('/api/get-initial-construction-cost', methods=['GET'])
def get_initial_construction_cost():
    """Get the latest calculated initial construction cost"""
    try:
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            calc_result = session.query(CalculationResults).filter_by(
                project_id=project.id,
                calculation_type='initial_construction_cost_auto'
            ).order_by(CalculationResults.created_at.desc()).first()
            
            if calc_result:
                return jsonify({
                    'success': True,
                    'result': calc_result.result_data
                })
            else:
                return jsonify({
                    'success': True,
                    'result': None,
                    'message': 'No calculation found'
                })
                
        finally:
            session.close()
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@structure_works_bp.route('/api/clear-database-calculations', methods=['DELETE'])
def clear_database_calculations():
    """Clear all calculation results AND form data from database"""
    try:
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            calc_deleted = session.query(CalculationResults).filter_by(project_id=project.id).count()
            form_deleted = session.query(FormData).filter_by(project_id=project.id).count()
            
            session.query(CalculationResults).filter_by(project_id=project.id).delete()
            session.query(FormData).filter_by(project_id=project.id).delete()  # ADD THIS LINE
            
            session.commit()
            
            print(f"=== MANUALLY CLEARED {calc_deleted} CALCULATIONS & {form_deleted} FORM DATA ===")
            
            return jsonify({
                'success': True,
                'message': f'Cleared {calc_deleted} calculations and {form_deleted} form data',
                'calculations_deleted': calc_deleted,
                'form_data_deleted': form_deleted
            })
        finally:
            session.close()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
def debug_form_storage():
    """Debug endpoint to check what's stored in database"""
    try:
        session = get_db_session()
        try:
            project = get_or_create_project(session, "default")
            
            form_data_list = session.query(FormData).filter_by(project_id=project.id).all()
            calc_results = session.query(CalculationResults).filter_by(project_id=project.id).all()
            
            storage_data = {}
            for form_data in form_data_list:
                storage_data[form_data.form_name] = {
                    'materials': form_data.materials,
                    'saved_at': form_data.saved_at.isoformat() if form_data.saved_at else None
                }
            
            return jsonify({
                'success': True,
                'storage_keys': list(storage_data.keys()),
                'storage_data': storage_data,
                'calculation_results_count': len(calc_results)
            })
            
        finally:
            session.close()
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500