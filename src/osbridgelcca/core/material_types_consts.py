# import copy

# # Updated template with Components -> Materials -> Sub-materials structure
# MATERIAL_COSTS_TEMPLATE = {
#     "foundation": {
#         "components": {
#             "Pile": {
#                 "materials": {
#                     "Concrete": {
#                         "units": ["cum", "kg"],
#                         "sub_materials": {
#                             "M15": {"cum": 0.0, "kg": 0.0},
#                             "M20": {"cum": 0.0, "kg": 0.0},
#                             "M25": {"cum": 0.0, "kg": 0.0},
#                             "M30": {"cum": 0.0, "kg": 0.0},
#                             "M35": {"cum": 0.0, "kg": 0.0},
#                             "M40": {"cum": 0.0, "kg": 0.0},
#                             "M45": {"cum": 0.0, "kg": 0.0},
#                             "M50": {"cum": 0.0, "kg": 0.0},
#                         }
#                     },
#                     "Steel": {
#                         "units": ["MT", "kg"],
#                         "sub_materials": {
#                             "E 165(Fe 290)": {"MT": 0.0, "kg": 0.0},
#                             "E 250(Fe 410W)A": {"MT": 0.0, "kg": 0.0},
#                             "E 250(Fe 410W)B": {"MT": 0.0, "kg": 0.0},
#                             "E 250(Fe 410)C": {"MT": 0.0, "kg": 0.0},
#                             "E 300(Fe 440)": {"MT": 0.0, "kg": 0.0},
#                             "E 350(Fe 490)": {"MT": 0.0, "kg": 0.0},
#                             "E 410(Fe 540)": {"MT": 0.0, "kg": 0.0},
#                             "E 450(Fe 570)D": {"MT": 0.0, "kg": 0.0},
#                         }
#                     }
#                 }
#             },
#             "Pile Cap": {
#                 "materials": {
#                     "Concrete": {
#                         "units": ["cum", "kg"],
#                         "sub_materials": {
#                             "M15": {"cum": 0.0, "kg": 0.0},
#                             "M20": {"cum": 0.0, "kg": 0.0},
#                             "M25": {"cum": 0.0, "kg": 0.0},
#                             "M30": {"cum": 0.0, "kg": 0.0},
#                         }
#                     },
#                     "Steel": {
#                         "units": ["MT", "kg"],
#                         "sub_materials": {
#                             "E 165(Fe 290)": {"MT": 0.0, "kg": 0.0},
#                             "E 250(Fe 410W)A": {"MT": 0.0, "kg": 0.0},
#                             "E 250(Fe 410W)B": {"MT": 0.0, "kg": 0.0},
#                         }
#                     }
#                 }
#             }
#         }
#     },
#     "sub-structure": {
#         "components": {
#             "Abutment": {
#                 "materials": {
#                     "Concrete": {
#                         "units": ["cum", "kg"],
#                         "sub_materials": {
#                             "M15": {"cum": 0.0, "kg": 0.0},
#                             "M20": {"cum": 0.0, "kg": 0.0},
#                             "M25": {"cum": 0.0, "kg": 0.0},
#                             "M30": {"cum": 0.0, "kg": 0.0},
#                             "M35": {"cum": 0.0, "kg": 0.0},
#                             "M40": {"cum": 0.0, "kg": 0.0},
#                         }
#                     },
#                     "Steel": {
#                         "units": ["MT", "kg"],
#                         "sub_materials": {
#                             "E 165(Fe 290)": {"MT": 0.0, "kg": 0.0},
#                             "E 250(Fe 410W)A": {"MT": 0.0, "kg": 0.0},
#                             "E 250(Fe 410W)B": {"MT": 0.0, "kg": 0.0},
#                             "E 250(Fe 410)C": {"MT": 0.0, "kg": 0.0},
#                         }
#                     }
#                 }
#             },
#             "Abutment protection works": {
#                 "materials": {
#                     "Concrete": {
#                         "units": ["cum", "kg"],
#                         "sub_materials": {
#                             "M15": {"cum": 0.0, "kg": 0.0},
#                             "M20": {"cum": 0.0, "kg": 0.0},
#                             "M25": {"cum": 0.0, "kg": 0.0},
#                         }
#                     }
#                 }
#             },
#             "Pier": {
#                 "materials": {
#                     "Concrete": {
#                         "units": ["cum", "kg"],
#                         "sub_materials": {
#                             "M20": {"cum": 0.0, "kg": 0.0},
#                             "M25": {"cum": 0.0, "kg": 0.0},
#                             "M30": {"cum": 0.0, "kg": 0.0},
#                             "M35": {"cum": 0.0, "kg": 0.0},
#                             "M40": {"cum": 0.0, "kg": 0.0},
#                         }
#                     },
#                     "Steel": {
#                         "units": ["MT", "kg"],
#                         "sub_materials": {
#                             "E 250(Fe 410W)A": {"MT": 0.0, "kg": 0.0},
#                             "E 250(Fe 410W)B": {"MT": 0.0, "kg": 0.0},
#                             "E 300(Fe 440)": {"MT": 0.0, "kg": 0.0},
#                             "E 350(Fe 490)": {"MT": 0.0, "kg": 0.0},
#                         }
#                     }
#                 }
#             },
#             "Pier cap": {
#                 "materials": {
#                     "Concrete": {
#                         "units": ["cum", "kg"],
#                         "sub_materials": {
#                             "M25": {"cum": 0.0, "kg": 0.0},
#                             "M30": {"cum": 0.0, "kg": 0.0},
#                             "M35": {"cum": 0.0, "kg": 0.0},
#                             "M40": {"cum": 0.0, "kg": 0.0},
#                         }
#                     },
#                     "Steel": {
#                         "units": ["MT", "kg"],
#                         "sub_materials": {
#                             "E 250(Fe 410W)A": {"MT": 0.0, "kg": 0.0},
#                             "E 250(Fe 410W)B": {"MT": 0.0, "kg": 0.0},
#                             "E 300(Fe 440)": {"MT": 0.0, "kg": 0.0},
#                         }
#                     }
#                 }
#             }
#         }
#     },
#     "super-structure": {
#         "components": {
#             "Girders/Main beams": {
#                 "materials": {
#                     "Concrete": {
#                         "units": ["cum", "kg"],
#                         "sub_materials": {
#                             "M30": {"cum": 0.0, "kg": 0.0},
#                             "M35": {"cum": 0.0, "kg": 0.0},
#                             "M40": {"cum": 0.0, "kg": 0.0},
#                             "M45": {"cum": 0.0, "kg": 0.0},
#                             "M50": {"cum": 0.0, "kg": 0.0},
#                         }
#                     },
#                     "Steel": {
#                         "units": ["MT", "kg"],
#                         "sub_materials": {
#                             "E 300(Fe 440)": {"MT": 0.0, "kg": 0.0},
#                             "E 350(Fe 490)": {"MT": 0.0, "kg": 0.0},
#                             "E 410(Fe 540)": {"MT": 0.0, "kg": 0.0},
#                             "E 450(Fe 570)D": {"MT": 0.0, "kg": 0.0},
#                         }
#                     }
#                 }
#             },
#             "Cross beams/diaphragms": {
#                 "materials": {
#                     "Concrete": {
#                         "units": ["cum", "kg"],
#                         "sub_materials": {
#                             "M25": {"cum": 0.0, "kg": 0.0},
#                             "M30": {"cum": 0.0, "kg": 0.0},
#                             "M35": {"cum": 0.0, "kg": 0.0},
#                             "M40": {"cum": 0.0, "kg": 0.0},
#                         }
#                     },
#                     "Steel": {
#                         "units": ["MT", "kg"],
#                         "sub_materials": {
#                             "E 250(Fe 410W)A": {"MT": 0.0, "kg": 0.0},
#                             "E 250(Fe 410W)B": {"MT": 0.0, "kg": 0.0},
#                             "E 300(Fe 440)": {"MT": 0.0, "kg": 0.0},
#                         }
#                     }
#                 }
#             },
#             "Deck slab": {
#                 "materials": {
#                     "Concrete": {
#                         "units": ["cum", "kg"],
#                         "sub_materials": {
#                             "M30": {"cum": 0.0, "kg": 0.0},
#                             "M35": {"cum": 0.0, "kg": 0.0},
#                             "M40": {"cum": 0.0, "kg": 0.0},
#                         }
#                     },
#                     "Steel": {
#                         "units": ["MT", "kg"],
#                         "sub_materials": {
#                             "E 250(Fe 410W)A": {"MT": 0.0, "kg": 0.0},
#                             "E 250(Fe 410W)B": {"MT": 0.0, "kg": 0.0},
#                             "E 300(Fe 440)": {"MT": 0.0, "kg": 0.0},
#                         }
#                     }
#                 }
#             },
#             "Cantilever slab": {
#                 "materials": {
#                     "Concrete": {
#                         "units": ["cum", "kg"],
#                         "sub_materials": {
#                             "M25": {"cum": 0.0, "kg": 0.0},
#                             "M30": {"cum": 0.0, "kg": 0.0},
#                             "M35": {"cum": 0.0, "kg": 0.0},
#                         }
#                     },
#                     "Steel": {
#                         "units": ["MT", "kg"],
#                         "sub_materials": {
#                             "E 250(Fe 410W)A": {"MT": 0.0, "kg": 0.0},
#                             "E 250(Fe 410W)B": {"MT": 0.0, "kg": 0.0},
#                         }
#                     }
#                 }
#             },
#             "Joints": {
#                 "materials": {
#                     "Steel": {
#                         "units": ["MT", "kg"],
#                         "sub_materials": {
#                             "E 300(Fe 440)": {"MT": 0.0, "kg": 0.0},
#                             "E 350(Fe 490)": {"MT": 0.0, "kg": 0.0},
#                         }
#                     }
#                 }
#             }
#         }
#     },
#     "miscellaneous": {
#         "components": {
#             "Wearing surface": {
#                 "materials": {
#                     "mastic asphalt": {
#                         "units": ["sqm"],
#                         "sub_materials": {
#                             "standard": {"sqm": 0.0}
#                         }
#                     }
#                 }
#             },
#             "Footpaths": {
#                 "materials": {
#                     "Concrete": {
#                         "units": ["cum", "kg"],
#                         "sub_materials": {
#                             "M15": {"cum": 0.0, "kg": 0.0},
#                             "M20": {"cum": 0.0, "kg": 0.0},
#                         }
#                     },
#                     "paver blocks": {
#                         "units": ["sqm"],
#                         "sub_materials": {
#                             "standard": {"sqm": 0.0}
#                         }
#                     }
#                 }
#             },
#             "Expansion joints": {
#                 "materials": {
#                     "Steel": {
#                         "units": ["MT", "kg"],
#                         "sub_materials": {
#                             "E 250(Fe 410W)A": {"MT": 0.0, "kg": 0.0},
#                             "E 300(Fe 440)": {"MT": 0.0, "kg": 0.0},
#                         }
#                     }
#                 }
#             },
#             "Painting system": {
#                 "materials": {
#                     "paint": {
#                         "units": ["ltr"],
#                         "sub_materials": {
#                             "white/yellow": {"ltr": 0.0},
#                             "primer_epoxy": {"ltr": 0.0},
#                             "oil": {"ltr": 0.0},
#                             "alluminium": {"ltr": 0.0}
#                         }
#                     }
#                 }
#             },
#             "Bearings": {
#                 "materials": {
#                     "Steel": {
#                         "units": ["MT", "kg"],
#                         "sub_materials": {
#                             "E 350(Fe 490)": {"MT": 0.0, "kg": 0.0},
#                             "E 410(Fe 540)": {"MT": 0.0, "kg": 0.0},
#                         }
#                     }
#                 }
#             }
#         }
#     }
# }


