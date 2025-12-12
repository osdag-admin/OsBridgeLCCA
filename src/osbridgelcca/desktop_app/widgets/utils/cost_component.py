from abc import ABC, abstractmethod
import os
import sqlite3
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field

class CostComponent(ABC):
    """Abstract Base Class for different cost components in Life Cycle Cost Analysis."""

    def __init__(self, amount, category, is_initial, is_recurring, present_worth_factor):
        """
        Initialize a generic cost component.

        :param amount: Cost amount in INR
        :param category: Economic, Environmental, or Social
        :param is_initial: True if an initial cost, False if future cost
        :param is_recurring: True if recurring, False if one-time
        :param present_worth_factor: Discounting factor for future costs (present_worth_factor)
        """
        self.amount = amount
        self.category = category
        self.is_initial = is_initial
        self.is_recurring = is_recurring
        self.present_worth_factor = present_worth_factor

    @abstractmethod
    def calculate_cost(self):
        """Abstract method to be implemented by subclasses for cost calculation."""
        pass

class InitialConstructionCost:
    """Calculation for all Structural works data"""
    def __init__(self): 
        self.present_worth_factor = 1.0

    def calculate_cost(self, quantity: float, rate: float) -> float:
        return quantity * rate * self.present_worth_factor

class InitialCarbonEmissionCost:
    """Calculates initial carbon emissions from material production and transport."""
    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, material_quantity: float,
                             carbon_emission_factor: float,
                             carbon_cost: float) -> float:
        return material_quantity * carbon_emission_factor * carbon_cost * self.present_worth_factor

class TimeCost:
    """Calculates economic losses due to construction delays."""
    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, construction_cost:float,
                             interest_rate:float,
                             time:float,
                             investment_ratio:float) -> float:
        return construction_cost * interest_rate * time * investment_ratio * self.present_worth_factor

class RoutineInspectionCost:
    """Annual cost of inspections for structural integrity."""

    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, inflation_rate:float,
                             init_construction_cost:float,
                             cost:float,
                             frequency:float,
                             discount_rate:float,
                             design_life:float) -> float:
        
        print(type(frequency),type(design_life))
        
        self.present_worth_factor = sum(((1 + inflation_rate) / (1 + discount_rate)) ** period for period in range(frequency, design_life, frequency))
        return init_construction_cost * self.present_worth_factor * cost

class PeriodicMaintenanceCost:
    """Includes expenses for routine maintenance activities."""

    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, inflation_rate:float,
                             init_construction_cost:float,
                             cost:float,
                             frequency:float,
                             discount_rate:float,
                             design_life:float) -> float:
        
        self.present_worth_factor = sum(((1 + inflation_rate) / (1 + discount_rate)) ** period for period in range(frequency, design_life, frequency))
        return init_construction_cost * self.present_worth_factor * cost

class MajorInspectionCost:

    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, inflation_rate:float,
                             init_construction_cost:float,
                             cost:float,
                             frequency:float,
                             discount_rate:float,
                             design_life:float) -> float:
        
        self.present_worth_factor = sum(((1 + inflation_rate) / (1 + discount_rate)) ** period for period in range(frequency, design_life, frequency))
        return init_construction_cost * self.present_worth_factor * cost

class MajorRepairCost:

    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, inflation_rate:float,
                             init_construction_cost:float,
                             cost:float,
                             frequency:float,
                             discount_rate:float,
                             design_life:float) -> float:
        
        self.present_worth_factor = sum(((1 + inflation_rate) / (1 + discount_rate)) ** period for period in range(frequency, design_life, frequency))
        return init_construction_cost * self.present_worth_factor * cost
    
class BearingAndExpansionJointReplacementCost:

    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, inflation_rate:float,
                             total_superstructure_cost:float,
                             cost:float,
                             frequency:float,
                             discount_rate:float,
                             design_life:float) -> float:
        
        self.present_worth_factor = sum(((1 + inflation_rate) / (1 + discount_rate)) ** period for period in range(frequency, design_life, frequency))
        return total_superstructure_cost * self.present_worth_factor * cost

