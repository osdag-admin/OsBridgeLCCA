import IRC_standards.IRCSP30_2019 as tableC1
from voc.utils.constants import vehicle_type_list, petrolToDieselRatio
import json
import os
from typing import Any, Dict, Union


def calculate_total_cost(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate total cost for both distanceCost and timeCost in the data.
    Updates totals based on IT/ET or value fields.
    Returns a dictionary with both totals and vehicle-specific totals.
    """
    total_cost: Dict[str, Any] = {}

    for cost_type in ["distanceCost", "timeCost"]:
        if cost_type not in data:
            continue

        total_cost[cost_type] = {"total": {"IT": 0.0, "ET": 0.0}}

        for vehicle_type, components in data[cost_type].items():
            if vehicle_type == "total":
                continue

            total_cost[cost_type][vehicle_type] = {"IT": 0.0, "ET": 0.0}

            for comp_name, comp_values in components.items():
                if comp_name.startswith("total_"):
                    continue

                if isinstance(comp_values, dict):
                    if comp_values.get('iHTC', False):
                        total_cost[cost_type]["total"]["IT"] += comp_values.get("IT", 0)
                        total_cost[cost_type]["total"]["ET"] += comp_values.get("ET", 0)
                        total_cost[cost_type][vehicle_type]["IT"] += comp_values.get("IT", 0)
                        total_cost[cost_type][vehicle_type]["ET"] += comp_values.get("ET", 0)
                    else:
                        value = comp_values.get("value", 0)
                        total_cost[cost_type]["total"]["IT"] += value
                        total_cost[cost_type]["total"]["ET"] += value
                        total_cost[cost_type][vehicle_type]["IT"] += value
                        total_cost[cost_type][vehicle_type]["ET"] += value
                elif isinstance(comp_values, (int, float)):
                    total_cost[cost_type]["total"]["IT"] += comp_values
                    total_cost[cost_type]["total"]["ET"] += comp_values
                    total_cost[cost_type][vehicle_type]["IT"] += comp_values
                    total_cost[cost_type][vehicle_type]["ET"] += comp_values
                else:
                    continue

        total_cost[cost_type]["units"] = "Rs/km/veh"

    return total_cost


def getWPI(category, vehicle_type, wpi):
    mapping = {
        "small_cars": "Small Cars",
        "big_cars": "Big Cars",
        "two_wheelers": "Two Wheeler",
        "buses": "Ordinary Buses",
        "lcv": "LCV",
        "hcv": "HCV",
        "mcv": "MCV"
    }

    vt = mapping.get(vehicle_type)
    if vt is None:
        raise ValueError(f"Invalid vehicle type: {vehicle_type}")

    WPI_data = wpi.get("WPI", {})

    # 1️⃣ CATEGORY EXISTS AT TOP LEVEL (fuelCost, commodityHoldingCost, medicalCost, passengerCrewCost, votCost)
    if category in WPI_data:
        block = WPI_data[category]

        if isinstance(block, dict) and vt in block:
            return block[vt]

        return block  # entire block if not vehicle-specific

    # 2️⃣ CATEGORY INSIDE vehicleCost (tyreCost, spareParts, fixedDepreciation, propertyDamage)
    vehicle_cost = WPI_data.get("vehicleCost", {})
    if category in vehicle_cost:
        block = vehicle_cost[category]
        return block.get(vt)

    # Category not found
    raise ValueError(f"WPI category '{category}' not found for vehicle type '{vehicle_type}'.")


# ----------------- Helper functions -----------------

def per_km_cost(liters_per_unit: float, price_IT: float, price_ET: float, factor: float = 1000.0):
    IT = (liters_per_unit * price_IT) / factor
    ET = (liters_per_unit * price_ET) / factor
    return IT, ET


def apply_wpi(cost: Dict[str, float], wpi_val: Union[float, Dict[str, Any], None]) -> dict[str, float | str | bool]:
    # normalize wpi_val to a numeric multiplier
    multiplier: float = 1.0
    if isinstance(wpi_val, (int, float)):
        multiplier = float(wpi_val)
    elif isinstance(wpi_val, dict):
        # prefer common numeric keys
        if "IT" in wpi_val and isinstance(wpi_val["IT"], (int, float)):
            multiplier = float(wpi_val["IT"])
        elif "value" in wpi_val and isinstance(wpi_val["value"], (int, float)):
            multiplier = float(wpi_val["value"])
        else:
            # try to pick any numeric value from the dict
            for v in wpi_val.values():
                if isinstance(v, (int, float)):
                    multiplier = float(v)
                    break

    return {
        "IT": cost["IT"] * multiplier,
        "ET": cost["ET"] * multiplier,
        "unit": "Rs/km",
        "iHTC": True
    }


# ----------------- Main function -----------------

def post_process(outputFromVocOutputBuilder: Dict[str, Any], wpi: Dict[str, Any], debug: bool = False) -> Dict[str, Any]:
    wpiAdjustedValues: Dict[str, Any] = {"distanceCost": {}, "timeCost": {}}

    for vt in vehicle_type_list:
        if vt in outputFromVocOutputBuilder:
            wpiAdjustedValues["distanceCost"][vt] = {}

    # ---------------- TYRE COST ----------------
    for vt in vehicle_type_list:
        vdata = outputFromVocOutputBuilder.get(vt)
        if not vdata or "VOC_summary" not in vdata:
            continue

        tyre_life_km = vdata["VOC_summary"]["distance_related"]["tyre_life"]["value"]
        tyre_info = tableC1.new_tyres_costs[vt]

        IT, ET = tyre_info["IT"], tyre_info["ET"]
        num_tyres = tyre_info["num_of_wheels"]

        tyre_cost_per_km_wt = IT * num_tyres / tyre_life_km
        tyre_cost_per_km_wot = ET * num_tyres / tyre_life_km

        vdata["VOC_summary"]["distance_related"]["tyre_life"]["tyre_cost_rs_per_km"] = {
            "num_tyres": num_tyres,
            "IT": tyre_cost_per_km_wt,
            "ET": tyre_cost_per_km_wot,
            "unit": "Rs/km",
            "iHTC": True
        }

        wpi_val = getWPI("tyreCost", vt, wpi)
        wpiAdjustedValues["distanceCost"][vt]["tyreCost"] = apply_wpi(
            {"IT": tyre_cost_per_km_wt, "ET": tyre_cost_per_km_wot}, wpi_val
        )

    # ---------------- FUEL, OILS, GREASE ----------------
    for vt in vehicle_type_list:
        vdata = outputFromVocOutputBuilder.get(vt)
        if not vdata or "VOC_summary" not in vdata:
            continue

        dist = vdata["VOC_summary"]["distance_related"]
        wpiAdjustedValues["distanceCost"].setdefault(vt, {})

        # Fuel
        fuel = dist.get("fuel_consumption")
        if fuel:
            wpi_block = getWPI("fuelCost", vt, wpi)

            petrol_cost = {"IT": 0, "ET": 0}
            diesel_cost = {"IT": 0, "ET": 0}

            if fuel.get("petrol", 0) > 0:
                liters_1000 = fuel["petrol"]
                pw = tableC1.petroleum_products_costs["petrol"]["IT"]
                pe = tableC1.petroleum_products_costs["petrol"]["ET"]
                petrol_cost["IT"], petrol_cost["ET"] = per_km_cost(liters_1000, pw, pe) # type: ignore
                fuel["petrol_cost_rs_per_km"] = {
                    **petrol_cost, "unit": "Rs/km", "WPI": wpi_block.get("Petrol"), "iHTC": False
                }

            if fuel.get("diesel", 0) > 0:
                liters_1000 = fuel["diesel"]
                dw = tableC1.petroleum_products_costs["diesel"]["IT"]
                de = tableC1.petroleum_products_costs["diesel"]["ET"]
                diesel_cost["IT"], diesel_cost["ET"] = per_km_cost(liters_1000, dw, de) # type: ignore
                fuel["diesel_cost_rs_per_km"] = {
                    **diesel_cost, "unit": "Rs/km", "WPI": wpi_block.get("Diesel"), "iHTC": False
                }

            ratio = petrolToDieselRatio.get(vt, {"petrol": 0, "diesel": 0})
            wt = ratio["petrol"] * petrol_cost["IT"] + ratio["diesel"] * diesel_cost["IT"]
            wot = ratio["petrol"] * petrol_cost["ET"] + ratio["diesel"] * diesel_cost["ET"]

            fuel["fuel_cost_rs_per_km_final"] = {"IT": wt, "ET": wot, "unit": "Rs/km", "iHTC": False}
            wpiAdjustedValues["distanceCost"][vt]["fuelCost"] = {
                "IT": ratio["petrol"] * petrol_cost["IT"] * wpi_block.get("Petrol") +
                      ratio["diesel"] * diesel_cost["IT"] * wpi_block.get("Diesel"),
                "ET": ratio["petrol"] * petrol_cost["ET"] * wpi_block.get("Petrol") +
                      ratio["diesel"] * diesel_cost["ET"] * wpi_block.get("Diesel"),
                "unit": "Rs/km",
                "iHTC": True
            }

        # Engine oil, other oil, grease
        for oil_name in ["engine_oil", "other_oil", "grease"]:
            if oil_name in dist:
                liters = dist[oil_name]["value"]
                factor = 1000 if oil_name == "engine_oil" else 10000
                pw = tableC1.petroleum_products_costs[oil_name]["IT"]
                pe = tableC1.petroleum_products_costs[oil_name]["ET"]
                IT, ET = per_km_cost(liters, pw, pe, factor)

                wpi_val = getWPI("fuelCost", vt, wpi)
                if isinstance(wpi_val, dict):
                    wpi_val = wpi_val.get(oil_name.replace("_", " ").title())
                else:
                    wpi_val = 1.0

                dist[oil_name][f"{oil_name}_cost_rs_per_km"] = {"IT": IT, "ET": ET, "unit": "Rs/km", "WPI": wpi_val, "iHTC": True}
                wpiAdjustedValues["distanceCost"][vt][oil_name] = apply_wpi({"IT": IT, "ET": ET}, wpi_val)

        # Spare parts and maintenance labour
        if "spare_parts" in dist:
            wpi_val = getWPI("spareParts", vt, wpi)
            dist["spare_parts"]["WPI"] = wpi_val
            wpiAdjustedValues["distanceCost"][vt]["spare_parts"] = {
                "IT": dist["spare_parts"]["IT"] * wpi_val,
                "ET": dist["spare_parts"]["ET"] * wpi_val,
                "unit": "Rs/km",
                "iHTC": True
            }

        if "maintenance_labour" in dist:
            wpi_val = getWPI("spareParts", vt, wpi)
            dist["maintenance_labour"]["WPI"] = wpi_val
            wpiAdjustedValues["distanceCost"][vt]["maintenance_labour"] = {
                "value": dist["maintenance_labour"]["value"] * wpi_val,
                "unit": "Rs/km",
                "iHTC": False
            }

        # ---------------- TIME COST ----------------
        if "time_related" not in vdata["VOC_summary"]:
            continue

        time_block = vdata["VOC_summary"]["time_related"]
        wpiAdjustedValues["timeCost"][vt] = {}

        # Fixed and depreciation cost
        for key in ["fixed_cost", "depreciation_cost"]:
            if key in time_block:
                wpi_val = getWPI("fixedDepreciation", vt, wpi)
                time_block[key]["WPI"] = wpi_val
                wpiAdjustedValues["timeCost"][vt][key] = {
                    "IT": time_block[key]["IT"] * wpi_val,
                    "ET": time_block[key]["ET"] * wpi_val,
                    "unit": time_block[key]["unit"],
                    "iHTC": time_block[key]["iHTC"]
                }

        # Passenger and crew cost
        for key, sub_key in [("passenger_time_cost", "Passenger Cost"), ("crew_cost", "Crew Cost")]:
            if key in time_block:
                wpi_val = getWPI("passengerCrewCost", vt, wpi).get(sub_key)
                time_block[key]["WPI"] = wpi_val
                wpiAdjustedValues["timeCost"][vt][key] = {
                    "value": time_block[key]["value"] * wpi_val,
                    "unit": time_block[key]["unit"],
                    "iHTC": time_block[key]["iHTC"]
                }

        # Commodity holding cost
        if "commodity_holding_cost" in time_block:
            wpi_val = getWPI("commodityHoldingCost", vt, wpi)
            time_block["commodity_holding_cost"]["WPI"] = wpi_val
            wpiAdjustedValues["timeCost"][vt]["commodity_holding_cost"] = {
                "value": time_block["commodity_holding_cost"]["value"] * wpi_val,
                "unit": "Rs/km",
                "iHTC": time_block["commodity_holding_cost"]["iHTC"]
            }

        # Total time cost
        total_IT, total_ET = 0, 0
        for cost in wpiAdjustedValues["timeCost"][vt].values():
            if "IT" in cost:
                total_IT += cost["IT"]
            if "ET" in cost:
                total_ET += cost["ET"]
            if "value" in cost:
                total_IT += cost["value"]
                total_ET += cost["value"]

        wpiAdjustedValues["timeCost"][vt]["total_time_cost"] = {
            "IT": total_IT,
            "ET": total_ET,
            "unit": "Rs/km",
            "iHTC": True
        }

    summaryOfVOC = calculate_total_cost(wpiAdjustedValues)

    if debug:
        os.makedirs("debug", exist_ok=True)
        json.dump(outputFromVocOutputBuilder, open("debug/outputFromVocOutputBuilder.json", "w"), indent=4)
        json.dump(wpiAdjustedValues, open("debug/wpiAdjustedValues.json", "w"), indent=4)
        json.dump(summaryOfVOC, open("debug/summaryOfVOC.json", "w"), indent=4)

    return summaryOfVOC
