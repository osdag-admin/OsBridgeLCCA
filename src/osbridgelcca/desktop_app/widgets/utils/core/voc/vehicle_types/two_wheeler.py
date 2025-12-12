from typing import Dict, Any, TypedDict
import IRC_standards.IRCSP30_2019
from voc.utils.output_builder import build_voc_output
from voc.utils.pre_processor import VehicleInput, extract_vehicle_inputs

Vehicle = "two_wheelers"


def compute_voc(vehicle_input: VehicleInput) -> Dict[str, Any]:
    vt, W, RG, FL, RS, lane, RF = extract_vehicle_inputs(vehicle_input)
    vt: str = vehicle_input["vehicle_type"]
    NP: Dict[str, Any] = IRC_standards.IRCSP30_2019.vehicle_costs[Vehicle]

    if vt == Vehicle:
        # -----------------------------
        # SPEED FORMULA
        # -----------------------------
        speed_map: Dict[str, float] = {
            'SL': 52.91 - 0.6922 * RF - 0.002874 * (RG - 2000),
            'IL': 58.86 - 0.7298 * RF - 0.002231 * (RG - 2000),
            '2L': 59.71 - 0.7892 * RF - 0.001891 * (RG - 2000),
            '4L': 78.57 - 0.7235 * RF - 0.001729 * RG,
            '6L': 81.35 - 0.7235 * RF - 0.001729 * RG,
            '8L': 82.73 - 0.7235 * RF - 0.001729 * RG,
            'EW': 77.19 - 0.7235 * RF - 0.001729 * RG + 0.396 * (W if W else 0)
        }

        V: float = speed_map.get(lane, 0.0)

        # -----------------------------
        # DISTANCE RELATED
        # -----------------------------

        # Fuel consumption
        petrol: float = 2.704 + (439.656 / V) + 0.00349 * (V ** 2) + 0.000157 * RG + 0.3642 * RS - 0.2709 * FL
        diesel: float = 0

        # Spare parts
        SP_ET: float = ((-55.879 + 0.024 * RG) * (10 ** -5)) * NP["ET"]
        SP_IT: float = ((-55.879 + 0.024 * RG) * (10 ** -5)) * NP["IT"]

        # Maintenance labour
        ML: float = 0.5498 * SP_ET

        # Tyre life
        TL: float = 47340 - 101.8 * RF - 18.39 * (RG / W)

        # Engine oil
        EOL: float = 0.405 + 0.007899 * RF + 0.000125 * (RG / W)

        # Other oil
        OL: float = 0.0

        # Grease
        G: float = 0.0

        # -----------------------------
        # TIME RELATED
        # -----------------------------

        # Utilisation
        UPD: float = 2.119 * V

        # Fixed costs
        FXC_ET: float = 24.32 / UPD
        FXC_IT: float = 24.86 / UPD

        # Depreciation costs
        DC_ET: float = 4.26 / UPD
        DC_IT: float = 5.85 / UPD

        # Passenger time cost
        if lane in ['SL', 'IL']:
            PT = 49.28 / V
        elif lane == '2L':
            PT = 70.29 / V
        elif lane in ['4L', '6L', '8L', 'EW']:
            PT = 70.77 / V
        else:
            PT = 0

        # Crew cost
        crew: float = 0.0

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