class PeriodicMaintenanceCarbonCost:
    """Calculates emissions from maintenance activities."""

    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, inflation_rate:float,
                             total_carbon_emission_cost:float,
                             cost:float,
                             frequency:float,
                             discount_rate:float,
                             design_life:float) -> float:
        
        self.present_worth_factor = sum(((1 + inflation_rate) / (1 + discount_rate)) ** period for period in range(frequency, design_life, frequency))
        return total_carbon_emission_cost * self.present_worth_factor * cost

class MajorRepairRelCarbonEmissionCost:

    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, inflation_rate:float,
                             total_carbon_emission_cost:float,
                             cost:float,
                             frequency:float,
                             discount_rate:float,
                             design_life:float) -> float:
        
        self.present_worth_factor = sum(((1 + inflation_rate) / (1 + discount_rate)) ** period for period in range(frequency, design_life, frequency))
        return total_carbon_emission_cost * self.present_worth_factor * cost

class CarbonEmissionDueToRerouting:

    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, additional_rerouting_dist:float,
                             duration_major_repair:float,
                             working_days_month:int,
                             total_traffic:float,
                             scc:float,
                             co2_emission_per_km:float,
                             repair_freq:float,
                             inflation_rate:float,
                             discount_rate:float,
                             design_life:float) -> float:
        
        self.present_worth_factor = sum(((1 + inflation_rate) / (1 + discount_rate)) ** period for period in range(repair_freq, design_life, repair_freq))
        return total_traffic * duration_major_repair * working_days_month * scc * co2_emission_per_km * self.present_worth_factor * additional_rerouting_dist

class DemolitionCost:
    """Costs incurred at the end of bridge life for demolition and disposal."""

    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, init_constr_cost:float,
                             demolition_disposal_cost:float,
                             analysis_period:float,
                             inflation_rate:float,
                             discount_rate:float) -> float:

        self.present_worth_factor = ((1 + inflation_rate) / (1 + discount_rate)) ** analysis_period                   
        return init_constr_cost * self.present_worth_factor * demolition_disposal_cost

class DemolitionCarbonCost:

    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, init_carbon_emission_cost:float,
                             demolition_disposal_cost:float,
                             analysis_period:float,
                             inflation_rate:float,
                             discount_rate:float) -> float:
                             
        self.present_worth_factor = ((1 + inflation_rate) / (1 + discount_rate)) ** analysis_period                   
        return init_carbon_emission_cost * self.present_worth_factor * demolition_disposal_cost

class DemolitionCarbonReroutingCost:

    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, additional_rerouting_dist:float,
                             init_constr_cost:float,
                             demolition_disposal_time:float,
                             working_days_month:int,
                             scc:float,
                             co2_emission_per_km:float,
                             design_life:float,
                             analysis_period:float,
                             inflation_rate:float,
                             discount_rate:float) -> float:

        self.present_worth_factor = sum(((1 + inflation_rate) / (1 + discount_rate)) ** period for period in range(analysis_period, design_life, analysis_period))
        return init_constr_cost * self.present_worth_factor * demolition_disposal_time * working_days_month * scc * co2_emission_per_km * additional_rerouting_dist

class RecyclingCost:
    """Accounts for material salvage and repurposing costs."""

    def __init__(self):
        self.present_worth_factor = 1.00

    def calculate_cost(self, total_material_cost:float,
                             material_scrap_rate:float,
                             material_recyclability:float,
                             design_life:float,
                             analysis_period:float,
                             inflation_rate:float,
                             discount_rate:float) -> float:

        self.present_worth_factor = sum(((1 + inflation_rate) / (1 + discount_rate)) ** period for period in range(analysis_period, design_life, analysis_period))
        return material_scrap_rate * material_recyclability * total_material_cost * self.present_worth_factor

