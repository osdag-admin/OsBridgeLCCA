# WPI Calculation
BASE_YEAR = 2019
KEY_PASSENGER_COST = "Passenger Cost"
KEY_CREW_COST = "Crew Cost"

# Keys for database
TABLE_WPI_MEDICAL = "wpi_medical_accessories"
TABLE_VOT = "wpi_vot"
COL_ACCIDENT_CATEGORY = "Category_of_Accident"
COL_COST_INR = "Economic_Cost_INR"
COL_TYPE_OF_VEHICLE = "Type_of_Vehicle"
COL_YEAR = "Year"

KEY_SINGLE_LANE_ROAD = "Single Lane Roads"
KEY_INTERMEDIATE_LANE_ROAD = "Intermediate Lane Roads"
KEY_TWO_LANE_ROAD = "Two Lane Roads"
KEY_FOUR_LANE_DIVIDED_ROAD = "Four Lane Divided Roads"
KEY_SIX_LANE_DIVIDED_ROAD = "Six Lane Divided Roads"
KEY_FOUR_LANE_DIVIDED_EXPRESSWAY = "Four Lane Divided Expressways"
KEY_SIX_LANE_DIVIDED_EXPRESSWAY = "Six Lane Divided Expressways"
KEY_EIGHT_LANE_DIVIDED_URBAN_EXPRESSWAY = "Eight Lane Divided Urban Expressways"
COL_OCCUPANCY = "Occupancy"

# Keys for All Type of Tabs
KEY_STRUCTURE_WORKS_DATA = "Structure Works Data"
KEY_FOUNDATION = "Foundation"
KEY_SUBSTRUCTURE = "Sub-Structure"
KEY_SUPERSTRUCTURE = "Super-Structure"
KEY_AUXILIARY = "Miscellaneous"
KEY_FINANCIAL = "Financial Data"
KEY_CARBON_EMISSION = "Carbon Emission Data"
KEY_CARBON_EMISSION_COST = "Carbon Emission Cost Data"
KEY_BRIDGE_TRAFFIC = "Bridge and Traffic Data"
KEY_MAINTAINANCE_REPAIR = "Maintenance and Repair"
KEY_DEMOLITION_RECYCLE = "Demolition and Recycling"

# Keys for structural works data
KEY_GRADE = "grade"
KEY_TYPE = "type"
KEY_QUANTITY = "quantity"
KEY_UNIT_M3 = "unit_m3"
KEY_RATE = "rate"
KEY_RATE_DATA_SOURCE = "rate_data_source"
KEY_COMPONENT = "component"
KEY_UNITS = "units"
KEY_OPTIONS = "options"

# Keys for Financial Widget
KEY_DISCOUNT_RATE_IA = "Discount Rate(Inflation Adjusted)"
KEY_INTEREST_RATE = "Interest Rate"
KEY_INFLATION_RATE = "Inflation Rate"
KEY_INVESTMENT_RATIO = "Investment Ratio"
KEY_DESIGN_LIFE = "Design Life"
KEY_CONSTR_TIME = "Time for Construction of Base Project"
KEY_ANALYSIS_PERIOD = "Analysis Period"

# Key Bridge and Traffic
KEY_TWO_WHEELER = "Two Wheeler"
KEY_SMALL_CARS = "Small Cars"
KEY_BIG_CARS = "Big Cars"
KEY_ORDINARY_BUS = "Ordinary Buses"
KEY_DELUXE_BUS = "Deluxe Buses"
KEY_LCV = "LCV"
KEY_HCV = "HCV"
KEY_MCV = "MCV"
KEY_MINOR_INJURY = "Minor Injury"
KEY_MAJOR_INJURY = "Major Injury"
KEY_FATAL = "Fatal"

KEY_PETROL = "Petrol"
KEY_DIESEL = "Diesel"
KEY_ENGINE_OIL = "Engine Oil"
KEY_OTHER_OIL = "Other Oil"
KEY_GREASE = "Grease"

KEY_LANES = "lanes"
KEY_ROADROUGHNESS = "road_roughness"
KEY_ROAD_RISE_AND_FALL = "road_rise_and_fall"
KEY_TYPE_OF_ROAD = "type_of_road"
KEY_ACCIDENT_CAT = "annual_increase"

# Key Carbon Emission
KEY_EMBODIED_CARBON_ENERGY = "embodied_carbon_energy"
KEY_CARBON_EMISSION_FACTOR = "carbon_emission_factor"

