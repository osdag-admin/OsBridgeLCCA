from typing import Dict, Any, TypedDict
import IRC_standards.IRCSP30_2019
from voc.utils.output_builder import build_voc_output
from voc.utils.pre_processor import VehicleInput, extract_vehicle_inputs


Vehicle = "small_cars"

def compute_voc(vehicle_input: VehicleInput) -> Dict[str, Any]:
    vt, W, RG, FL, RS, lane, RF = extract_vehicle_inputs(vehicle_input)
    NP: Dict[str, Any] = IRC_standards.IRCSP30_2019.vehicle_costs[Vehicle]

    if vt == Vehicle:
        # -----------------------------
        # SPEED FORMULA
        # -----------------------------
        speed_map: Dict[str, float] = {
            'SL': 66.44 - 0.6922 * RF - 0.002874 * (RG - 2000),
            'IL': 73.16 - 0.7298 * RF - 0.002231 * (RG - 2000),
            '2L': 81.19 - 0.7892 * RF - 0.001891 * (RG - 2000),
            '4L': 100.625 - 0.394 * RF - 0.00330 * RG,
            '6L': 101.065 - 0.386 * RF - 0.00323 * RG,
            '8L': 103.517 - 0.386 * RF - 0.00323 * RG,
            'EW': 93.71 - 0.386 * RF - 0.00323 * RG + 0.701 * W
        }

        V: float = speed_map.get(lane, 0.0)

        # -----------------------------
        # DISTANCE RELATED
        # -----------------------------

        petrol: float = 30 + (844.085 / V) + 0.003 * (V ** 2) + 0.001 * RG + 0.3414 * RS - 0.2225 * FL
        diesel: float = 35 + (983.503 / V) + 0.003 * (V ** 2) + 0.002 * RG + 0.339 * RS - 0.4785 * FL
        fuel: float = 0.7 * petrol + 0.3 * diesel

        SP_ET: float = (0.0075 * (RG - 2000) * (10 ** -5)) * NP["ET"]
        SP_IT: float = (0.0075 * (RG - 2000) * (10 ** -5)) * NP["IT"]

        ML: float = 1.79934 * SP_ET
        TL: float = 68771 - 147.9 * RF - 26.72 * (RG / W)
        EOL: float = 1.8807 + 0.036615 * RF + 0.000578 * (RG / W)
        OL: float = 1.631 + 0.05167 * RF + 0.001867 * (RG / W)
        G: float = 2.816 + 0.2007 * RF

        # -----------------------------
        # TIME RELATED
        # -----------------------------
        UPD: float = 6.7127  * V
        FXC_ET: float = 395.65 / UPD
        FXC_IT: float = 400.61 / UPD
        DC_ET: float = 42.83 / UPD
        DC_IT: float = 76.68 / UPD

        if lane in ["SL", "IL"]:
            PT: float = 244.07 / V
        elif lane == "2L":
            PT: float = 328.06 / V
        elif lane in ["4L", "6L", "8L"]:
            PT: float = 498.65 / V
        elif lane == 'EW':
            PT: float = 721.73 / V
        else:
            PT: float = 0.0

        crew: float = 0.0

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
