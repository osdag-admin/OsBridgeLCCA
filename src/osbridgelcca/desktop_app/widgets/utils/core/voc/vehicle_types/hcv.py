from typing import Dict, Any, TypedDict
import IRC_standards.IRCSP30_2019
from voc.utils.output_builder import build_voc_output
from voc.utils.pre_processor import VehicleInput, extract_vehicle_inputs
import math

Vehicle = "hcv"


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
            'SL': 48.29 - 0.4306 * RF - 0.00086 * (RG - 2000),
            'IL': 53.12 - 0.4736 * RF - 0.00094 * (RG - 2000),
            '2L': 56.52 - 0.5040 * RF - 0.00100 * (RG - 2000),
            '4L': 75.15 - 0.6487 * RF - 0.001285 * RG,
            '6L': 77.17 - 0.6487 * RF - 0.001285 * RG,
            '8L': 79.19 - 0.6487 * RF - 0.001285 * RG,
            'EW': 71.11 - 0.6487 * RF - 0.001285 * RG + 0.577 * W
        }

        V: float = speed_map.get(lane, 0.0)

        # -----------------------------
        # DISTANCE RELATED
        # -----------------------------

        # Fuel consumption

        petrol: float = 0
        diesel: float = 50 + (8049.955 / V) + 0.012 * (V ** 2) + \
            0.005 * RG + 4.565 * RS - 4.904 * FL - 7.285 * (pwr)

        # Spare parts
        SP_ET: float = (math.exp(-9.492638 + 0.0001413 *
                        RG + 3.493 / W)) * NP["ET"]
        SP_IT: float = (math.exp(-9.492638 + 0.0001413 *
                        RG + 3.493 / W)) * NP["IT"]

        # Maintenance labour
        ML: float = 0.7912 * SP_ET

        # Tyre life
        TL: float = 24662 + 4205 * W - 413.6 * RF - 1.142 * RG

        # Engine oil
        EOL: float = 1.0277 + 0.02495 * RF + 0.0001782 * (RG / W)

        # Other oil
        OL: float = 5.1037 + 0.0002646 * RG

        # Grease
        G: float = 0.9153 + 0.0707 * RF + 0.000627 * RG

        # -----------------------------
        # TIME RELATED
        # -----------------------------

        # Utilisation
        UPD: float = 55.6719 + 4.22 * V

        # Fixed costs
        FXC_ET: float = 924.28 / UPD
        FXC_IT: float = 1056.82 / UPD

        # Depreciation costs
        DC_ET: float = 154.84 / UPD
        DC_IT: float = 256.80 / UPD

        # Passenger time cost
        PT = 0

        # Crew cost
        crew: float = 1500 / UPD

        # Commodity holding cost
        CHC: float = 0.0
        if lane in ['SL', 'IL']:
            CHC = 182.79 / UPD
        elif lane == '2L':
            CHC = 218.75 / UPD
        elif lane in ['4L', '6L', '8L']:
            CHC = 1084.14 / UPD
        elif lane == 'EW':
            CHC = 1084.14 / UPD
        else:
            raise ValueError(f"Invalid lane type '{lane}' for HCV vehicle.")
        

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
