# from flask import Blueprint, jsonify, request
# from osbridgelcca.core.material_types_consts import (
#     get_forms, get_components, get_materials, get_sub_materials, 
#     get_units_for_material, get_material_cost_template, is_valid_form, 
#     is_valid_component, is_valid_material_for_form_component, is_valid_material
# )

# materials_dropdown_bp = Blueprint('materials_dropdown', __name__)
# material_costs = get_material_cost_template()

# # Get all forms (foundation, sub-structure, super-structure, miscellaneous)
# @materials_dropdown_bp.route('/forms')
# def forms():
    
#     return jsonify(get_forms())

# # Get components for a specific form
# @materials_dropdown_bp.route('/components/<form_name>')
# def components(form_name):
#     # Handle URL decoding and form name normalization
    
#     form_name = form_name.replace('%20', ' ').replace('-', '-')
#     if not is_valid_form(form_name):
#         return jsonify([])
#     return jsonify(get_components(form_name))

# # Get all materials (independent of form/component)
# @materials_dropdown_bp.route('/materials')
# def all_materials():
#     return jsonify(get_materials())

# # Get materials for a specific form and component (backward compatibility)
# @materials_dropdown_bp.route('/materials/<form_name>/<component_name>')
# def materials_for_component(form_name, component_name):
#     # Since materials are independent of components, return all materials
#     return jsonify(get_materials())

# # Get sub-materials (grades) for a specific material
# @materials_dropdown_bp.route('/sub-materials/<material_name>')
# def sub_materials_for_material(material_name):
#     # Handle URL decoding
#     material_name = material_name.replace('%20', ' ')
    
#     if not is_valid_material(material_costs, material_name):
#         return jsonify([])
#     return jsonify(get_sub_materials(None, None, material_name))

# # Get sub-materials for a specific form, component, and material (backward compatibility)
# @materials_dropdown_bp.route('/sub-materials/<form_name>/<component_name>/<material_name>')
# def sub_materials(form_name, component_name, material_name):
#     # Handle URL decoding
#     form_name = form_name.replace('%20', ' ').replace('-', '-')
#     component_name = component_name.replace('%20', ' ')
#     material_name = material_name.replace('%20', ' ')
    
#     if not is_valid_material(material_costs, material_name):
#         return jsonify([])
#     return jsonify(get_sub_materials(form_name, component_name, material_name))

# # Get units for a specific material
# @materials_dropdown_bp.route('/units/<material_name>')
# def units_for_material(material_name):
#     # Handle URL decoding
#     material_name = material_name.replace('%20', ' ')
    
#     if not is_valid_material(material_costs, material_name):
#         return jsonify([])
#     return jsonify(get_units_for_material(None, None, material_name))

# # Get units for a specific form, component, and material (backward compatibility)
# @materials_dropdown_bp.route('/units/<form_name>/<component_name>/<material_name>')
# def units(form_name, component_name, material_name):
#     # Handle URL decoding
#     form_name = form_name.replace('%20', ' ').replace('-', '-')
#     component_name = component_name.replace('%20', ' ')
#     material_name = material_name.replace('%20', ' ')
    
#     if not is_valid_material(material_costs, material_name):
#         return jsonify([])
#     return jsonify(get_units_for_material(form_name, component_name, material_name))

# # Get all data for a specific form (components with all materials and their properties)
# @materials_dropdown_bp.route('/form-data/<form_name>')
# def form_data(form_name):
#     # Handle URL decoding and form name normalization
#     form_name = form_name.replace('%20', ' ').replace('-', '-')
    
#     if not is_valid_form(form_name):
#         return jsonify({})
    
#     form_components = get_components(form_name)
#     all_materials = get_materials()
#     result = {}
    
#     for component in form_components:
#         result[component] = {}
        
#         # Since materials are independent, all materials are available for all components
#         for material in all_materials:
#             result[component][material] = {
#                 'sub_materials': get_sub_materials(form_name, component, material),
#                 'units': get_units_for_material(form_name, component, material)
#             }
    
