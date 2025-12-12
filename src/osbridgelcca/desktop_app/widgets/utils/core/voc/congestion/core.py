import voc.congestion.formulas as cf
import voc.congestion.input_validation as validate

def calculate_total_adjusted_costs(a, vc, vehicle_input, debug=False):
    """
    Calculate total adjusted costs (distance + time) with congestion factors applied.
    Parameters:
    a (dict): Base cost data containing 'distanceCost' and 'timeCost'.
    vc (float): Volume-to-capacity ratio.
    lane_type (str): Type of lane (e.g., "SL", "IL", "2L", "4L", "6L").
    vehicle_input (dict): Vehicle input data containing vehicle counts.
    debug (bool): If True, includes detailed breakdown of calculations.
    """
    lane_type =  vehicle_input["lane_type"]
    validate.validate(a, vc, lane_type, vehicle_input, debug)

    cv = {
        "distance_congestion_factors": cf.distance_congestion_factors(lane_type, vc=vc),
        "time_congestion_factors": cf.time_congestion_factors(lane_type, vc=vc)
    }

    total_distance_cost = {'IT': 0, 'ET': 0}
    total_time_cost = {'IT': 0, 'ET': 0}

    breakdown = {}  # NEW dictionary for detailed debugging

    vehicles = set(a['distanceCost'].keys()) & set(a['timeCost'].keys())
    vehicles -= {'units', 'total'}

    for vehicle in vehicles:

        veh_count = vehicle_input["vehicle_info"].get(vehicle, 0)

        # Base costs
        distance_it = a['distanceCost'][vehicle]['IT']
        distance_et = a['distanceCost'][vehicle]['ET']
        time_it = a['timeCost'][vehicle]['IT']
        time_et = a['timeCost'][vehicle]['ET']

        # Factors
        cd = cv['distance_congestion_factors'].get(vehicle, 1)
        ct = cv['time_congestion_factors'].get(vehicle, 1)
        # pcu_factor = pcu.get(vehicle, 1)

        # Adjusted costs per vehicle
        adj_distance_it = distance_it * cd
        adj_distance_et = distance_et * cd
        adj_time_it = time_it * ct
        adj_time_et = time_et * ct

        # Total cost including volume
        total_distance_cost['IT'] += adj_distance_it * veh_count
        total_distance_cost['ET'] += adj_distance_et * veh_count
        total_time_cost['IT'] += adj_time_it * veh_count
        total_time_cost['ET'] += adj_time_et * veh_count

        if debug:
            # Save detailed breakdown
            breakdown[vehicle] = {
                "vehicle_count": veh_count,
                "factors": {
                    "distance_congestion_factor": cd,
                    "time_congestion_factor": ct,
                },
                "base_costs": {
                    "distance": {"IT": distance_it, "ET": distance_et},
                    "time": {"IT": time_it, "ET": time_et}
                },
                "adjusted_costs_per_vehicle": {
                    "distance": {"IT": adj_distance_it, "ET": adj_distance_et},
                    "time": {"IT": adj_time_it, "ET": adj_time_et}
                },
                "total_adjusted_costs": {
                    "distance": {
                        "IT": adj_distance_it * veh_count,
                        "ET": adj_distance_et * veh_count
                    },
                    "time": {
                        "IT": adj_time_it * veh_count,
                        "ET": adj_time_et * veh_count
                    }
                },
                "total": {   # <-- NEW FIELD
                    "IT": (adj_distance_it * veh_count) + (adj_time_it * veh_count),
                    "ET": (adj_distance_et * veh_count) + (adj_time_et * veh_count)
                }
            }

    result = {
        "distance_total": total_distance_cost,
        "time_total": total_time_cost,
        "total": {
            "IT": total_distance_cost["IT"] + total_time_cost["IT"],
            "ET": total_distance_cost["ET"] + total_time_cost["ET"]
        },
        "unit": "Rs/km"
    }

    if debug:
        result["breakdown"] = breakdown

    return result