# Result Dictionary
COST_TOTAL_INIT_CONST = "Total Initial Construction Cost"
COST_TOTAL_SUPERSTRUCTURE = "Total SuperStructure Cost"
COST_TOTAL_INIT_CARBON_EMISSION = "Total Initial Carbon Emission Cost"
COST_TIME = "Time Cost"
COST_CARBON_EMISSION_REROUTING_INIT = "Carbon Emission due to Rerouting during Initial Construction"
COST_TOTAL_ROAD_USER = "Total Road User Cost"
COST_ADDITIONAL_CARBON_EMISSION = "Additional Carbon Emission Cost"
COST_PERIODIC_MAINTAINANCE = "Periodic Maintenance Cost"
COST_MAJOR_INSPECTION = "Major Inspection Cost"
COST_MAJOR_REPAIR = "Major Repair Cost"
COST_PERIODIC_MAINTAINANCE_CARBON_EMISSION = "Periodic Maintenance Carbon Emission Cost"
COST_MAJOR_REPAIR_RELATED_CARBON_EMISSION = "Major Repair Related Carbon Emisson Cost"
COST_CARBON_EMISSION_RR_DURING_MAJOR_REPAIR = "Carbon Emission due to rerouting during Major Repairs"
COST_CARBON_EMISSION_RR_DURING_REPLACEMENT = "Carbon Emission due to rerouting during Replacement"
COST_DEMOLITION_DISPOSAL_CARBON = "Demolition and Disposal related Carbon Emission"
COST_DEMOLITION_DISPOSAL_CARBON_REROUTING = "Carbon Emission due to Rerouting during Demolition and Disposal"
COST_TOTAL_ROUTINE_INSPECTION = "Total Routine Inspection Cost"
COST_REPAIR_REHAB = "Repair and Rehabilitation Cost"
COST_DEMOLITION_DISPOSAL = "Demolition and Disposal Cost"
COST_RECYCLING = "Recycling Cost"
COST_RECONSTRUCTION = "Reconstruction Cost"

# Keys for Carbon Emission Cost Data
KEY_SCC = "Social Cost of Carbon"
KEY_SOURCE = "Source"
KEY_USD_T_INR = "USD to INR Conversion Factor"
SCC_NITI_Aayog = "NITI Aayog"
SCC_K_Ricke_et_al = "Social Cost of Carbon (K.Ricke et. al.)"
SCC_CUSTOM = "Custom"
KEY_SCC_OPTIONS = [SCC_NITI_Aayog, SCC_K_Ricke_et_al, SCC_CUSTOM]
SCC_SSP = "Shared Socioeconomic Pathway(SSP)"
SCC_RCP = "Representative Concentration Pathway(RCP)"
SCC_CLIMATE = "Climate"
SCC_RUN = "Run"
SCC_K_Ricke_OPTIONS = [SCC_SSP, SCC_RCP, SCC_CLIMATE, SCC_RUN, "USD to INR Conversion"]
SCC_SSP_OPTIONS = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]
SCC_RCP_OPTIONS = ["RCP4.5", "RCP6.0", "RCP8.5"]
SSC_CLIMATE_OPTIONS = ["Expected", "Uncertain"]
SCC_RUN_OPTIONS = ["bhm_lr", "bhm_richpoor_lr", "bhm_richpoor_sr", "bhm_sr", "djo"]

# Maintainance and Repair
KEY_ROUTINE_INSP_COST = "Routine Inspection Cost Rate"
KEY_ROUTINE_INSP_FREQ = "Routine Inspection Frequency"

KEY_PERIODIC_MAINT_COST = "Routine Maintainance Cost"
KEY_PERIODIC_MAINT_FREQ = "Routine Maintainance Frequency"

KEY_MAJOR_INSP_COST = "Major Inspection Cost"
KEY_MAJOR_INSP_FREQ = "Major Inspection Frequency"
KEY_MAJOR_REPAIR_COST = "Major Repair Cost"
KEY_MAJOR_REPAIR_FREQ = "Major Repair Frequency"

KEY_BEARING_EXP_JOINT_REPAIR_COST = "Repair cost of bearing and expansion joints"
KEY_BEARING_EXP_JOINT_REPAIR_FREQ = "Frequency of Repair cost of bearing and expansion joints"

# Demolition and Disposal
KEY_DEMOLITION_DISPOSAL_COST = "Demolition and Disposal Cost"
KEY_STRUCT_STEEL_SCRAP_RATE = "Structural Steel Scrap Rate"
KEY_STRUCT_STEEL_RECYLABILITY = "Structural Steel Recylability"
KEY_STEEL_REBAR_SCRAP_RATE = "Steel Rebar Scrap Rate"
KEY_STEEL_REBAR_RECYLABILITY = "Steel Rebar Recylability"
KEY_PS_TENDONS_SCRAP_RATE = "Pre Stressed Tendons Scrap Rate"
KEY_PS_TENDONS_RECYLABILITY = "Pre Stressed Tendons Recylability"

# Bridge and Traffic Data
KEY_ALTER_ROAD_CARRIAGEWAY = "Alternate Road Carriageway"
KEY_ADDIT_REROUTING_DISTANCE = "Additional Rerouting Distance"
KEY_ADDIT_TRAVEL_TIME = "Additonal Travel Time"
KEY_ROAD_ROUGHNESS = "Road Roughness"
KEY_ROAD_RISE = "Road Rise"
KEY_ROAD_FALL = "Road Fall"
KEY_ROAD_TYPE = "Type of Road"
KEY_CRASH_RATE = "Crash Rate"