#     return jsonify(result)

# # Get material data (grades and units) for a specific material
# @materials_dropdown_bp.route('/material-data/<material_name>')
# def material_data(material_name):
#     # Handle URL decoding
#     material_name = material_name.replace('%20', ' ')
    
#     if not is_valid_material(material_costs, material_name):
#         return jsonify({})
    
#     return jsonify({
#         'sub_materials': get_sub_materials(None, None, material_name),
#         'units': get_units_for_material(None, None, material_name)
#     })

# # Debug endpoint to check form name mappings
# @materials_dropdown_bp.route('/debug/<form_name>')
# def debug_form(form_name):
#     form_name = form_name.replace('%20', ' ').replace('-', '-')
#     return jsonify({
#         'received_form_name': form_name,
#         'is_valid': is_valid_form(form_name),
#         'available_forms': get_forms(),
#         'components': get_components(form_name) if is_valid_form(form_name) else [],
#         'all_materials': get_materials()
#     })

# # Debug endpoint for material data
# @materials_dropdown_bp.route('/debug/material/<material_name>')
# def debug_material(material_name):
#     material_name = material_name.replace('%20', ' ')
#     return jsonify({
#         'received_material_name': material_name,
#         'is_valid': is_valid_material(material_costs, material_name),
#         'sub_materials': get_sub_materials(None, None, material_name) if is_valid_material(material_costs, material_name) else [],
#         'units': get_units_for_material(None, None, material_name) if is_valid_material(material_costs, material_name) else []
#     })
from flask import Blueprint, jsonify, request
from osbridgelcca.core.material_types_consts import (
    get_forms, get_components, get_materials, get_sub_materials, 
    get_units_for_material, get_material_cost_template, is_valid_form, 
    is_valid_component, is_valid_material_for_form_component, is_valid_material,
    get_component_materials
)

materials_dropdown_bp = Blueprint('materials_dropdown', __name__)
material_costs = get_material_cost_template()

# Get all forms (foundation, sub-structure, super-structure, miscellaneous)
@materials_dropdown_bp.route('/forms')
def forms():
    return jsonify(get_forms())

# Get components for a specific form
@materials_dropdown_bp.route('/components/<form_name>')
def components(form_name):
    # Handle URL decoding and form name normalization
    form_name = form_name.replace('%20', ' ').replace('-', '-')
    if not is_valid_form(form_name):
        return jsonify([])
    return jsonify(get_components(form_name))

# Get all materials (independent of form/component) - for backward compatibility
@materials_dropdown_bp.route('/materials')
def all_materials():
    return jsonify(get_materials())

# Get materials for a specific form and component (NOW COMPONENT-DEPENDENT)
@materials_dropdown_bp.route('/materials/<form_name>/<component_name>')
def materials_for_component(form_name, component_name):
    # Handle URL decoding
    form_name = form_name.replace('%20', ' ').replace('-', '-')
    component_name = component_name.replace('%20', ' ')
    
    if not is_valid_form(form_name) or not is_valid_component(form_name, component_name):
        return jsonify([])
    
    # Return materials specific to this component
    return jsonify(get_component_materials(form_name, component_name))

# Get sub-materials (grades) for a specific material
@materials_dropdown_bp.route('/sub-materials/<material_name>')
def sub_materials_for_material(material_name):
    # Handle URL decoding
    material_name = material_name.replace('%20', ' ')
    
    if not is_valid_material(material_costs, material_name):
        return jsonify([])
    return jsonify(get_sub_materials(None, None, material_name))

# Get sub-materials for a specific form, component, and material (backward compatibility)
@materials_dropdown_bp.route('/sub-materials/<form_name>/<component_name>/<material_name>')
def sub_materials(form_name, component_name, material_name):
    # Handle URL decoding
    form_name = form_name.replace('%20', ' ').replace('-', '-')
    component_name = component_name.replace('%20', ' ')
    material_name = material_name.replace('%20', ' ')
    
    if not is_valid_material(material_costs, material_name):
        return jsonify([])
    return jsonify(get_sub_materials(form_name, component_name, material_name))