# def get_material_cost_template():
#     return copy.deepcopy(MATERIAL_COSTS_TEMPLATE)


# # Get all form names
# def get_forms():
#     return list(MATERIAL_COSTS_TEMPLATE.keys())


# # Get components for a specific form
# def get_components(form_name):
#     form_data = MATERIAL_COSTS_TEMPLATE.get(form_name, {})
#     return list(form_data.get("components", {}).keys())


# # Get materials for a specific form and component
# def get_materials(form_name, component_name):
#     form_data = MATERIAL_COSTS_TEMPLATE.get(form_name, {})
#     component_data = form_data.get("components", {}).get(component_name, {})
#     return list(component_data.get("materials", {}).keys())


# # Get sub-materials (grades) for a specific material
# def get_sub_materials(form_name, component_name, material_name):
#     form_data = MATERIAL_COSTS_TEMPLATE.get(form_name, {})
#     component_data = form_data.get("components", {}).get(component_name, {})
#     material_data = component_data.get("materials", {}).get(material_name, {})
#     return list(material_data.get("sub_materials", {}).keys())


# # Get units for a specific material
# def get_units(form_name, component_name, material_name):
#     form_data = MATERIAL_COSTS_TEMPLATE.get(form_name, {})
#     component_data = form_data.get("components", {}).get(component_name, {})
#     material_data = component_data.get("materials", {}).get(material_name, {})
#     return material_data.get("units", [])