class RoadUserCost(CostComponent):
    """Evaluates economic impact on road users due to delays and detours."""

    def __init__(self, vehicles_affected, vehicle_operation_cost, construction_time):
        cost = vehicles_affected * vehicle_operation_cost * construction_time
        super().__init__(amount=cost, category="Economic", is_initial=True, is_recurring=False, present_worth_factor=1.00)
        self.vehicles_affected = vehicles_affected
        self.vehicle_operation_cost = vehicle_operation_cost
        self.construction_time = construction_time

    def calculate_cost(self):
        return self.vehicles_affected * self.vehicle_operation_cost * self.construction_time * self.present_worth_factor


class AdditionalCarbonEmissionCost(CostComponent):
    """Accounts for increased emissions from detoured traffic during bridge work."""

    def __init__(self, vehicles_affected, reroute_distance, co2_emission_per_km, carbon_cost):
        cost = vehicles_affected * reroute_distance * co2_emission_per_km * carbon_cost
        super().__init__(amount=cost, category="Environmental", is_initial=True, is_recurring=False, present_worth_factor=1.00)
        self.vehicles_affected = vehicles_affected
        self.reroute_distance = reroute_distance
        self.co2_emission_per_km = co2_emission_per_km
        self.carbon_cost = carbon_cost

    def calculate_cost(self):
        return self.vehicles_affected * self.reroute_distance * self.co2_emission_per_km * self.carbon_cost * self.present_worth_factor

class RepairAndRehabilitationCost(CostComponent):
    """Covers major structural repairs and retrofitting."""

    def __init__(self, repair_cost_rate, construction_cost=0, discount_rate=0, period=1, design_life=1):
        pwf = 1 / ((1 + discount_rate) ** (period))
        cost = repair_cost_rate * construction_cost * pwf
        super().__init__(amount=cost, category="Economic", is_initial=False, is_recurring=True, present_worth_factor=pwf)

    def calculate_cost(self):
        return self.amount


class ReconstructionCost(CostComponent):
    """Accounts for partial or complete reconstruction of the bridge due to structural failures or obsolescence."""

    def __init__(self, demolition_cost, reconstruction_cost, reconstruction_carbon_cost, reconstruction_time_cost, reconstruction_roaduser_cost, reconstruction_rerouting_carbon_cost, design_life, discount_rate):
        pwf = 1 / ((1 + discount_rate) ** design_life)
        cost = (demolition_cost + reconstruction_cost + reconstruction_carbon_cost + reconstruction_time_cost + reconstruction_roaduser_cost + reconstruction_rerouting_carbon_cost) * pwf 
        super().__init__(amount=cost, category="Economic", is_initial=False, is_recurring=False, present_worth_factor=pwf)

    def calculate_cost(self):
        return self.amount



@dataclass
class UserInputs:
    user_materials: List[Dict[str, Any]] = field(default_factory=lambda: [
        {"material": "concrete", "grade": "M40", "unit": "cum", "quantity": 214, "rate": 11994},
        {"material": "steel", "grade": "E 250(Fe 410W)A", "unit": "MT", "quantity": 27.99, "rate": 91565},
        {"material": "steel", "grade": "E 300(Fe 440)", "unit": "MT", "quantity": 5.69, "rate": 185100},
    ])
    road_user_inputs: Dict[str, Any] = field(default_factory=lambda: {
        "Lane_Type": "Single Lane Roads",
        "Roughness": 2000,
        "RF": 5,
        "reroute_distance": 1,
        "Vehicles": [
            {"Vehicle_Type": "Small Cars", "Count": 1000},
            {"Vehicle_Type": "Big Cars", "Count": 2000},
            {"Vehicle_Type": "Two Wheelers", "Count": 4000},
        ]
    })
    user_input_steel_quantity: float = 0.0
    user_input_steel_unit: str = "MT"
    analysis_period: float = 50.0
    design_life: float = 50.0
    discount_rate: float = 0.0425
    construction_time: float = 0.75
    reroute_distance: float = 1.0
    interest_rate: float = 0.1
    investment_ratio: float = 0.5
    concrete_emission_factor: float = 0.084
    concrete_co2_emission_factor: float = 0.487032864540167
    steel_emission_factor: float = 2.6
    co2_emission_per_km: float = 0.1213
    carbon_cost: float = 6.3936
    maintenance_cost_rate: float = 0.0055
    maintenance_period: float = 5.0
    inspection_rate: float = 0.01
    inspection_period: float = 1.0
    repair_cost_rate: float = 0.10
    repair_period: float = 30.0
    demolition_rate: float = 0.10
    scrap_value: float = 50000.0
    scrap_rate: float = 0.98



