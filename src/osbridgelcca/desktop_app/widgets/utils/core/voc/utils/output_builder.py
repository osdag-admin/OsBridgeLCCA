from typing import Dict, Any

def build_voc_output(
    vt: str,
    lane: str,
    velocity: float,
    petrol: float,
    diesel: float,
    SP_ET: float,
    SP_IT: float,
    ML: float,
    TL: float,
    EOL: float,
    OL: float,
    G: float,
    FXC_ET: float,
    FXC_IT: float,
    DC_ET: float,
    DC_IT: float,
    PT: float,
    crew: float,
    CHC: float,
    UPD: float
) -> Dict[str, Any]:
 
    def nn(x):
        # Helper to ensure non-negative values
        return max(x, 0)
    
    return {
        "vehicle_type": vt,
        "lane_type": lane,
        "velocity": {
            "value": nn(velocity),
            "unit": "kmph"
        },
        "VOC_summary": {
            "distance_related": {
                "fuel_consumption": {
                    "petrol": nn(petrol),
                    "diesel": nn(diesel),
                    "unit": "liters per 1000 km",
                    "iHTC": False
                },
                "spare_parts": {
                    "ET": nn(SP_ET)/100,
                    "IT": nn(SP_IT)/100,
                    "unit": "Rs/km",
                    "iHTC": True
                },
                "maintenance_labour": {
                    "value": nn(ML)/100,
                    "unit": "Rs/km",
                    "iHTC": False
                },
                "tyre_life": {
                    "value": nn(TL),
                    "unit": "km/tyre",
                    "iHTC": False
                },
                "engine_oil": {
                    "value": nn(EOL),
                    "unit": "liters per 1000 km",
                    "iHTC": False
                },
                "other_oil": {
                    "value": nn(OL),
                    "unit": "liters per 10000 km",
                    "iHTC": False
                },
                "grease": {
                    "value": nn(G),
                    "unit": "liters per 10000 km",
                    "iHTC": False
                },
            },

            "time_related": {
                "fixed_cost": {
                    "ET": nn(FXC_ET),
                    "IT": nn(FXC_IT),
                    "unit": "Rs/km",
                    "iHTC": True
                },
                "depreciation_cost": {
                    "ET": nn(DC_ET),
                    "IT": nn(DC_IT),
                    "unit": "Rs/km",
                    "iHTC": True
                },
                "passenger_time_cost": {
                    "value": nn(PT),
                    "unit": "Rs/km",
                    "iHTC": False
                },
                "crew_cost": {
                    "value": nn(crew),
                    "unit": "Rs/km",
                    "iHTC": False
                },
                "commodity_holding_cost": {
                    "value": nn(CHC),
                    "unit": "Rs/km",
                    "iHTC": False
                },
            },

            "utilisation": {
                "value": nn(UPD),
                "iHTC": False
            },
            "note": "All Values mentioned here are without WPI adjustments!"
        }
    }