# # Get cost for specific material, sub-material, and unit
# def get_material_cost(form_name, component_name, material_name, sub_material_name, unit):
#     form_data = MATERIAL_COSTS_TEMPLATE.get(form_name, {})
#     component_data = form_data.get("components", {}).get(component_name, {})
#     material_data = component_data.get("materials", {}).get(material_name, {})
#     sub_material_data = material_data.get("sub_materials", {}).get(sub_material_name, {})
#     return sub_material_data.get(unit, None)


# # Set cost for specific material, sub-material, and unit
# def set_material_cost(form_name, component_name, material_name, sub_material_name, unit, cost):
#     try:
#         form_data = MATERIAL_COSTS_TEMPLATE.get(form_name, {})
#         component_data = form_data.get("components", {}).get(component_name, {})
#         material_data = component_data.get("materials", {}).get(material_name, {})
#         sub_material_data = material_data.get("sub_materials", {}).get(sub_material_name, {})
        
#         if unit in sub_material_data:
#             sub_material_data[unit] = cost
#             return True
#         return False
#     except (KeyError, AttributeError):
#         return False


# # Validation helpers
# def is_valid_form(form_name):
#     return form_name in MATERIAL_COSTS_TEMPLATE


# def is_valid_component(form_name, component_name):
#     return component_name in MATERIAL_COSTS_TEMPLATE.get(form_name, {}).get("components", {})


