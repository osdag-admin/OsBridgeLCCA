from typing import Dict, Any, TypedDict
import IRC_standards.IRCSP30_2019
from voc.utils.output_builder import build_voc_output
from voc.utils.pre_processor import VehicleInput, extract_vehicle_inputs
import math

Vehicle = "mcv"


def compute_voc(vehicle_input: VehicleInput) -> Dict[str, Any]:
    vt, W, RG, FL, RS, lane, RF = extract_vehicle_inputs(vehicle_input)
    NP: Dict[str, int] = IRC_standards.IRCSP30_2019.vehicle_costs[Vehicle]

    pwr = vehicle_input["power_weight_ratio_pwr"]
    if pwr == None:
        raise ValueError(
            "Power to weight ratio (pwr) must be provided for HCV vehicles.")
    
    if vt == Vehicle:
        # -----------------------------
        # SPEED FORMULA
        # -----------------------------
        speed_map: Dict[str, float] = {
            'SL': 38.27 - 0.3412 * RF - 0.00068 * (RG - 2000),
            'IL': 42.01 - 0.3753 * RF - 0.00074 * (RG - 2000),
            '2L': 44.79 - 0.3994 * RF - 0.00079 * (RG - 2000),
            '4L': 74.16 - 0.6405 * RF - 0.00128 * RG,
            '6L': 76.60 - 0.6405 * RF - 0.00128 * RG,
            '8L': 79.03 - 0.6405 * RF - 0.00128 * RG,
            'EW': 69.29 - 0.6405 * RF - 0.00128 * RG + 0.696 * W
        }

        V: float = speed_map.get(lane, 0.0)

        # -----------------------------
        # DISTANCE RELATED
        # -----------------------------

        # Fuel consumption
        petrol: float = 0
        diesel: float = 90 + (14489.919 / V) + 0.0216 * (V ** 2) + 0.01 * RG + 8.217 * RS - 8.8272 * FL - 13.113 * (pwr)

        # Spare parts
        SP_ET: float = math.exp(-9.492638 + 0.0001413 * RG + 3.493 / W) * NP["ET"]
        SP_IT: float = math.exp(-9.492638 + 0.0001413 * RG + 3.493 / W) * NP["IT"]

        # Maintenance labour
        ML: float = 0.7912 * SP_ET

        # Tyre life
        TL: float = 23726 + 4046 * W - 398 * RF - 1.0099 * RG

        # Engine oil
        EOL: float = 1.3826 + 0.03348 * RF + 0.002319 * (RG / W)

        # Other oil
        OL: float = 5.1037 + 0.0002646 * RG

        # Grease
        G: float = 0.9153 + 0.0707 * RF + 0.000627 * RG

        # -----------------------------
        # TIME RELATED
        # -----------------------------

        # Utilisation
        UPD: float = 77.7233 + 5.8915 * V

        # Fixed costs
        FXC_ET: float = 1238.28 / UPD
        FXC_IT: float = 1479.30 / UPD

        # Depreciation costs
        DC_ET: float = 238.54 / UPD
        DC_IT: float = 425.84 / UPD

        # Passenger time cost
        PT: float = 0

        # Crew cost
        crew: float = 1800 / UPD

        # Commodity holding cost
        CHC: float
        if lane in ['SL', 'IL']:
            CHC = 0
            raise Warning("Multi Axle Heavy Commercial Vehicles (MCVs) vehicles are not typically used in 'SL' or 'IL' lanes. Setting CHC to 0.")
        elif lane == '2L':
            CHC = 409.28 / UPD
        elif lane in ['4L', '6L', '8L', 'EW']:
            CHC = 1707.37 / UPD
        else:
            raise ValueError(f"Invalid lane type '{lane}' for Multi Axle Heavy Commercial Vehicles (MCVs) vehicle.")

        # -----------------------------
        # BUILD FINAL OUTPUT
        # -----------------------------
        return build_voc_output(
            vt=vt, lane=lane,
            velocity=V,
            petrol=petrol, diesel=diesel,
            SP_ET=SP_ET, SP_IT=SP_IT,
            ML=ML, TL=TL,
            EOL=EOL, OL=OL, G=G,
            FXC_ET=FXC_ET, FXC_IT=FXC_IT,
            DC_ET=DC_ET, DC_IT=DC_IT,
            PT=PT, crew=crew, CHC=CHC,
            UPD=UPD
        )

    else:
        raise NotImplementedError(
            f"VOC computation for vehicle type '{vt}' is not implemented yet."
        )
