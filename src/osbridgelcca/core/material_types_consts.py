import copy

# Base template for material costs
MATERIAL_COSTS_TEMPLATE = {
    "concrete": {
        "units": ["cum", "kg"],
        "grades": {
            "M15": {"cum": 0.0, "kg": 0.0},
            "M20": {"cum": 0.0, "kg": 0.0},
            "M25": {"cum": 0.0, "kg": 0.0},
            "M30": {"cum": 0.0, "kg": 0.0},
            "M35": {"cum": 0.0, "kg": 0.0},
            "M40": {"cum": 0.0, "kg": 0.0},
            "M45": {"cum": 0.0, "kg": 0.0},
            "M50": {"cum": 0.0, "kg": 0.0},
        }
    },
    "steel": {
        "units": ["MT", "kg"],
        "grades": {
            "E 165(Fe 290)": {"MT": 0.0, "kg": 0.0},
            "E 250(Fe 410W)A": {"MT": 0.0, "kg": 0.0},
            "E 250(Fe 410W)B": {"MT": 0.0, "kg": 0.0},
            "E 250(Fe 410)C": {"MT": 0.0, "kg": 0.0},
            "E 300(Fe 440)": {"MT": 0.0, "kg": 0.0},
            "E 350(Fe 490)": {"MT": 0.0, "kg": 0.0},
            "E 410(Fe 540)": {"MT": 0.0, "kg": 0.0},
            "E 450(Fe 570)D": {"MT": 0.0, "kg": 0.0},
        }
    },
    "mastic asphalt": {
        "units": ["sqm"],
        "grades": {
            "default": {"sqm": 0.0}
        }
    },
    "paint": {
        "units": ["ltr"],
        "grades": {
            "white/yellow": {"ltr": 0.0},
            "primer_epoxy": {"ltr": 0.0},
            "oil": {"ltr": 0.0},
            "alluminium": {"ltr": 0.0}
        }
    },
    "paver blocks": {
        "units": ["sqm"],
        "grades": {
            "default": {"sqm": 0.0}
        }
    },
    "prestressing tendons": {
        "units": ["MT", "kg"],
        "grades": {
            "E 165(Fe 290)": {"MT": 0.0, "kg": 0.0},
            "E 250(Fe 410W)A": {"MT": 0.0, "kg": 0.0},
            "E 250(Fe 410W)B": {"MT": 0.0, "kg": 0.0},
            "E 250(Fe 410)C": {"MT": 0.0, "kg": 0.0},
            "E 300(Fe 440)": {"MT": 0.0, "kg": 0.0},
            "E 350(Fe 490)": {"MT": 0.0, "kg": 0.0},
            "E 410(Fe 540)": {"MT": 0.0, "kg": 0.0},
            "E 450(Fe 570)D": {"MT": 0.0, "kg": 0.0},
        }
    },
    "other": {
        "units": ["MT", "kg", "cum", "sqm", "ltr"],  # All supported units
        "grades": {
            "default": {unit: 0.0 for unit in ["MT", "kg", "cum", "sqm", "ltr"]}
        }
    },
}


def get_material_cost_template():
    return copy.deepcopy(MATERIAL_COSTS_TEMPLATE)


def get_materials(material_costs):
    return list(material_costs.keys())

def get_grades(material_costs, material):
    return list(material_costs.get(material, {}).get("grades", {}).keys())

def get_units(material_costs, material):
    return material_costs.get(material, {}).get("units", [])

def get_material_cost(material_costs, material, grade, unit):
    return material_costs.get(material, {}).get("grades", {}).get(grade, {}).get(unit, None)

# returns True on success, False if invalid keys
def set_material_cost(material_costs, material, grade, unit, cost):
    grades = material_costs.get(material, {}).get("grades", {})
    if grade in grades and unit in grades[grade]:
        grades[grade][unit] = cost
        return True
    return False

# Validation helpers 
def is_valid_material(material_costs, material):
    return material in material_costs

def is_valid_grade(material_costs, material, grade):
    return grade in material_costs.get(material, {}).get("grades", {})

def is_valid_unit(material_costs, material, unit):
    return unit in material_costs.get(material, {}).get("units", [])

# returns all (material, grade, unit) combinations
def get_all_material_unit_combinations(material_costs):
    combinations = []
    for material, data in material_costs.items():
        for grade, units in data.get("grades", {}).items():
            for unit in units:
                combinations.append((material, grade, unit))
    return combinations


# Road User Cost Components
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