# def is_valid_material(form_name, component_name, material_name):
#     form_data = MATERIAL_COSTS_TEMPLATE.get(form_name, {})
#     component_data = form_data.get("components", {}).get(component_name, {})
#     return material_name in component_data.get("materials", {})


# def is_valid_sub_material(form_name, component_name, material_name, sub_material_name):
#     form_data = MATERIAL_COSTS_TEMPLATE.get(form_name, {})
#     component_data = form_data.get("components", {}).get(component_name, {})
#     material_data = component_data.get("materials", {}).get(material_name, {})
#     return sub_material_name in material_data.get("sub_materials", {})


# def is_valid_unit(form_name, component_name, material_name, unit):
#     form_data = MATERIAL_COSTS_TEMPLATE.get(form_name, {})
#     component_data = form_data.get("components", {}).get(component_name, {})
#     material_data = component_data.get("materials", {}).get(material_name, {})
#     return unit in material_data.get("units", [])
# ----------------------------------------------------------------------------------------------------------------
# import copy

# # Base template for material costs (independent of components)
# MATERIAL_COSTS_TEMPLATE = {
#     "concrete": {
#         "units": ["cum", "kg"],
#         "grades": {
#             "M15": {"cum": 0.0, "kg": 0.0},
#             "M20": {"cum": 0.0, "kg": 0.0},
#             "M25": {"cum": 0.0, "kg": 0.0},
#             "M30": {"cum": 0.0, "kg": 0.0},
#             "M35": {"cum": 0.0, "kg": 0.0},
#             "M40": {"cum": 0.0, "kg": 0.0},
#             "M45": {"cum": 0.0, "kg": 0.0},
#             "M50": {"cum": 0.0, "kg": 0.0},
#         }
#     },
#     "steel": {
#         "units": ["MT", "kg"],
#         "grades": {
#             "E 165(Fe 290)": {"MT": 0.0, "kg": 0.0},
#             "E 250(Fe 410W)A": {"MT": 0.0, "kg": 0.0},
#             "E 250(Fe 410W)B": {"MT": 0.0, "kg": 0.0},
#             "E 250(Fe 410)C": {"MT": 0.0, "kg": 0.0},
#             "E 300(Fe 440)": {"MT": 0.0, "kg": 0.0},
#             "E 350(Fe 490)": {"MT": 0.0, "kg": 0.0},
#             "E 410(Fe 540)": {"MT": 0.0, "kg": 0.0},
#             "E 450(Fe 570)D": {"MT": 0.0, "kg": 0.0},
#         }
#     },
#     "mastic asphalt": {
#         "units": ["sqm"],
#         "grades": {
#             "standard": {"sqm": 0.0}
#         }
#     },
#     "paint": {
#         "units": ["ltr"],
#         "grades": {
#             "white/yellow": {"ltr": 0.0},
#             "primer_epoxy": {"ltr": 0.0},
#             "oil": {"ltr": 0.0},
#             "alluminium": {"ltr": 0.0}
#         }
#     },
#     "paver blocks": {
#         "units": ["sqm"],
#         "grades": {
#             "standard": {"sqm": 0.0}
#         }
#     },
#     "prestressing tendons": {
#         "units": ["MT", "kg"],
#         "grades": {
#             "E 165(Fe 290)": {"MT": 0.0, "kg": 0.0},
#             "E 250(Fe 410W)A": {"MT": 0.0, "kg": 0.0},
#             "E 250(Fe 410W)B": {"MT": 0.0, "kg": 0.0},
#             "E 250(Fe 410)C": {"MT": 0.0, "kg": 0.0},
#             "E 300(Fe 440)": {"MT": 0.0, "kg": 0.0},
#             "E 350(Fe 490)": {"MT": 0.0, "kg": 0.0},
#             "E 410(Fe 540)": {"MT": 0.0, "kg": 0.0},
#             "E 450(Fe 570)D": {"MT": 0.0, "kg": 0.0},
#         }
#     },
   
