vehicle_type_list = ["small_cars", "big_cars",
                     "two_wheelers", "buses", "lcv", "hcv", "mcv"]

petrolToDieselRatio = {
    "small_cars": {
        "petrol": 0.7,
        "diesel": 0.3
    },
    "big_cars": {
        "petrol": 0.3,
        "diesel": 0.7
    },
    "two_wheelers": {
        "petrol": 1,
        "diesel": 0
    },
    "buses": {
        "petrol": 0,
        "diesel": 1
    },
    "lcv": {
        "petrol": 0,
        "diesel": 1
    },
    "hcv": {
        "petrol": 0,
        "diesel": 1
    },
    "mcv": {
        "petrol": 0,
        "diesel": 1
    },
}


pcu = {
    "small_cars": 1, 
    "big_cars": 1, 
    "two_wheelers": 0.75, 
    "buses": 2.2, 
    "lcv": 1.4, 
    "hcv": 2.2, 
    "mcv": 2.2
}