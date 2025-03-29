from abc import ABC, abstractmethod
import pandas as pd



class CostComponent(ABC):
    """Abstract Base Class for different cost components in Life Cycle Cost Analysis."""

    def __init__(self):
        self.amount = 0  # To be calculated in subclasses
        self.category = None  # Defined in subclass
        self.is_initial = None  # Defined in subclass
        self.is_recurring = None  # Defined in subclass
        self.pwf = None  # To be calculated in subclasses

    @abstractmethod
    def calculate_cost(self):
        """Abstract method to be implemented by subclasses for cost calculation."""
        pass

    def __str__(self):
        return f"{self.__class__.__name__}: Amount = {self.amount:.2f}, Category = {self.category}"


def calculate_pwf(discount_rate=None, design_life=None, is_initial=False, is_recurring=True, interval=1,
                  future_year=None):
    """
    Calculates the Present Worth Factor (PWF) based on cost type.

    :param discount_rate: Discount rate (decimal form, e.g., 0.05 for 5%).
    :param design_life: Total design life in years.
    :param is_initial: True for initial cost (PWF = 1).
    :param is_recurring: True for recurring costs.
    :param interval: Interval in years for recurring costs (default is 1).
    :param future_year: Year when a non-recurring future cost occurs.
    :return: Present Worth Factor (PWF).
    """
    if is_initial:
        return 1.0  # Initial cost has no discounting
    elif not is_recurring:
        if future_year is None:
            raise ValueError("future_year must be provided for non-recurring future costs")
        return 1 / ((1 + discount_rate) ** future_year)
    else:
        return sum(1 / ((1 + discount_rate) ** (i * interval)) for i in range(1, int(design_life / interval) + 1))


class InitialConstructionCost(CostComponent):
    def __init__(self, material_boq: pd.DataFrame):
        super().__init__()
        self.material_boq = material_boq
        self.category = "Economic"
        self.is_initial = True
        self.is_recurring = False
        self.pwf = calculate_pwf(is_initial=True)
        self.amount = self.calculate_cost()

    def calculate_cost(self):
        return (self.material_boq.iloc[:, 2] * self.material_boq.iloc[:, 3]).sum()


class InitialCarbonEmissionCost(CostComponent):
    def __init__(self, material_boq: pd.DataFrame, carbon_cost):
        super().__init__()
        self.material_boq = material_boq
        self.carbon_cost = carbon_cost
        self.category = "Environmental"
        self.is_initial = True
        self.is_recurring = False
        self.pwf = calculate_pwf(is_initial=True)
        self.amount = self.calculate_cost()

    def calculate_cost(self):
        return self.carbon_cost * (self.material_boq.iloc[:, 2] * self.material_boq.iloc[:, 4]).sum()


class TimeCost(CostComponent):
    def __init__(self, construction_cost, interest_rate, construction_time, investment_ratio):
        super().__init__()
        self.construction_cost = construction_cost
        self.interest_rate = interest_rate
        self.construction_time = construction_time
        self.investment_ratio = investment_ratio
        self.category = "Economic"
        self.is_initial = True
        self.is_recurring = False
        self.pwf = calculate_pwf(is_initial=True)
        self.amount = self.calculate_cost()

    def calculate_cost(self):
        return self.construction_cost * self.interest_rate * self.construction_time * self.investment_ratio


class RoadUserCost(CostComponent):
    def __init__(self, vehicles_affected, vehicle_operation_cost, construction_time):
        super().__init__()
        self.vehicles_affected = vehicles_affected
        self.vehicle_operation_cost = vehicle_operation_cost
        self.construction_time = construction_time
        self.delay_cost = 0.00
        self.category = "Economic"
        self.is_initial = True
        self.is_recurring = False
        self.pwf = 1.0
        self.amount = self.calculate_cost()

    def calculate_cost(self):
        return self.vehicles_affected * (self.vehicle_operation_cost + self.delay_cost) * self.construction_time


