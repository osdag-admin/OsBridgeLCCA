from .voc import core
from .voc.congestion import core as congestion_core

vc = 0.8854
wpi = {'year': 2024,
       'WPI': {
           'fuelCost': {
               'Petrol': 1.8067915690866512, 
               'Diesel': 1.7733050847457628, 
               'Engine Oil': 1.4496951219512195, 
               'Other Oil': 1.6951351351351354, 
               'Grease': 1.6951351351351354
               },
           'vehicleCost': {
               'propertyDamage': {
                   'Small Cars': 1.1395759717314486, 
                   'Big Cars': 1.1395759717314486, 
                   'Two Wheeler': 1.1395759717314486, 
                   'Ordinary Buses': 1.1395759717314486, 
                   'Deluxe Buses': 1.1395759717314486, 
                   'LCV': 1.1395759717314486, 
                   'HCV': 1.1395759717314486, 
                   'MCV': 1.1395759717314486
                   },
               'tyreCost': {
                   'Small Cars': 1.123991935483871, 
                   'Big Cars': 1.123991935483871, 
                   'Two Wheeler': 1.1336538461538461, 
                   'Ordinary Buses': 1.1702564102564101, 
                   'Deluxe Buses': 1.1702564102564101, 
                   'LCV': 1.1702564102564101, 
                   'HCV': 1.1702564102564101, 
                   'MCV': 1.1702564102564101
                   },
               'spareParts': {
                   'Small Cars': 1.1395759717314486, 
                   'Big Cars': 1.1395759717314486, 
                   'Two Wheeler': 1.1395759717314486, 
                   'Ordinary Buses': 1.1395759717314486, 
                   'Deluxe Buses': 1.1395759717314486, 
                   'LCV': 1.1395759717314486, 
                   'HCV': 1.1395759717314486, 
                   'MCV': 1.1395759717314486
                   },
               'fixedDepreciation': {
                   'Small Cars': 1.1388400702987698, 
                   'Big Cars': 1.1388400702987698, 
                   'Two Wheeler': 1.1388400702987698, 
                   'Ordinary Buses': 1.1388400702987698, 
                   'Deluxe Buses': 1.1388400702987698, 
                   'LCV': 1.1388400702987698, 
                   'HCV': 1.1388400702987698, 
                   'MCV': 1.1388400702987698
                   }
           },
           'commodityHoldingCost': {
               'Small Cars': 1.4788593903638152, 
               'Big Cars': 1.4788593903638152, 
               'Two Wheeler': 1.4788593903638152, 
               'Ordinary Buses': 1.4788593903638152, 
               'Deluxe Buses': 1.4788593903638152, 
               'LCV': 1.4788593903638152, 
               'HCV': 1.4788593903638152, 
               'MCV': 1.4788593903638152
               },
           'passengerCrewCost': {
               'Passenger Cost': 1.2706270627062706, 
               'Crew Cost': 1.2706270627062706
               }, 
            'medicalCost': {
                'Fatal': 1.0867924528301887, 
                'Major Injury': 1.0867924528301887, 
                'Minor Injury': 1.0867924528301887
            }, 
            'votCost': {
                'Small Cars': 1.2706270627062706, 
                'Big Cars': 1.2706270627062706, 
                'Two Wheeler': 1.2706270627062706, 
                'Ordinary Buses': 1.2706270627062706, 
                'Deluxe Buses': 1.2706270627062706, 
                'LCV': 1.2706270627062706, 
                'HCV': 1.2706270627062706, 
                'MCV': 1.2706270627062706
                }
            }
        }

vehicle_input = {
    "vehicle_info": {
        "small_cars": 3943,
        "big_cars": 2397,
        "two_wheelers": 12505,
        "buses": 329,
        "lcv": 271,
        "hcv": 0,
        "mcv": 1
    },
    # "carriageway_width": 10, ### ONLY REQUIRED WHEN "lane_type" = "EW"
    "rg_roughness_factor": 2000,
    "fl_fall_factor": 0,
    "rs_rise_factor": 0,
    "lane_type": "2L",
    "power_weight_ratio_pwr": {
        "mcv": 8,
        "hcv": 7.22
    }
}

def calc_voc(inputs: dict,
             all_wpi: dict,
             vehicle_cost: float) -> dict:
    """
    return calculate_total_adjusted_costs
    """
    val = core.main(inputs, all_wpi)
    return congestion_core.calculate_total_adjusted_costs(val, vehicle_cost, vehicle_input)