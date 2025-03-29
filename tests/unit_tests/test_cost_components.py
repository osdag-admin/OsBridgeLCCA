import pytest
from src.osbridgelcca.core.cost_components import (
    InitialConstructionCost,
    InitialCarbonEmissionCost,
    TimeCost,
    RoadUserCost,
    ReroutingCarbonEmissionCost,
    PeriodicMaintenanceCost,
    PeriodicMaintenanceCarbonCost,
    RoutineInspectionCost,
    RepairAndRehabilitationCost,
    DemolitionCost,
    RecyclingCost,
)

def test_initial_construction_cost():
    cost = InitialConstructionCost(quantity=100, rate=50)
    assert cost.calculate_cost() == 5000

def test_initial_carbon_emission_cost():
    cost = InitialCarbonEmissionCost(material_quantity=100, carbon_emission_factor=2, carbon_cost=10)
    assert cost.calculate_cost() == 2000

def test_time_cost():
    cost = TimeCost(construction_cost=10000, interest_rate=0.05, construction_time=2, investment_ratio=0.8)
    assert cost.calculate_cost() == 800.0

def test_road_user_cost():
    cost = RoadUserCost(vehicles_affected=1000, vehicle_operation_cost=2, construction_time=5)
    assert cost.calculate_cost() == 10000

def test_additional_carbon_emission_cost():
    cost = ReroutingCarbonEmissionCost(vehicles_affected=1000, reroute_distance=10, co2_emission_per_km=0.5, carbon_cost=20)
    assert cost.calculate_cost() == 100000.0

def test_periodic_maintenance_cost():
    cost = PeriodicMaintenanceCost(maintenance_cost_rate=0.02, construction_cost=100000, discount_rate=0.03, period=5, design_life=50)
    assert cost.calculate_cost() > 0  # Ensure cost is calculated

def test_periodic_maintenance_carbon_cost():
    cost = PeriodicMaintenanceCarbonCost(material_quantity=500, carbon_emission_factor=1.5, carbon_cost=20, discount_rate=0.03, period=5, design_life=50)
    assert cost.calculate_cost() > 0

def test_routine_inspection_cost():
    cost = RoutineInspectionCost(quantity=10, rate=1000, discount_rate=0.03, design_life=50)
    assert cost.calculate_cost() > 0

def test_repair_and_rehabilitation_cost():
    cost = RepairAndRehabilitationCost(repair_cost_rate=0.1, construction_cost=100000, discount_rate=0.03, period=10, design_life=50)
    assert cost.calculate_cost() > 0

def test_demolition_cost():
    cost = DemolitionCost(demolition_rate=0.05, construction_cost=100000, discount_rate=0.03, design_life=50)
    assert cost.calculate_cost() > 0

def test_recycling_cost():
    cost = RecyclingCost(scrap_value=1000, quantity=10, discount_rate=0.03, design_life=50)
    assert cost.calculate_cost() > 0
