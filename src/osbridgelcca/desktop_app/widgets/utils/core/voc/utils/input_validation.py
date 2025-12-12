from utils import carriage_way_standards
from utils import constants

def validate_input(vehicle_input):
    errors = []

    # -----------------------------
    # Validate lane_type using carriagewayStandards
    # -----------------------------
    available_types, _ = carriage_way_standards.CarriagewayStandards.list_types()
    lane_type = vehicle_input.get("lane_type")

    if not isinstance(lane_type, str):
        errors.append("lane_type must be a string.")
    else:
        if lane_type not in available_types:
            errors.append(
                f"lane_type '{lane_type}' is invalid. Allowed: {available_types}"
            )

    # -----------------------------
    # Validate carriageway width logic
    # -----------------------------
    if lane_type == "EW":
        custom_width = vehicle_input.get("carriageway_width")
        if custom_width is None or not isinstance(custom_width, (int, float)) or custom_width <= 0:
            errors.append(
                "For Expressway type, 'carriageway_width' must be a positive number (custom width required)."
            )
    else:
        standard_width, msg = carriage_way_standards.CarriagewayStandards.get_width(lane_type)
        if standard_width is None:
            errors.append(f"Could not retrieve standard width: {msg}")
        else:
            vehicle_input["carriageway_width"] = standard_width

    # -----------------------------
    # Validate numeric fields
    # -----------------------------
    numeric_fields = [
        "rg_roughness_factor",
        "fl_fall_factor",
        "rs_rise_factor"
    ]

    for field in numeric_fields:
        value = vehicle_input.get(field)
        if not isinstance(value, (int, float)):
            errors.append(f"{field} must be a number (int or float).")

    # -----------------------------
    # Validate vehicle_info
    # -----------------------------
    vehicle_info = vehicle_input.get("vehicle_info")
    if not isinstance(vehicle_info, dict):
        errors.append("vehicle_info must be a dictionary.")
    else:
        missing_keys = [vtype for vtype in constants.vehicle_type_list if vtype not in vehicle_info]
        if missing_keys:
            errors.append(
                f"Missing vehicle types in vehicle_info: {missing_keys}. All must be present."
            )

        invalid_keys = [vtype for vtype in vehicle_info if vtype not in constants.vehicle_type_list]
        if invalid_keys:
            errors.append(
                f"Invalid vehicle types in vehicle_info: {invalid_keys}. Allowed: {constants.vehicle_type_list}"
            )

        for vtype, count in vehicle_info.items():
            if not isinstance(count, (int, float)) or count < 0:
                errors.append(f"Count for '{vtype}' must be a non-negative number.")

        # -----------------------------
        # Validate power_weight_ratio_pwr for HCV, MCV
        # -----------------------------
        mcv_count = vehicle_info.get("mcv", 0)
        hcv_count = vehicle_info.get("hcv", 0)

    if mcv_count > 0 or hcv_count > 0:
        pwr = vehicle_input.get("power_weight_ratio_pwr")
        if pwr is None:
            errors.append(
                "power_weight_ratio_pwr must be provided if LCV, HCV, or MCV count > 0."
            )
        elif isinstance(pwr, dict):
            # Check all relevant vehicle types have a numeric value > 0
            for vt in ["mcv", "hcv"]:
                if vehicle_info.get(vt, 0) > 0:
                    if vt not in pwr or not isinstance(pwr[vt], (int, float)) or pwr[vt] <= 0:
                        errors.append(
                            f"power_weight_ratio_pwr for '{vt}' is required, must be a numeric value greater than 0, but the provided value is {value}."
                        )
        elif not isinstance(pwr, (int, float)) or pwr <= 0:
            errors.append(
                f"power_weight_ratio_pwr must be numeric (int/float) and > 0, or a dictionary keyed by vehicle type with values > 0."
            )


    # -----------------------------
    # Return or raise errors
    # -----------------------------
    if errors:
        raise ValueError("\n".join(errors))

    return True