# }

# # Form-specific components (extracted from your backend data)
# FORM_COMPONENTS = {
#     "foundation": [
#         "Pile",
#         "Pile Cap"
#     ],
#     "sub-structure": [
#         "Abutment",
#         "Abutment protection works",
#         "Pier",
#         "Pier cap"
#     ],
#     "super-structure": [
#         "Girders/Main beams",
#         "Cross beams/diaphragms",
#         "Deck slab",
#         "Cantilever slab",
#         "Joints"
#     ],
#     "miscellaneous": [
#         "Wearing surface",
#         "Footpaths",
#         "Expansion joints",
#         "Painting system",
#         "Bearings"
#     ]
# }

# def get_material_cost_template():
#     return copy.deepcopy(MATERIAL_COSTS_TEMPLATE)

# def get_materials(material_costs=None):
#     """Get all available materials (independent of components)"""
#     if material_costs is None:
#         material_costs = MATERIAL_COSTS_TEMPLATE
#     return list(material_costs.keys())

# def get_grades(material_costs, material):
#     """Get all grades for a specific material"""
#     return list(material_costs.get(material, {}).get("grades", {}).keys())

# def get_units(material_costs, material):
#     """Get all units for a specific material"""
#     return material_costs.get(material, {}).get("units", [])

# def get_material_cost(material_costs, material, grade, unit):
#     """Get cost for a specific material, grade, and unit"""
#     return material_costs.get(material, {}).get("grades", {}).get(grade, {}).get(unit, None)

# def set_material_cost(material_costs, material, grade, unit, cost):
#     """Set cost for a specific material, grade, and unit"""
#     grades = material_costs.get(material, {}).get("grades", {})
#     if grade in grades and unit in grades[grade]:
#         grades[grade][unit] = cost
#         return True
#     return False

# # Component-related functions
# def get_forms():
#     """Get all available forms"""
#     return list(FORM_COMPONENTS.keys())

# def get_components(form_name):
#     """Get components for a specific form"""
#     return FORM_COMPONENTS.get(form_name, [])

# def get_sub_materials(form_name, component_name, material_name):
#     """Get sub-materials (grades) for a material - independent of form/component"""
#     return get_grades(MATERIAL_COSTS_TEMPLATE, material_name)

# def get_units_for_material(form_name, component_name, material_name):
#     """Get units for a material - independent of form/component"""
#     return get_units(MATERIAL_COSTS_TEMPLATE, material_name)

# # Validation helpers 
# def is_valid_material(material_costs, material):
#     """Check if material exists"""
#     return material in material_costs

# def is_valid_grade(material_costs, material, grade):
#     """Check if grade exists for material"""
#     return grade in material_costs.get(material, {}).get("grades", {})

# def is_valid_unit(material_costs, material, unit):
#     """Check if unit exists for material"""
#     return unit in material_costs.get(material, {}).get("units", [])

# def is_valid_form(form_name):
#     """Check if form exists"""
#     return form_name in FORM_COMPONENTS

# def is_valid_component(form_name, component_name):
#     """Check if component exists for form"""
#     return component_name in FORM_COMPONENTS.get(form_name, [])

# def is_valid_material_for_form_component(form_name, component_name, material_name):
#     """Check if material is valid (materials are independent of form/component)"""
#     return material_name in MATERIAL_COSTS_TEMPLATE

