from typing import Dict, Any, TypedDict
import IRC_standards.IRCSP30_2019
from voc.utils.output_builder import build_voc_output
from voc.utils.pre_processor import VehicleInput, extract_vehicle_inputs
import math

Vehicle = "buses"


def compute_voc(vehicle_input: VehicleInput) -> Dict[str, Any]:
    vt, W, RG, FL, RS, lane, RF = extract_vehicle_inputs(vehicle_input)
    NP: Dict[str, int] = IRC_standards.IRCSP30_2019.vehicle_costs[Vehicle]

    if vt == Vehicle:
        # -----------------------------
        # SPEED FORMULA
        # -----------------------------
        speed_map: Dict[str, float] = {
            'SL': 47.25 - 0.3698 * RF - 0.00165 * (RG - 2000),
            'IL': 52.65 - 0.4031 * RF - 0.00123 * (RG - 2000),
            '2L': 54.23 - 0.4111 * RF - 0.00098 * (RG - 2000),
            '4L': 75.43 - 0.214 * RF - 0.00198 * RG,
            '6L': 77.58 - 0.214 * RF - 0.00198 * RG,
            '8L': 79.73 - 0.214 * RF - 0.00198 * RG,
            'EW': 71.13 - 0.214 * RF - 0.00198 * RG + 0.614 * W
        }

        V: float = speed_map.get(lane, 0.0)

        # -----------------------------
        # DISTANCE RELATED
        # -----------------------------

        # Fuel consumption
        petrol: float = 0
        diesel: float = 34.23 + (4054.42 / V) + 0.02149 * \
            (V ** 2) + 0.001246 * RG + \
            3.4557 * RS - 1.8454 * FL

        # Spare parts
        SP_ET: float = (math.exp(-9.7871 + 0.007373 * RF +
                        0.0000723 * RG + 1.925 / W)) * NP["ET"]
        SP_IT: float = (math.exp(-10.1126 + 0.007373 * RF +
                        0.0000723 * RG + 1.925 / W)) * NP["IT"]

        # Maintenance labour
        ML: float = 1.1781 * SP_ET

        # Tyre life
        TL: float = 38519 - 389.52 * RF - 1.32 * RG + 983.829 * W

        # Engine oil
        EOL: float = 0.4303 + 0.001494 * RF + 0.0007885 * (RG / W)

        # Other oil
        OL: float = 3.3201 + 0.002889 * RF + 0.0008217 * RG - 0.3295 * W

        # Grease
        G: float = 4.992 + 0.03376 * RF + 0.3634 * W

        # -----------------------------
        # TIME RELATED
        # -----------------------------

        # Utilisation
        UPD: float = 22.7134 + 12.2569 * V

        # Fixed costs
        FXC_ET: float = 772.89 / UPD
        FXC_IT: float = 1415.09 / UPD

        # Depreciation costs
        DC_ET: float = 221.00 / UPD
        DC_IT: float = 355.71 / UPD

        # Passenger time cost
        if lane in ['SL', 'IL']:
            PT = 7297.63 / UPD
        elif lane == '2L':
            PT = 15509.80 / UPD
        elif lane in ['4L', '6L', '8L']:
            PT = 23721.98 / UPD
        elif lane == 'EW':
            PT = 28385.28 / UPD
        else:
            PT = 0
            
        # Crew cost
        crew: float = 3775.3 / UPD

        # Commodity holding cost
        CHC: float = 0.0

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