construction_materials = {
    KEY_FOUNDATION: {
        "Excavation": {
            "Rock": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
                },
            "Soft Rock": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
                },
            "Medium Soil": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
                },
            "Clay": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
                },
            "Marshy Soil": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
                },
            "Soft Murrum": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
                },
            "Loam": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
                },
            "Stiff Clay": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
                },
            "Gravel": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
                },
            "Hard Laterite": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
                },
            "Marine Clay": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
                },
            "Other": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
                },
        },
        "Pile": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["kg", "MT"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg"]
            }
        },
        "Pile Cap": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["kg", "MT"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg"]
            }
        }        
    },
    
    KEY_SUBSTRUCTURE: {
        "Pier": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["kg", "MT"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg"]
            },
            "Paint": {
                KEY_GRADE: ["Epoxy", "Oil Paint", "Primer"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            }
        },
        "Pier Cap": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["kg", "MT"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg"]
            },
            "Paint": {
                KEY_GRADE: ["Epoxy", "Oil Paint", "Primer"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Steel Anchor Rods": {
                KEY_GRADE: ["E250", "E350"],
                KEY_UNITS: ["kg", "MT"]
            }
        },
        "Pedestal": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["kg", "MT"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg"]
            }
        },
        "Bearing": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["kg", "MT"]
            }
        }
    },
    
    KEY_SUPERSTRUCTURE: {
        "Girder": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["kg", "MT"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg"]
            },
            "Pre-stressed Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg"]
            },
            "Tendons": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Structural Steel": {
                KEY_GRADE: ["E250", "E350"],
                KEY_UNITS: ["kg", "MT"]
            },
            "Shear Connectors": {
                KEY_GRADE: ["E250", "E350"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Paint": {
                KEY_GRADE: ["Epoxy", "Oil Paint", "Primer", "Anti-Corrosive Paint"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            }
        },
        "Deck Slab": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["kg", "MT"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                        "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg"]
            }
        },
        "Diaphragm": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["kg", "MT"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg"]
            }
        },
        "Cross Bracings": {
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg"]
            }
        }
  },
    
    KEY_AUXILIARY: {
        "Bearings": {
            "Structural Steel": {
                KEY_GRADE: ["E250", "E350"],
                KEY_UNITS: ["kg", "MT"]
            },
            "Rubber": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            }
        },
        "Railing & Crash Barrier": {
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg"]
            },
            "Structural Steel": {
                KEY_GRADE: ["E250", "E350"],
                KEY_UNITS: ["kg", "MT"]
            },
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["kg", "MT"]
            },
            "Paint": {
                KEY_GRADE: ["Epoxy", "Oil Paint", "Primer", "Anti-Corrosive Paint"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            }
        },
        "Drainage": {
            "PVC": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg"]
            },
            "Structural Steel": {
                KEY_GRADE: ["E250", "E350"],
                KEY_UNITS: ["kg", "MT"]
            },
            "FRP": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            }
        },
        "Asphalt & Utilities": {
            "Asphalt": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Paint": {
                KEY_GRADE: ["Epoxy", "Oil Paint", "Primer", "Anti-Corrosive Paint"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            }
        },
        "Waterproofing": {
            KEY_GRADE: [],
            KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
        }
    }

}



bridge_traffic_data = {
    KEY_BRIDGE_TRAFFIC: {
        KEY_LANES: {
            KEY_OPTIONS: [
                KEY_SINGLE_LANE_ROAD,
                KEY_INTERMEDIATE_LANE_ROAD,
                KEY_TWO_LANE_ROAD,
                KEY_FOUR_LANE_DIVIDED_ROAD,
                KEY_SIX_LANE_DIVIDED_ROAD,
                KEY_FOUR_LANE_DIVIDED_EXPRESSWAY,
                KEY_SIX_LANE_DIVIDED_EXPRESSWAY,
                KEY_EIGHT_LANE_DIVIDED_URBAN_EXPRESSWAY
            ],
           
        },
        
        KEY_ROADROUGHNESS: {
            KEY_OPTIONS: ["2000", "3000", "4000", "5000", "6000", "7000", "8000", "9000", "10000"],
            
        },
        
        KEY_ROAD_RISE_AND_FALL: {
            KEY_OPTIONS: ["0", "5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60", "65", "70", "75", "80", "85", "90", "95", "100"],
            
        },
        
        KEY_TYPE_OF_ROAD: {
            KEY_OPTIONS: [
                "Urban Road",
                "Rural Road"
            ],
            
        },
        KEY_ACCIDENT_CAT: {
            KEY_OPTIONS: ["Minor Injury", "Major Injury", "Fatal"],
       
       },
    }   

}