# # Get all (material, grade, unit) combinations
# def get_all_material_unit_combinations(material_costs):
#     """Get all possible material, grade, unit combinations"""
#     combinations = []
#     for material, data in material_costs.items():
#         for grade, units in data.get("grades", {}).items():
#             for unit in units:
#                 combinations.append((material, grade, unit))
#     return combinations

# # Road User Cost Components (unchanged)
# VEHICLE_TYPES = [
#     "Small Cars",
#     "Big Cars",
#     "Two Wheelers",
#     "Buses",
#     "LCV",
#     "HCV",
#     "MCV"
# ]

# LANE_TYPES = [
#     "Single Lane Roads",
#     "Intermediate Lane Roads",
#     "Two Lane Roads",
#     "Four Lane Divided Roads",
#     "Four Lane Divided Expressways Roads"
# ]

# ROUGHNESS_VALUES = [2000, 3000, 4000, 5000, 6000, 7000, 8000]

# RF_VALUES = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

# def get_vehicle_types():
#     return VEHICLE_TYPES

# def get_lane_types():
#     return LANE_TYPES

# def get_roughness_values():
#     return ROUGHNESS_VALUES

# def get_rf_values():
#     return RF_VALUES

import copy

# Base template for material costs (independent of components)
MATERIAL_COSTS_TEMPLATE = {
    "Steel Rebar": {
        "units": ["MT", "Kg", "Cum", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "Fe415": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Fe500": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Fe550": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Other": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Reinforced Cement Concrete": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "M10": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M15": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M20": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M25": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M30": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M35": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M40": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M45": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M50": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M55": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M60": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M65": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M70": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M75": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M80": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M85": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M90": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M95": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M100": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Other": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Pre-Stressed Cement Concrete": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "M10": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M15": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M20": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M25": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M30": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M35": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M40": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M45": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M50": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M55": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M60": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M65": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M70": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M75": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M80": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M85": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M90": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M95": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "M100": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Other": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    # Excavation materials - NO GRADES
    "Rock": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "N/A": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Soft Rock": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "N/A": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Medium Soil": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "N/A": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Clay": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "N/A": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Marshy Soil": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "N/A": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Soft Murrum": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "N/A": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Loam": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "N/A": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Stiff Clay": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "N/A": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Gravel": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "N/A": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Hard Laterite": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "N/A": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Marine Clay": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "N/A": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Paint": {
        "units": ["Ltr", "Cum", "Kg", "MT", "RMT", "Sqm", "Lumpsum"],
        "grades": {
            "Epoxy": {"Ltr": 0.0, "Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Lumpsum": 0.0},
            "Oil Paint": {"Ltr": 0.0, "Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Lumpsum": 0.0},
            "Primer": {"Ltr": 0.0, "Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Lumpsum": 0.0},
            "Anti-Corrosive Paint": {"Ltr": 0.0, "Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Lumpsum": 0.0},
            "Other": {"Ltr": 0.0, "Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Lumpsum": 0.0},
        }
    },
    "Structural Steel": {
        "units": ["MT", "Kg", "Cum", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "E250": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "E350": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "E410": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "E450": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Other": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Steel Anchor Rods": {
        "units": ["MT", "Kg", "Cum", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "E250": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "E350": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "E410": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "E450": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Other": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Tendons": {
        "units": ["MT", "Kg", "Cum", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "Standard": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Other": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Shear Connectors": {
        "units": ["MT", "Kg", "Cum", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "E250": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "E350": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "E410": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "E450": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Other": {"MT": 0.0, "Kg": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Rubber": {
        "units": ["Kg", "MT", "Cum", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "Standard": {"Kg": 0.0, "MT": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Other": {"Kg": 0.0, "MT": 0.0, "Cum": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "PVC": {
        "units": ["RMT", "Kg", "MT", "Cum", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "Standard": {"RMT": 0.0, "Kg": 0.0, "MT": 0.0, "Cum": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Other": {"RMT": 0.0, "Kg": 0.0, "MT": 0.0, "Cum": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "FRP": {
        "units": ["Sqm", "Kg", "MT", "Cum", "RMT", "Ltr", "Lumpsum"],
        "grades": {
            "Standard": {"Sqm": 0.0, "Kg": 0.0, "MT": 0.0, "Cum": 0.0, "RMT": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Other": {"Sqm": 0.0, "Kg": 0.0, "MT": 0.0, "Cum": 0.0, "RMT": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Asphalt": {
        "units": ["Sqm", "Cum", "Kg", "MT", "RMT", "Ltr", "Lumpsum"],
        "grades": {
            "Standard": {"Sqm": 0.0, "Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Other": {"Sqm": 0.0, "Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Waterproofing": {
        "units": ["Sqm", "Cum", "Kg", "MT", "RMT", "Ltr", "Lumpsum"],
        "grades": {
            "Standard": {"Sqm": 0.0, "Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
            "Other": {"Sqm": 0.0, "Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    },
    "Other": {
        "units": ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"],
        "grades": {
            "Standard": {"Cum": 0.0, "Kg": 0.0, "MT": 0.0, "RMT": 0.0, "Sqm": 0.0, "Ltr": 0.0, "Lumpsum": 0.0},
        }
    }
}

# Form-specific components with their applicable materials
FORM_COMPONENTS = {
    "Foundation": {
        "Pile": ["Steel Rebar", "Reinforced Cement Concrete", "Other"],
        "Excavation": ["Rock", "Soft Rock", "Medium Soil", "Clay", "Marshy Soil", "Soft Murrum", 
                       "Loam", "Stiff Clay", "Gravel", "Hard Laterite", "Marine Clay", "Other"],
        "Pile Cap": ["Steel Rebar", "Reinforced Cement Concrete", "Other"],
    },
    "Sub-Structure": {
        "Pier": ["Steel Rebar", "Reinforced Cement Concrete", "Paint", "Other"],
        "Pier Cap": ["Steel Rebar", "Reinforced Cement Concrete", "Paint", "Steel Anchor Rods", "Other"],
        "Pedestal": ["Steel Rebar", "Reinforced Cement Concrete", "Paint", "Other"],
        "Bearing": ["Structural Steel", "Rubber", "Other"],
    },
    "Super-Structure": {
        "Girder": ["Steel Rebar", "Reinforced Cement Concrete", "Pre-Stressed Cement Concrete", 
                   "Tendons", "Structural Steel", "Shear Connectors", "Paint", "Other"],
        "Deck Slab": ["Steel Rebar", "Reinforced Cement Concrete", "Other"],
        "Diaphragm": ["Steel Rebar", "Reinforced Cement Concrete", "Structural Steel", "Paint", "Other"],
        "Cross Bracings": ["Structural Steel", "Steel Rebar", "Paint", "Other"],
    },
    "Miscellaneous": {
        "Bearings": ["Structural Steel", "Rubber", "Other"],
        "Railing & Crash Barrier": ["Reinforced Cement Concrete", "Structural Steel", "Steel Rebar", "Paint", "Other"],
        "Drainage": ["PVC", "Reinforced Cement Concrete", "Structural Steel", "FRP", "Other"],
        "Asphalt & Utilities": ["Asphalt", "Paint", "Other"],
        "Waterproofing": ["Waterproofing", "Other"],
    }
}

# Standard units available across all materials
STANDARD_UNITS = ["Cum", "Kg", "MT", "RMT", "Sqm", "Ltr", "Lumpsum"]

def get_material_cost_template():
    """Get a deep copy of the material costs template"""
    return copy.deepcopy(MATERIAL_COSTS_TEMPLATE)

def get_materials(material_costs=None):
    """Get all available materials (independent of components)"""
    if material_costs is None:
        material_costs = MATERIAL_COSTS_TEMPLATE
    return list(material_costs.keys())

def get_grades(material_costs, material):
    """Get all grades for a specific material"""
    return list(material_costs.get(material, {}).get("grades", {}).keys())

def get_units(material_costs, material):
    """Get all units for a specific material"""
    return material_costs.get(material, {}).get("units", [])

def get_standard_units():
    """Get standard units available for all materials"""
    return STANDARD_UNITS

def get_material_cost(material_costs, material, grade, unit):
    """Get cost for a specific material, grade, and unit"""
    return material_costs.get(material, {}).get("grades", {}).get(grade, {}).get(unit, None)

def set_material_cost(material_costs, material, grade, unit, cost):
    """Set cost for a specific material, grade, and unit"""
    grades = material_costs.get(material, {}).get("grades", {})
    if grade in grades and unit in grades[grade]:
        grades[grade][unit] = cost
        return True
    return False

def has_grades(material_costs, material):
    """Check if a material has actual grades (not just N/A)"""
    grades = material_costs.get(material, {}).get("grades", {})
    if len(grades) == 1 and "N/A" in grades:
        return False
    return True

def add_custom_material(material_costs, material_name, grades_list=None, units_list=None):
    """Add a new custom material to the material costs"""
    if material_name in material_costs:
        return False  # Material already exists
    
    if grades_list is None:
        grades_list = ["Standard", "Other"]
    if units_list is None:
        units_list = STANDARD_UNITS
    
    grades_dict = {}
    for grade in grades_list:
        grade_units = {unit: 0.0 for unit in units_list}
        grades_dict[grade] = grade_units
    
    material_costs[material_name] = {
        "units": units_list,
        "grades": grades_dict
    }
    return True

def add_custom_grade(material_costs, material, grade_name):
    """Add a new grade to an existing material"""
    if material not in material_costs:
        return False
    
    if grade_name in material_costs[material]["grades"]:
        return False  # Grade already exists
    
    units = material_costs[material]["units"]
    material_costs[material]["grades"][grade_name] = {unit: 0.0 for unit in units}
    return True

def add_custom_unit(material_costs, material, unit_name):
    """Add a new unit to an existing material"""
    if material not in material_costs:
        return False
    
    if unit_name in material_costs[material]["units"]:
        return False  # Unit already exists
    
    material_costs[material]["units"].append(unit_name)
    
    # Add this unit to all existing grades
    for grade in material_costs[material]["grades"]:
        material_costs[material]["grades"][grade][unit_name] = 0.0
    
    return True

# Component-related functions
def get_forms():
    """Get all available forms"""
    return list(FORM_COMPONENTS.keys())

def get_components(form_name):
    """Get components for a specific form"""
    return list(FORM_COMPONENTS.get(form_name, {}).keys())

def get_component_materials(form_name, component_name):
    """Get materials applicable for a specific component"""
    form_data = FORM_COMPONENTS.get(form_name, {})
    return form_data.get(component_name, [])

def add_custom_component(form_name, component_name, materials_list=None):
    """Add a new component to a form"""
    if form_name not in FORM_COMPONENTS:
        return False
    
    if component_name in FORM_COMPONENTS[form_name]:
        return False  # Component already exists
    
    if materials_list is None:
        materials_list = []
    
    FORM_COMPONENTS[form_name][component_name] = materials_list
    return True

def get_sub_materials(form_name, component_name, material_name):
    """Get sub-materials (grades) for a material - independent of form/component"""
    return get_grades(MATERIAL_COSTS_TEMPLATE, material_name)

def get_units_for_material(form_name, component_name, material_name):
    """Get units for a material - independent of form/component"""
    return get_units(MATERIAL_COSTS_TEMPLATE, material_name)

# Validation helpers 
def is_valid_material(material_costs, material):
    """Check if material exists"""
    return material in material_costs

def is_valid_grade(material_costs, material, grade):
    """Check if grade exists for material"""
    return grade in material_costs.get(material, {}).get("grades", {})

def is_valid_unit(material_costs, material, unit):
    """Check if unit exists for material"""
    return unit in material_costs.get(material, {}).get("units", [])

def is_valid_form(form_name):
    """Check if form exists"""
    return form_name in FORM_COMPONENTS

def is_valid_component(form_name, component_name):
    """Check if component exists for form"""
    return component_name in FORM_COMPONENTS.get(form_name, {})

def is_valid_material_for_form_component(form_name, component_name, material_name):
    """Check if material is valid for a specific component"""
    component_materials = get_component_materials(form_name, component_name)
    return material_name in component_materials or material_name == "Other"

# Get all (material, grade, unit) combinations
def get_all_material_unit_combinations(material_costs):
    """Get all possible material, grade, unit combinations"""
    combinations = []
    for material, data in material_costs.items():
        for grade, units in data.get("grades", {}).items():
            for unit in units:
                combinations.append((material, grade, unit))
    return combinations

# Road User Cost Components (unchanged)
VEHICLE_TYPES = [
    "Small Cars",
    "Big Cars",
    "Two Wheelers",
    "Buses",
    "LCV",
    "HCV",
    "MCV"
]

LANE_TYPES = [
    "Single Lane Roads",
    "Intermediate Lane Roads",
    "Two Lane Roads",
    "Four Lane Divided Roads",
    "Four Lane Divided Expressways Roads"
]

ROUGHNESS_VALUES = [2000, 3000, 4000, 5000, 6000, 7000, 8000]

RF_VALUES = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

def get_vehicle_types():
    return VEHICLE_TYPES

def get_lane_types():
    return LANE_TYPES

def get_roughness_values():
    return ROUGHNESS_VALUES

def get_rf_values():
    return RF_VALUES