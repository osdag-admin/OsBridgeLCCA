# cost_defaults.py
"""
Default constants for cost and environmental calculations in LCCA.
"""

# Carbon emission factors for common construction materials
CARBON_EMISSION_FACTORS = {
    "Structural Steel": 2.5,
    "Rebar": 2.6,
    "Concrete (M25)": 0.084,
}

def get_carbon_emission_factor(material_name):
    """
    Returns the carbon emission factor for a given material name.
    :param material_name: str
    :return: float or None if not found
    """
    return CARBON_EMISSION_FACTORS.get(material_name)

# GHG Global Warming Potential (GWP) equivalency factors
GHG_EQUIVALENCY_FACTORS = {
    "Carbon Dioxide (CO2)": 1,
    "Methane (CH4)": 25,
    "Nitrogen Trifluoride (NF3)": 17200,
}

def get_ghg_equivalency_factor(ghg_name):
    """
    Returns the GWP equivalency factor for a given greenhouse gas name.
    :param ghg_name: str
    :return: int or None if not found
    """
    return GHG_EQUIVALENCY_FACTORS.get(ghg_name)

# Environmental and economic coefficients
COEFFICIENT_CARBON_EMISSIONS_CONCRETE = 0.0840  # kgCO2e/kg
CARBON_EMISSION_FACTOR_PER_KM = 0.1213  # kgCO2e/km
SOCIAL_COST_OF_CARBON = 6.3936  # INR/kg
COEFFICIENT_EMBODIED_ENERGY_HYSD_STEEL = 30  # MJ/kg
COEFFICIENT_CARBON_EMISSIONS_STRUCTURAL_STEEL = 2.6000  # kgCO2e/kg

def get_coefficient_carbon_emissions_concrete():
    return COEFFICIENT_CARBON_EMISSIONS_CONCRETE

def get_carbon_emission_factor_per_km():
    return CARBON_EMISSION_FACTOR_PER_KM

def get_social_cost_of_carbon():
    return SOCIAL_COST_OF_CARBON

def get_coefficient_embodied_energy_hysd_steel():
    return COEFFICIENT_EMBODIED_ENERGY_HYSD_STEEL

def get_coefficient_carbon_emissions_structural_steel():
    return COEFFICIENT_CARBON_EMISSIONS_STRUCTURAL_STEEL

# Maintenance, inspection, and repair cost rates and frequencies

PERIODIC_MAINTENANCE_COST_RATE = 0.0055  # 0.55% as a decimal
ANNUAL_ROUTINE_INSPECTION_COST_RATE = 0.01  # 1% as a decimal
REPAIR_AND_REHABILITATION_COST_RATE = 0.10  # 10% as a decimal
PERIODIC_MAINTENANCE_FREQUENCY_YEARS = 5
ROUTINE_INSPECTION_FREQUENCY_YEARS = 1

def get_periodic_maintenance_cost_rate():
    return PERIODIC_MAINTENANCE_COST_RATE

def get_annual_routine_inspection_cost_rate():
    return ANNUAL_ROUTINE_INSPECTION_COST_RATE

def get_repair_and_rehabilitation_cost_rate():
    return REPAIR_AND_REHABILITATION_COST_RATE

def get_periodic_maintenance_frequency_years():
    return PERIODIC_MAINTENANCE_FREQUENCY_YEARS

def get_routine_inspection_frequency_years():
    return ROUTINE_INSPECTION_FREQUENCY_YEARS

# Demolition and recycling recommended values
DEMOLITION_COST_RATE = 0.10  # 10% as a decimal
SCRAP_VALUE_STRUCTURAL_STEEL = 50000  # INR/MT
STRUCTURAL_STEEL_SCRAP_RATE = 0.98  # 98% as a decimal

def get_demolition_cost_rate():
    return DEMOLITION_COST_RATE

def get_scrap_value_structural_steel():
    return SCRAP_VALUE_STRUCTURAL_STEEL

def get_structural_steel_scrap_rate():
    return STRUCTURAL_STEEL_SCRAP_RATE