#COST CALULATIONS 



if __name__ == "__main__":

    # === USER INPUTS (all overridable parameters grouped) ===
    inputs = UserInputs()
    user_materials = inputs.user_materials
    road_user_inputs = inputs.road_user_inputs
    user_input_steel_quantity = inputs.user_input_steel_quantity
    user_input_steel_unit = inputs.user_input_steel_unit
    analysis_period = inputs.analysis_period
    design_life = inputs.design_life
    discount_rate = inputs.discount_rate
    construction_time = inputs.construction_time
    reroute_distance = inputs.reroute_distance
    interest_rate = inputs.interest_rate
    investment_ratio = inputs.investment_ratio
    concrete_emission_factor = inputs.concrete_emission_factor
    concrete_co2_emission_factor = inputs.concrete_co2_emission_factor
    steel_emission_factor = inputs.steel_emission_factor
    co2_emission_per_km = inputs.co2_emission_per_km
    carbon_cost = inputs.carbon_cost
    maintenance_cost_rate = inputs.maintenance_cost_rate
    maintenance_period = inputs.maintenance_period
    inspection_rate = inputs.inspection_rate
    inspection_period = inputs.inspection_period
    repair_cost_rate = inputs.repair_cost_rate
    repair_period = inputs.repair_period
    demolition_rate = inputs.demolition_rate
    scrap_value = inputs.scrap_value
    scrap_rate = inputs.scrap_rate

    # 1. Initial Construction Cost Calculation
    total_initial_construction_cost = 0
    for item in user_materials:
        component = InitialConstructionCost(
            quantity=item["quantity"],
            rate=item["rate"]
        )
        total_initial_construction_cost += component.calculate_cost()
    print("Total Initial Construction Cost:", total_initial_construction_cost)  # INR

    # 2. Initial Carbon Emission Cost Calculation (Concrete + Steel)
    total_concrete_kg = 0
    for item in user_materials:
        if item["material"] == "concrete":
            qty = item["quantity"]
            unit = item["unit"].lower()
            if unit == "cum":
                qty = qty * 2549.25  # density: kg/cum
            total_concrete_kg += qty
    total_steel_kg = 0
    for item in user_materials:
        if item["material"] == "steel":
            qty = item["quantity"]
            unit = item["unit"].upper()
            if unit == "MT":
                qty = qty * 1000  # 1 MT = 1000 kg
            total_steel_kg += qty
    total_carbon_emission_cost = (
        (total_concrete_kg * concrete_emission_factor) + (total_steel_kg * steel_emission_factor)
    ) * carbon_cost
    print("Total Initial Carbon Emission Cost:", total_carbon_emission_cost)  # INR

    # 3. Time Cost Calculation
    time_cost_component = TimeCost(
        construction_cost=total_initial_construction_cost,
        interest_rate=interest_rate,
        time=construction_time,
        investment_ratio=investment_ratio
    )
    print("Time Cost:", time_cost_component.calculate_cost())  # INR

    # 4. Road User Cost Calculation

    total_vehicles_affected = sum(v["Count"] for v in road_user_inputs["Vehicles"])
    
    # Use a relative path for the database
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'databases', 'IRC_Road_Costs.db')
    db_path = os.path.abspath(db_path)

    total_road_user_cost = 0
    # construction_time and reroute_distance are now shared variables
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_name = cursor.fetchone()[0]
        for vehicle in road_user_inputs["Vehicles"]:
            vehicle_type = vehicle["Vehicle_Type"]
            count = vehicle["Count"]
            lane_type = road_user_inputs["Lane_Type"]
            roughness = road_user_inputs["Roughness"]
            rf = road_user_inputs["RF"]
            cursor.execute(f'''
                SELECT Grand_Cost FROM {table_name} WHERE 
                    Vehicle_Type = ? AND Lane_Type = ? AND Roughness = ? AND RF = ?
            ''', (vehicle_type, lane_type, roughness, rf))
            result = cursor.fetchone()
            if result:
                grand_cost = result[0]
                ct = construction_time * reroute_distance
                road_user_cost_component = RoadUserCost(
                    vehicles_affected=count,
                    vehicle_operation_cost=grand_cost,
                    construction_time=ct
                )
                total_road_user_cost += road_user_cost_component.calculate_cost()
            else:
                print(f"No Grand_Cost found for {vehicle_type}, {lane_type}, {roughness}, {rf}")
    print("Total Road User Cost:", total_road_user_cost)  # INR
    

    # 5. Additional Carbon Emission Cost Calculation
    vehicles_affected = sum(v["Count"] for v in road_user_inputs["Vehicles"])
    additional_carbon_inputs = {
        "vehicles_affected": vehicles_affected,
        "reroute_distance": reroute_distance,
    }
    additional_carbon_emission_component = AdditionalCarbonEmissionCost(
        vehicles_affected=additional_carbon_inputs["vehicles_affected"],
        reroute_distance=additional_carbon_inputs["reroute_distance"],
        co2_emission_per_km=co2_emission_per_km,
        carbon_cost=carbon_cost
    )
    print("Additional Carbon Emission Cost:", additional_carbon_emission_component.calculate_cost())  # INR

    # 6. Periodic Maintenance Cost Calculation
    period = maintenance_period
    periodic_maintenance_component = PeriodicMaintenanceCost(
        maintenance_cost_rate=maintenance_cost_rate,
        construction_cost=total_initial_construction_cost,
        discount_rate=discount_rate,
        period=period,
        design_life=design_life
    )
    print("Periodic Maintenance Cost:", periodic_maintenance_component.calculate_cost())  # INR

    # 7. Periodic Maintenance Carbon Emission Cost Calculation (Concrete only)
    maintenance_concrete_kg = 0
    for item in user_materials:
        if item["material"].lower() == "concrete":
            qty = item["quantity"]
            unit = item["unit"].lower()
            if unit == "cum":
                qty = qty * 2549.25  # density: kg/cum
            # If already in kg, use as is
            maintenance_concrete_kg += qty
    maintenance_concrete_emission_factor = concrete_co2_emission_factor
    maintenance_carbon_cost = carbon_cost
    maintenance_discount_rate = discount_rate
    maintenance_period = period
    maintenance_design_life = design_life
    periodic_maintenance_concrete_carbon_component = PeriodicMaintenanceCarbonCost(
        material_quantity=maintenance_concrete_kg,
        carbon_emission_factor=maintenance_concrete_emission_factor,
        carbon_cost=maintenance_carbon_cost,
        discount_rate=maintenance_discount_rate,
        period=maintenance_period,
        design_life=maintenance_design_life
    )
    print("Periodic Maintenance Carbon Emission Cost (Concrete only):", periodic_maintenance_concrete_carbon_component.calculate_cost())  # INR

    # 8. Annual Routine Inspection Cost Calculation
    inspection_discount_rate = discount_rate
    inspection_design_life = design_life
    inspection_component = RoutineInspectionCost(
        inspection_cost_rate=inspection_rate,  # Use inspection_rate as inspection cost rate
        construction_cost=total_initial_construction_cost,  # Always use total_initial_construction_cost
        discount_rate=inspection_discount_rate,
        design_life=inspection_design_life,
        period=inspection_period  # always annual
    )
    total_routine_inspection_cost = inspection_component.calculate_cost()
    print("Total Routine Inspection Cost:", total_routine_inspection_cost)  # INR

    # 9. Repair and Rehabilitation Cost Calculation
    repair_period = repair_period
    repair_component = RepairAndRehabilitationCost(
        repair_cost_rate=repair_cost_rate,
        construction_cost=total_initial_construction_cost,
        discount_rate=discount_rate,
        period=repair_period,
        design_life=design_life
    )
    print("Repair and Rehabilitation Cost:", repair_component.calculate_cost())  # INR

    # 10. Demolition and Disposal Cost Calculation
    demolition_discount_rate = discount_rate
    demolition_design_life = design_life
    demolition_component = DemolitionCost(
        demolition_rate=demolition_rate,
        construction_cost=total_initial_construction_cost,
        discount_rate=demolition_discount_rate,
        design_life=demolition_design_life
    )
    print("Demolition and Disposal Cost:", demolition_component.calculate_cost())  # INR

    # 11. Recycling Cost Calculation
    recycling_design_life = design_life
    user_input_steel_quantity = 0  # eg (user input, 15 MT or 15000 kg)
    user_input_steel_unit = "MT"   # eg (user input, can be 'MT' or 'kg')
    if user_input_steel_unit.lower() == "kg":
        user_input_steel_quantity_mt = user_input_steel_quantity / 1000
    else:
        user_input_steel_quantity_mt = user_input_steel_quantity
    recycling_component = RecyclingCost(
        scrap_value=scrap_value,
        quantity=user_input_steel_quantity_mt,
        scrap_rate=scrap_rate,
        discount_rate=discount_rate,
        design_life=recycling_design_life
    )
    print("Recycling Cost (user-input steel only):", recycling_component.calculate_cost())  # INR

    # 12. Reconstruction Cost Calculation 
    demolition_cost = demolition_component.calculate_cost()
    reconstruction_cost = total_initial_construction_cost
    reconstruction_carbon_cost = total_carbon_emission_cost
    reconstruction_time_cost = time_cost_component.calculate_cost()
    reconstruction_roaduser_cost = road_user_cost_component.calculate_cost()
    reconstruction_rerouting_carbon_cost = additional_carbon_emission_component.calculate_cost()
    reconstruction_design_life = design_life
    reconstruction_result = 0
    if analysis_period > design_life:
        reconstruction_component = ReconstructionCost(
            demolition_cost=demolition_cost,
            reconstruction_cost=reconstruction_cost,
            reconstruction_carbon_cost=reconstruction_carbon_cost,
            reconstruction_time_cost=reconstruction_time_cost,
            reconstruction_roaduser_cost=reconstruction_roaduser_cost,
            reconstruction_rerouting_carbon_cost=reconstruction_rerouting_carbon_cost,
            design_life=reconstruction_design_life,
            discount_rate=discount_rate
        )
        reconstruction_result = reconstruction_component.calculate_cost()
    else:
        reconstruction_result = 0
    print("Reconstruction Cost:", reconstruction_result)  # INR





    # --- To be connected to UI ---
    results = {
        "Total Initial Construction Cost": total_initial_construction_cost,
        "Total Initial Carbon Emission Cost": total_carbon_emission_cost,
        "Time Cost": time_cost_component.calculate_cost(),
        "Total Road User Cost": total_road_user_cost,
        "Additional Carbon Emission Cost": additional_carbon_emission_component.calculate_cost(),
        "Periodic Maintenance Cost": periodic_maintenance_component.calculate_cost(),
        "Periodic Maintenance Carbon Emission Cost": periodic_maintenance_concrete_carbon_component.calculate_cost(),
        "Total Routine Inspection Cost": total_routine_inspection_cost,
        "Repair and Rehabilitation Cost": repair_component.calculate_cost(),
        "Demolition and Disposal Cost": demolition_component.calculate_cost(),
        "Recycling Cost": recycling_component.calculate_cost(),
        "Reconstruction Cost": reconstruction_result
    }










