from typing import TypedDict, Tuple


class VehicleInput(TypedDict):
    vehicle_type: str
    carriageway_width: float
    rg_roughness_factor: float
    fl_fall_factor: float
    rs_rise_factor: float
    lane_type: str
    rf_rise_and_fall_factor: float
    power_weight_ratio_pwr: float | None


def extract_vehicle_inputs(vehicle_input: VehicleInput) -> Tuple[
    str, float, float, float, float, str, float
]:
    """
    Extracts common vehicle input fields.

    Returns:
        vt   - vehicle type
        W    - carriageway width
        RG   - roughness factor
        FL   - fall factor
        RS   - rise factor
        lane - lane type
        RF   - rise and fall factor
    """
    vt: str = vehicle_input["vehicle_type"]
    W: float = vehicle_input["carriageway_width"]
    RG: float = vehicle_input["rg_roughness_factor"]
    FL: float = vehicle_input["fl_fall_factor"]
    RS: float = vehicle_input["rs_rise_factor"]
    lane: str = vehicle_input["lane_type"]
    RF: float = vehicle_input["rf_rise_and_fall_factor"]

    return vt, W, RG, FL, RS, lane, RF
