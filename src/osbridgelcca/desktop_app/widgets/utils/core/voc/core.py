from .utils.input_validation import validate_input
from .vehicle_types import big_cars, buses, hcv, lcv, mcv, small_cars, two_wheeler
from .utils import post_processor as pp
import sys

# Map vehicle_info keys to their model modules
MODEL_MAP = {
    "big_cars": big_cars,
    "small_cars": small_cars,
    "two_wheelers": two_wheeler,
    "buses": buses,
    "hcv": hcv,
    "lcv": lcv,
    "mcv": mcv,
}

def main(vehicle_input, wpi, debug = False):
    """
    Validates input and executes the correct vehicle models for all vehicles with count > 0.
    Adapts input to match the old format expected by model_module.test().

    Parameters:
    vehicle_input (dict): Input data containing vehicle counts and other parameters.
    wpi (dict): Wholesale Price Index data for cost adjustments.
    debug (bool): If True, includes detailed breakdown of calculations. Files generated in the `debug` folder.
    """

    # --------------------
    # 1. Validate input
    # --------------------

    # --------------------
    # 1. Validate input
    # --------------------
    try:
        validate_input(vehicle_input)
    except ValueError as e:
        print("Input validation failed:\n", str(e))
        sys.exit(1)  # Terminate the program with an error code


    # --------------------
    # 2. Vehicle model execution
    # --------------------
    vehicle_info = vehicle_input.get("vehicle_info", {})
    results = {}

    for vt, count in vehicle_info.items():
        if count > 0:
            model_module = MODEL_MAP.get(vt)
            if model_module is None:
                results[vt] = {"status": "error",
                            "message": f"No model available for '{vt}'."}
            else:
                # Keep input_for_model same structure as before
                input_for_model = {
                    **{k: v for k, v in vehicle_input.items() if k != "vehicle_info"},
                    "vehicle_type": vt,
                    "rf_rise_and_fall_factor": vehicle_input.get("fl_fall_factor", 0)
                                            + vehicle_input.get("rs_rise_factor", 0)
                }

                # Adapt power_weight_ratio_pwr if it's a dict
                if isinstance(vehicle_input.get("power_weight_ratio_pwr"), dict):
                    input_for_model["power_weight_ratio_pwr"] = vehicle_input["power_weight_ratio_pwr"].get(vt, 0)

                results[vt] = model_module.compute_voc(input_for_model)
                summaryOfVOC = pp.post_process(results, wpi, debug)

    return summaryOfVOC
