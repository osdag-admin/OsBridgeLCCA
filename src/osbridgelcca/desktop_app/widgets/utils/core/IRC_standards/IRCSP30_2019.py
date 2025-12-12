# IRC SP-30:2019, Table C.1 Current Vehicle Operating Cost Inputs

vehicle_costs = {
    "two_wheelers": {"ET": 34209, "IT": 61235},
    "small_cars": {"ET": 273728, "IT": 489972},
    "big_cars": {"ET": 558599, "IT": 999892},
    "buses": {"ET": 1647150, "IT": 2948400},
    "lcv": {"ET": 449721, "IT": 805000},
    "hcv": {"ET": 940531, "IT": 1683550},
    "mcv": {"ET": 1415350, "IT": 1415350},
}

petroleum_products_costs = {
    "petrol": {
        "ET": 33.58,
        "IT": 79.92,
        "units": "Rs/l"
    },
    "diesel": {
        "ET": 30.51,
        "IT": 72.61,
        "units": "Rs/l"
    },
    "engine_oil": {
        "ET": 187.96,
        "IT": 384.39,
        "units": "Rs/l"
    },
    "other_oil": {
        "ET": 167.70,
        "IT": 338.78,
        "units": "Rs/l"
    },
    "grease": {
        "ET": 183.70,
        "IT": 390.90,
        "units": "Rs/kg"
    }
}

new_tyres_costs = {
    "two_wheelers": {
        "ET": 1355,
        "IT": 1668,
        "units": "Rs/unit",
        "num_of_wheels": 2  # Source "Steel - reconstruction, inflation included" sheets
    },
    "big_cars": {
        "ET": 2940,
        "IT": 4456,
        "units": "Rs/unit",
        "num_of_wheels": 4  # Source "Steel - reconstruction, inflation included" sheets
    },
    "small_cars": {
        "ET": 2940,
        "IT": 4456,
        "units": "Rs/unit",
        "num_of_wheels": 4  # Source "Steel - reconstruction, inflation included" sheets
    },
    "buses": {
        "ET": 13475,
        "IT": 17500,
        "units": "Rs/unit",
        "num_of_wheels": 6  # Source "Steel - reconstruction, inflation included" sheets
    },
    "lcv": {
        "ET": 5420,
        "IT": 8900,
        "units": "Rs/unit",
        "num_of_wheels": 6  # Source "Steel - reconstruction, inflation included" sheets
    },
    "hcv": {
        "ET": 13890,
        "IT": 20000,
        "units": "Rs/unit",
        "num_of_wheels": 10  # Source "Steel - reconstruction, inflation included" sheets
    },
    "mcv": {
        "ET": 13890,
        "IT": 20000,
        "units": "Rs/unit",
        "num_of_wheels": 14  # Source "Steel - reconstruction, inflation included" sheets
    }
}