# Get units for a specific material
@materials_dropdown_bp.route('/units/<material_name>')
def units_for_material(material_name):
    # Handle URL decoding
    material_name = material_name.replace('%20', ' ')
    
    if not is_valid_material(material_costs, material_name):
        return jsonify([])
    return jsonify(get_units_for_material(None, None, material_name))

# Get units for a specific form, component, and material (backward compatibility)
@materials_dropdown_bp.route('/units/<form_name>/<component_name>/<material_name>')
def units(form_name, component_name, material_name):
    # Handle URL decoding
    form_name = form_name.replace('%20', ' ').replace('-', '-')
    component_name = component_name.replace('%20', ' ')
    material_name = material_name.replace('%20', ' ')
    
    if not is_valid_material(material_costs, material_name):
        return jsonify([])
    return jsonify(get_units_for_material(form_name, component_name, material_name))

# Get all data for a specific form (components with their specific materials and properties)
@materials_dropdown_bp.route('/form-data/<form_name>')
def form_data(form_name):
    # Handle URL decoding and form name normalization
    form_name = form_name.replace('%20', ' ').replace('-', '-')
    
    if not is_valid_form(form_name):
        return jsonify({})
    
    form_components = get_components(form_name)
    result = {}
    
    for component in form_components:
        result[component] = {}
        
        # Get materials specific to this component
        component_materials = get_component_materials(form_name, component)
        
        for material in component_materials:
            result[component][material] = {
                'sub_materials': get_sub_materials(form_name, component, material),
                'units': get_units_for_material(form_name, component, material)
            }
    
    return jsonify(result)

# Get material data (grades and units) for a specific material
@materials_dropdown_bp.route('/material-data/<material_name>')
def material_data(material_name):
    # Handle URL decoding
    material_name = material_name.replace('%20', ' ')
    
    if not is_valid_material(material_costs, material_name):
        return jsonify({})
    
    return jsonify({
        'sub_materials': get_sub_materials(None, None, material_name),
        'units': get_units_for_material(None, None, material_name)
    })

# Debug endpoint to check form name mappings
@materials_dropdown_bp.route('/debug/<form_name>')
def debug_form(form_name):
    form_name = form_name.replace('%20', ' ').replace('-', '-')
    return jsonify({
        'received_form_name': form_name,
        'is_valid': is_valid_form(form_name),
        'available_forms': get_forms(),
        'components': get_components(form_name) if is_valid_form(form_name) else [],
        'all_materials': get_materials()
    })

# Debug endpoint for component materials
@materials_dropdown_bp.route('/debug/<form_name>/<component_name>')
def debug_component(form_name, component_name):
    form_name = form_name.replace('%20', ' ').replace('-', '-')
    component_name = component_name.replace('%20', ' ')
    return jsonify({
        'received_form_name': form_name,
        'received_component_name': component_name,
        'is_valid_form': is_valid_form(form_name),
        'is_valid_component': is_valid_component(form_name, component_name) if is_valid_form(form_name) else False,
        'component_materials': get_component_materials(form_name, component_name) if is_valid_form(form_name) and is_valid_component(form_name, component_name) else []
    })

# Debug endpoint for material data
@materials_dropdown_bp.route('/debug/material/<material_name>')
def debug_material(material_name):
    material_name = material_name.replace('%20', ' ')
    return jsonify({
        'received_material_name': material_name,
        'is_valid': is_valid_material(material_costs, material_name),
        'sub_materials': get_sub_materials(None, None, material_name) if is_valid_material(material_costs, material_name) else [],
        'units': get_units_for_material(None, None, material_name) if is_valid_material(material_costs, material_name) else []
    })