class ReroutingCarbonEmissionCost(CostComponent):
    def __init__(self, vehicles_affected, reroute_distance, co2_emission_per_km, carbon_cost):
        super().__init__()
        self.vehicles_affected = vehicles_affected
        self.reroute_distance = reroute_distance
        self.co2_emission_per_km = co2_emission_per_km
        self.carbon_cost = carbon_cost
        self.category = "Environmental"
        self.is_initial = True
        self.is_recurring = False
        self.pwf = 1.0
        self.amount = self.calculate_cost()

    def calculate_cost(self):
        return self.vehicles_affected * self.reroute_distance * self.co2_emission_per_km * self.carbon_cost


class PeriodicMaintenanceCost(CostComponent):
    def __init__(self, maintenance_cost_rate, construction_cost, discount_rate, interval, design_life):
        super().__init__()
        self.maintenance_cost_rate = maintenance_cost_rate
        self.construction_cost = construction_cost
        self.discount_rate = discount_rate
        self.interval = interval
        self.design_life = design_life
        self.category = "Economic"
        self.is_initial = False
        self.is_recurring = True
        self.pwf = calculate_pwf(discount_rate, design_life=self.design_life, is_recurring=self.is_recurring,
                                 interval=interval)
        self.amount = self.calculate_cost()

    def calculate_cost(self):
        return self.maintenance_cost_rate * self.construction_cost * self.pwf


class PeriodicMaintenanceCarbonEmissionCost(CostComponent):
    def __init__(self, material_quantity, carbon_emission_factor, carbon_cost, discount_rate, interval, design_life):
        super().__init__()
        self.material_quantity = material_quantity
        self.carbon_emission_factor = carbon_emission_factor
        self.carbon_cost = carbon_cost
        self.discount_rate = discount_rate
        self.interval = interval
        self.design_life = design_life
        self.category = "Environmental"
        self.is_initial = False
        self.is_recurring = True
        self.pwf = calculate_pwf(discount_rate, design_life, is_recurring=True, interval=interval)
        self.amount = self.calculate_cost()

    def calculate_cost(self):
        return self.material_quantity * self.carbon_emission_factor * self.carbon_cost * self.pwf


class RoutineInspectionCost(CostComponent):
    def __init__(self, quantity, rate, discount_rate, design_life):
        super().__init__()
        self.quantity = quantity
        self.rate = rate
        self.discount_rate = discount_rate
        self.design_life = design_life
        self.category = "Economic"
        self.is_initial = False
        self.is_recurring = True
        self.pwf = calculate_pwf(discount_rate, design_life, is_recurring=True)
        self.amount = self.calculate_cost()

    def calculate_cost(self):
        return self.quantity * self.rate * self.pwf


class DemolitionCost(CostComponent):
    def __init__(self, demolition_rate, construction_cost, discount_rate, design_life):
        super().__init__()
        self.demolition_rate = demolition_rate
        self.construction_cost = construction_cost
        self.discount_rate = discount_rate
        self.design_life = design_life
        self.category = "Economic"
        self.is_initial = False
        self.is_recurring = False
        self.pwf = calculate_pwf(discount_rate, design_life, is_recurring=False, future_year=design_life)
        self.amount = self.calculate_cost()

    def calculate_cost(self):
        return self.demolition_rate * self.construction_cost * self.pwf


class RecyclingCost(CostComponent):
    def __init__(self, scrap_value, quantity, discount_rate, design_life):
        super().__init__()
        self.scrap_value = scrap_value
        self.quantity = quantity
        self.discount_rate = discount_rate
        self.design_life = design_life
        self.category = "Economic"
        self.is_initial = False
        self.is_recurring = False
        self.pwf = calculate_pwf(discount_rate, design_life, is_recurring=False, future_year=design_life)
        self.amount = self.calculate_cost()

    def calculate_cost(self):
        return self.scrap_value * self.quantity * self.pwf
