from voc.utils import carriage_way_standards

def validate(a, vc, lane_type, vehicle_input, debug=False):
    errors = []

    # -----------------------------
    # Validate 'a'
    # -----------------------------
    if not isinstance(a, dict):
        errors.append("'a' must be a dictionary.")
    else:
        for key in ['distanceCost', 'timeCost']:
            if key not in a:
                errors.append(f"'a' must contain '{key}' key.")
            elif not isinstance(a[key], dict):
                errors.append(f"'{key}' in 'a' must be a dictionary.")
            else:
                # Check totals
                if 'total' not in a[key]:
                    errors.append(f"'{key}' must contain 'total' breakdown.")
                # Check units
                if 'units' not in a[key]:
                    errors.append(f"'{key}' must contain 'units' key.")

    # -----------------------------
    # Validate 'vc'
    # -----------------------------
    if not isinstance(vc, (int, float)) or vc < 0:
        errors.append(f"'vc' must be a non-negative number. Provided: {vc}")

    # -----------------------------
    # Validate 'lane_type'
    # -----------------------------
    if not isinstance(lane_type, str):
        errors.append(f"'lane_type' must be a string. Provided: {lane_type}")
    else:
        available_types, _ = carriage_way_standards.CarriagewayStandards.list_types()
        if lane_type not in available_types:
            errors.append(f"'lane_type' must be one of {available_types}. Provided: {lane_type}")

    # -----------------------------
    # Validate 'vehicle_input'
    # -----------------------------
    if not isinstance(vehicle_input, dict):
        errors.append("'vehicle_input' must be a dictionary.")
    else:
        vehicle_info = vehicle_input.get("vehicle_info")
        if not isinstance(vehicle_info, dict):
            errors.append("'vehicle_input' must contain 'vehicle_info' dictionary.")
        else:
            # Check vehicle counts are non-negative numbers
            for vt, count in vehicle_info.items():
                if not isinstance(count, (int, float)) or count < 0:
                    errors.append(f"Vehicle count for '{vt}' must be non-negative number. Provided: {count}")

        # Check power_weight_ratio_pwr if present
        pwr = vehicle_input.get("power_weight_ratio_pwr")
        if pwr is not None:
            if isinstance(pwr, dict):
                for vt, val in pwr.items():
                    if not isinstance(val, (int, float)) or val <= 0:
                        errors.append(f"power_weight_ratio_pwr for '{vt}' must be > 0. Provided: {val}")
            elif not isinstance(pwr, (int, float)) or pwr <= 0:
                errors.append(f"power_weight_ratio_pwr must be numeric and > 0. Provided: {pwr}")

        # Check carriageway_width
        width = vehicle_input.get("carriageway_width")
        if width is None or not isinstance(width, (int, float)) or width <= 0:
            errors.append(f"'carriageway_width' must be positive number. Provided: {width}")

    # -----------------------------
    # Validate 'debug'
    # -----------------------------
    if not isinstance(debug, bool):
        errors.append(f"'debug' must be a boolean. Provided: {debug}")

    # -----------------------------
    # Raise error if any validation fails
    # -----------------------------
    if errors:
        raise ValueError("\n".join(errors))

    return True
