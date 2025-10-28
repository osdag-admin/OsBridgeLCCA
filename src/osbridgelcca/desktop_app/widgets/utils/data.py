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

KEY_GRADE = "grade"
KEY_TYPE = "type"
KEY_QUANTITY = "quantity"
KEY_UNIT_M3 = "unit_m3"
KEY_RATE = "rate"
KEY_RATE_DATA_SOURCE = "rate_data_source"
KEY_COMPONENT = "component"
KEY_UNITS = "units"
KEY_OPTIONS = "options"


KEY_LANES = "lanes"
KEY_ROADROUGHNESS = "road_roughness"
KEY_ROAD_RISE_AND_FALL = "road_rise_and_fall"
KEY_TYPE_OF_ROAD = "type_of_road"
KEY_ANNUAL_INCREASE = "annual_increase"


construction_materials = {
    KEY_FOUNDATION: {
        "Pile": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            }
        },
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
        "Pile Cap": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            }
        }
    },
    
    KEY_SUBSTRUCTURE: {
        "Pier": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Paint": {
                KEY_GRADE: ["Epoxy", "Oil Paint", "Primer"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            }
        },
        "Pier Cap": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Paint": {
                KEY_GRADE: ["Epoxy", "Oil Paint", "Primer"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Steel Anchor Rods": {
                KEY_GRADE: ["E250", "E350"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            }
        }
    },
    
    KEY_SUPERSTRUCTURE: {
        "Girder": {
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Reinforced Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Pre-stressed Cement Concrete": {
                KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                          "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Tendons": {
                KEY_GRADE: [],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Structural Steel": {
                KEY_GRADE: ["E250", "E350"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
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
            KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
        },
        "Reinforced Cement Concrete": {
            KEY_GRADE: ["M10", "M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50", 
                      "M55", "M60", "M65", "M70", "M75", "M80", "M85", "M90", "M95", "M100"],
            KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
        }
    }

  },
    
    KEY_AUXILIARY: {
        "Bearings": {
            "Structural Steel": {
                KEY_GRADE: ["E250", "E350"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
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
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Structural Steel": {
                KEY_GRADE: ["E250", "E350"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Steel Rebar": {
                KEY_GRADE: ["Fe415", "Fe500", "Fe550"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
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
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
            },
            "Structural Steel": {
                KEY_GRADE: ["E250", "E350"],
                KEY_UNITS: ["cum", "kg", "MT", "rmt", "sqm", "ltr"]
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
                "Single Lane",
                "Intermediate Lane",
                "Two Lane",
                "Three Lane",
                "Four Lane Divided Roads",
                "Four Lane Divided Expressway"
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
                "Rural Road",
                "Highway",
                "Expressway"
            ],
            
        },
        KEY_ANNUAL_INCREASE: {
            KEY_OPTIONS: ["8", "9", "10", "12"],
       
       },
    }   

}