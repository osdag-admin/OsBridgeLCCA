import pandas as pd
from input_data import Input
from cost_components import CostComponent
from src.osbridgelcca.core.cost_components import InitialConstructionCost, InitialCarbonEmissionCost, TimeCost, \
    RoadUserCost


class BridgeLCC:
    """Main class for handling Life Cycle Cost Analysis of bridges."""

    def __init__(self, project_name: str, inputs: Input):
        self.project_name = project_name
        self.inputs = inputs  # Expecting an instance of Input class
        self.outputs = {}  # Initialize output storage

    def calculate_lcc(self):
        """Calculate the total life cycle cost based on input parameters."""
        try:
            material_cost = self.inputs.material_data.quantity * self.inputs.material_data.unit_rate
            maintenance_cost = self.inputs.maintenance_data.periodic_maintenance_rate
            operation_cost = self.inputs.traffic_data.annual_traffic_increase * 5000  # Example formula
            discount_rate = self.inputs.finance_data.discount_rate / 100  # Convert percentage to decimal

            # Simple NPV calculation
            total_cost = (material_cost + maintenance_cost + operation_cost) / (1 + discount_rate)
            self.outputs["total_lcc"] = total_cost
            return total_cost
        except AttributeError as e:
            raise ValueError(f"Missing input parameter: {e}")

    def get_outputs(self):
        """Return computed outputs."""
        return self.outputs

    def tabulate_cost_components(self):
        """Create a Pandas DataFrame for cost components."""
        data = {
            "Sl. No.": list(range(1, 12)) + ["Total"],
            "Cost Component": [
                "Initial costs", "Initial carbon emissions costs", "Time costs",
                "Road user costs due to re-routing", "Carbon emission cost due to re-routing",
                "Periodic maintenance costs", "Periodic maintenance carbon emissions costs",
                "Annual routine inspection costs", "Repair and rehabilitation costs",
                "Demolition and disposal costs", "Recycling costs", "Total life cycle cost"
            ],
            "Cost Amount": [InitialConstructionCost.amount,
                            InitialCarbonEmissionCost.amount,
                            TimeCost.amount,
                            RoadUserCost.amount,
                            82.62, 19.36, 1.5, 17.68, 13.8, 0, 0.84, -2.67, 212.81],
            "Life Cycle Stage": [
                "Initial", "Initial", "Initial", "Initial", "Initial",
                "Use", "Use", "Use", "Use",
                "End", "End", "Total"
            ],
            "Cost Type": [
                "Economic", "Environmental", "Social", "Social", "Environmental",
                "Economic", "Environmental", "Economic", "Economic",
                "Economic", "Economic", "Total"
            ]
        }

        df = pd.DataFrame(data)
        return df

# Example Usage
if __name__ == "__main__":
    from input_data import MaterialData, FinanceData, TrafficData, MaintenanceData, RepairData, DemolitionData, RecycleData, CarbonEmissionData

    material = MaterialData("Steel", "Reinforcement bars", 5000, "kg", 60, "Govt Schedule", 32, 2.5, "EPD Source", 5, 90)
    finance = FinanceData(5.0, 7.5, 1.2)
    carbon = CarbonEmissionData("SSP2", "RCP6", 1200)
    traffic = TrafficData(15, 4000, "Plain", "Urban", 10, {"Car": 50, "Truck": 30, "Bus": 20})
    maintenance = MaintenanceData(0.55, 1.0, 10, 5, 1)
    repair = RepairData("Component-wise repair details")
    demolition = DemolitionData(10)
    recycle = RecycleData(80, 10000, 5000)

    project_input = Input(material, finance, carbon, traffic, maintenance, repair, demolition, recycle)
    bridge = BridgeLCC("Bridge A", project_input)

    print("Total LCC:", bridge.calculate_lcc())
    print("\nCost Components Table:")
    print(bridge.tabulate_cost_components())
