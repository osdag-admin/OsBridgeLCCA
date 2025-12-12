import pandas as pd
from .data import *

class IRC_SP_30:
    def __init__(self):
        """Initialize the dataframes with IRC SP-30 data."""
        self._initialize_dataframes()
    
    def _initialize_dataframes(self):
        """Create and populate all DataFrames with IRC SP-30 data."""
        
        # Table 8: Accident Type Costs (Pg. 17)
        self.accident_type_costs = pd.DataFrame({
            COL_ACCIDENT_CATEGORY: [KEY_FATAL, KEY_MAJOR_INJURY, KEY_MINOR_INJURY],
            COL_COST_INR: [1325049.00, 432651.00, 46680.00]
        }).set_index(COL_ACCIDENT_CATEGORY)
        
        # Table 9: Vehicle Damage Costs (Pg. 18)
        self.vehicle_damage_costs = pd.DataFrame({
            COL_TYPE_OF_VEHICLE: [KEY_TWO_WHEELER, KEY_SMALL_CARS, KEY_BIG_CARS, 
                               KEY_ORDINARY_BUS, KEY_DELUXE_BUS, 
                               KEY_LCV, KEY_MCV, KEY_HCV],
            COL_COST_INR: [ 10194.00, 40088.00, 40088.00, 
                            116585.00, 116585.00, 
                            205483.00, 205483.00, 120494.00]
        }).set_index(COL_TYPE_OF_VEHICLE)
        
        # Table 6: VOT of Passengers (Pg. 16)
        self.vot_of_passengers = pd.DataFrame({
            COL_TYPE_OF_VEHICLE: [KEY_TWO_WHEELER, KEY_SMALL_CARS, KEY_BIG_CARS, 
                               KEY_ORDINARY_BUS, KEY_DELUXE_BUS, 
                               KEY_LCV, KEY_MCV, KEY_HCV],
            KEY_SINGLE_LANE_ROAD: [41.3, 98.5, 98.5, 27.2, 0, 0, 0, 0],
            KEY_INTERMEDIATE_LANE_ROAD: [41.3, 98.5, 98.5, 27.2, 0, 0, 0, 0],
            KEY_TWO_LANE_ROAD: [60.1, 117.3, 117.3, 73.2, 81.6, 0, 0, 0],
            KEY_FOUR_LANE_DIVIDED_ROAD: [60.5, 178.5, 258.0, 73.2, 109.0, 0, 0, 0],
            KEY_SIX_LANE_DIVIDED_ROAD: [60.5, 178.5, 258.0, 73.2, 109.0, 0, 0, 0],
            KEY_FOUR_LANE_DIVIDED_EXPRESSWAY: [60.5, 178.5, 258.0, 73.2, 109.0, 0, 0, 0],
            KEY_SIX_LANE_DIVIDED_EXPRESSWAY: [60.5, 178.5, 258.0, 73.2, 109.0, 0, 0, 0],
            KEY_EIGHT_LANE_DIVIDED_URBAN_EXPRESSWAY: [60.5, 178.5, 258.0, 73.2, 109.0, 0, 0, 0],
            COL_OCCUPANCY: [1.71, 3.23, 4.28, 30.0, 40.0, 2.5, 2.0, 1.5]
        }).set_index(COL_TYPE_OF_VEHICLE)

        # WPI: Medical Accessories for Human Injury Cost
        self.wpi_medical_accessories = pd.DataFrame({
            COL_YEAR: [2019, 2020, 2021, 2022, 2023, 2024],
            KEY_FATAL: [132.5, 135.8, 139.5, 140.5, 142.5, 144.0],
            KEY_MAJOR_INJURY: [132.5, 135.8, 139.5, 140.5, 142.5, 144.0],
            KEY_MINOR_INJURY: [132.5, 135.8, 139.5, 140.5, 142.5, 144.0]
        }).set_index(COL_YEAR)  
        
        # WPI: Travel Time (Table 6, Pg. 16)
        self.wpi_vot = pd.DataFrame({
            COL_YEAR: [2019, 2020, 2021, 2022, 2023, 2024],
            KEY_SMALL_CARS: [121.2, 121.8, 135.0, 151.3, 151.3, 154.0],
            KEY_BIG_CARS: [121.2, 121.8, 135.0, 151.3, 151.3, 154.0],
            KEY_TWO_WHEELER: [121.2, 121.8, 135.0, 151.3, 151.3, 154.0],
            KEY_ORDINARY_BUS: [121.2, 121.8, 135.0, 151.3, 151.3, 154.0],
            KEY_DELUXE_BUS: [121.2, 121.8, 135.0, 151.3, 151.3, 154.0],
            KEY_LCV: [121.2, 121.8, 135.0, 151.3, 151.3, 154.0],
            KEY_HCV: [121.2, 121.8, 135.0, 151.3, 151.3, 154.0],
            KEY_MCV: [121.2, 121.8, 135.0, 151.3, 151.3, 154.0]
        }).set_index(COL_YEAR)
        
        # WPI: Property Damage (Manufacture of parts and accessories for motor vehicles)
        self.wpi_property_damage = pd.DataFrame({
            COL_YEAR: [2019, 2020, 2021, 2022, 2023, 2024],
            KEY_SMALL_CARS: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_BIG_CARS: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_TWO_WHEELER: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_ORDINARY_BUS: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_DELUXE_BUS: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_LCV: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_HCV: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_MCV: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0]
        }).set_index(COL_YEAR)
        
        # WPI: VOC: Fuel Costs (Engine Oil, Other Oil, Grease)
        self.voc_fuel_costs = pd.DataFrame({
            COL_YEAR: [2019, 2020, 2021, 2022, 2023, 2024],
            KEY_PETROL: [85.4, 74.2, 109.9, 159.8, 158.9, 154.3],
            KEY_DIESEL: [94.4, 79.4, 114.7, 183.5, 174.2, 167.4],
            KEY_ENGINE_OIL: [131.2, 134.0, 157.8, 174.7, 188.0, 190.2],
            KEY_OTHER_OIL: [92.5, 78.1, 113.8, 168.2, 160.1, 156.8],
            KEY_GREASE: [92.5, 78.1, 113.8, 168.2, 160.1, 156.8]
        }).set_index(COL_YEAR)
        
        # WPI: Tyre Cost (for each vehicle)
        self.tyre_costs = pd.DataFrame({
            COL_YEAR: [2019, 2020, 2021, 2022, 2023, 2024],
            KEY_SMALL_CARS: [99.2, 98.7, 102.8, 109.9, 111.5, 111.5],
            KEY_BIG_CARS: [99.2, 98.7, 102.8, 109.9, 111.5, 111.5],
            KEY_TWO_WHEELER: [104.0, 102.0, 105.9, 116.4, 119.8, 117.9],
            KEY_ORDINARY_BUS: [97.5, 96.1, 103.2, 110.5, 114.4, 114.1],
            KEY_DELUXE_BUS: [97.5, 96.1, 103.2, 110.5, 114.4, 114.1],
            KEY_LCV: [97.5, 96.1, 103.2, 110.5, 114.4, 114.1],
            KEY_HCV: [97.5, 96.1, 103.2, 110.5, 114.4, 114.1],
            KEY_MCV: [97.5, 96.1, 103.2, 110.5, 114.4, 114.1]
        }).set_index(COL_YEAR)
        
        # WPI: Spare Parts: New Price (Manufacture of parts and accessories for motor vehicles)
        self.spare_parts_costs = pd.DataFrame({
            COL_YEAR: [2019, 2020, 2021, 2022, 2023, 2024],
            KEY_SMALL_CARS: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_BIG_CARS: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_TWO_WHEELER: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_ORDINARY_BUS: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_DELUXE_BUS: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_LCV: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_HCV: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0],
            KEY_MCV: [113.2, 115.5, 120.6, 128.5, 128.2, 129.0]
        }).set_index(COL_YEAR)
        
        # WPI: Fixed and Depreciation Costs: Manufacture of motor vehicles, trailers and semi-trailers
        self.fixed_depreciation_costs = pd.DataFrame({
            COL_YEAR: [2019, 2020, 2021, 2022, 2023, 2024],
            KEY_SMALL_CARS: [113.8, 116.9, 121.1, 127.1, 128.0, 129.6],
            KEY_BIG_CARS: [113.8, 116.9, 121.1, 127.1, 128.0, 129.6],
            KEY_TWO_WHEELER: [113.8, 116.9, 121.1, 127.1, 128.0, 129.6],
            KEY_ORDINARY_BUS: [113.8, 116.9, 121.1, 127.1, 128.0, 129.6],
            KEY_DELUXE_BUS: [113.8, 116.9, 121.1, 127.1, 128.0, 129.6],
            KEY_LCV: [113.8, 116.9, 121.1, 127.1, 128.0, 129.6],
            KEY_HCV: [113.8, 116.9, 121.1, 127.1, 128.0, 129.6],
            KEY_MCV: [113.8, 116.9, 121.1, 127.1, 128.0, 129.6]
        }).set_index(COL_YEAR)
        
        # WPI: Commodity Holding Cost: Fuel & Power
        self.commodity_holding_cost = pd.DataFrame({
            COL_YEAR: [2019, 2020, 2021, 2022, 2023, 2024],
            KEY_SMALL_CARS: [101.7, 93.3, 116.1, 155.2, 152.7, 150.4],
            KEY_BIG_CARS: [101.7, 93.3, 116.1, 155.2, 152.7, 150.4],
            KEY_TWO_WHEELER: [101.7, 93.3, 116.1, 155.2, 152.7, 150.4],
            KEY_ORDINARY_BUS: [101.7, 93.3, 116.1, 155.2, 152.7, 150.4],
            KEY_DELUXE_BUS: [101.7, 93.3, 116.1, 155.2, 152.7, 150.4],
            KEY_LCV: [101.7, 93.3, 116.1, 155.2, 152.7, 150.4],
            KEY_HCV: [101.7, 93.3, 116.1, 155.2, 152.7, 150.4],
            KEY_MCV: [101.7, 93.3, 116.1, 155.2, 152.7, 150.4]
        }).set_index(COL_YEAR)
        
        # WPI: Passenger and Crew Costs
        self.passenger_crew_costs = pd.DataFrame({
            COL_YEAR: [2019, 2020, 2021, 2022, 2023, 2024],
            KEY_PASSENGER_COST: [138.58, 147.91, 155.33, 166.94, 176.38, 184.27],
            KEY_CREW_COST: [118.07, 131.77, 145.91, 159.05, 160.28, 164.18]
        }).set_index(COL_YEAR)
    
    # ==================== Get Methods ====================
    
    def _get_accident_cost(self, category: str) -> float:
        """
        Get the economic cost for a specific accident category.
        
        Args:
            category: 'Fatal', 'Major Injury', or 'Minor Injury'
        
        Returns:
            Economic cost in INR
        """
        try:
            return float(self.accident_type_costs.loc[category, COL_COST_INR])
        except KeyError:
            raise ValueError(f"Invalid accident category: '{category}'. "
                           f"Valid options: {list(self.accident_type_costs.index)}")
    
    def _get_vehicle_damage_cost(self, vehicle_type: str) -> float:
        """
        Get the economic cost of vehicle damage.
        
        Args:
            vehicle_type: e.g., 'Two Wheeler', 'Small Cars', 'LCV'
        
        Returns:
            Economic cost in INR
        """
        try:
            return float(self.vehicle_damage_costs.loc[vehicle_type, COL_COST_INR])
        except KeyError:
            raise ValueError(f"Invalid vehicle type: '{vehicle_type}'. "
                           f"Valid options: {list(self.vehicle_damage_costs.index)}")
    
    def _get_wpi(self, table: str, column: str, current_year: int, base_year: int) -> float:
        """
        Calculate WPI ratio between current and base year.
        
        Args:
            table: 'medical' or 'vot'
            column: Column name (lowercase with underscores)
            current_year: Target year
            base_year: Reference year (default: 2019)
        
        Returns:
            WPI ratio (current/base)
        """
        # Select the appropriate DataFrame
        if table == TABLE_WPI_MEDICAL:
            df = self.wpi_medical_accessories
        elif table == TABLE_VOT:
            df = self.wpi_vot
        else:
            raise ValueError(f"Invalid table: '{table}'. Use {TABLE_WPI_MEDICAL} or {TABLE_VOT}")
        
        try:
            cur_value = df.loc[current_year, column]
            base_value = df.loc[base_year, column]
            return float(cur_value / base_value)
        except KeyError as e:
            raise ValueError(f"Year or column not found: {e}")
    
    def _get_vot(self, vehicle_type: str, column: str) -> float:
        """
        Get Value of Travel Time for specific vehicle and road type.
        
        Args:
            vehicle_type: e.g., 'Two Wheeler', 'Small Car', 'Big Car'
            road_type: Road type (lowercase with underscores)
        
        Returns:
            VOT value in INR per hour
        """
        try:
            return float(self.vot_of_passengers.loc[vehicle_type, column])
        except KeyError:
            raise ValueError(f"Invalid vehicle type '{vehicle_type}' or "
                           f"column '{column}'")
    
    def _get_occupancy(self, vehicle_type: str) -> float:
        """
        Get average occupancy for a vehicle type.
        
        Args:
            vehicle_type: e.g., 'Two Wheeler', 'Small Car'
        
        Returns:
            Average occupancy (persons per vehicle)
        """
        try:
            return float(self.vot_of_passengers.loc[vehicle_type, COL_OCCUPANCY])
        except KeyError:
            raise ValueError(f"Invalid vehicle type: '{vehicle_type}'")  
        
    def getWPI(self, year: int):
        """
        Get the WPI of all relevant items for a given year, relative to BASE_YEAR.

        Returns:
            dict: Nested dictionary of WPI values (current_year / BASE_YEAR)
        """

        wpi_dict = {"year": year, "WPI": {}}

        def calc_ratio(df, col):
            try:
                return float(df.loc[year, col] / df.loc[BASE_YEAR, col])
            except KeyError:
                return None

        # ------------------------------------------------
        # 1. Fuel Costs
        # ------------------------------------------------
        wpi_dict["WPI"]["fuelCost"] = {
            col: calc_ratio(self.voc_fuel_costs, col)
            for col in self.voc_fuel_costs.columns
        }

        # ------------------------------------------------
        # 2. Vehicle Costs – separated categories
        # ------------------------------------------------
        wpi_dict["WPI"]["vehicleCost"] = {
            "propertyDamage": {
                col: calc_ratio(self.wpi_property_damage, col)
                for col in self.wpi_property_damage.columns
            },
            "tyreCost": {
                col: calc_ratio(self.tyre_costs, col)
                for col in self.tyre_costs.columns
            },
            "spareParts": {
                col: calc_ratio(self.spare_parts_costs, col)
                for col in self.spare_parts_costs.columns
            },
            "fixedDepreciation": {
                col: calc_ratio(self.fixed_depreciation_costs, col)
                for col in self.fixed_depreciation_costs.columns
            }
        }

        # ------------------------------------------------
        # 3. Commodity Holding Cost
        # ------------------------------------------------
        wpi_dict["WPI"]["commodityHoldingCost"] = {
            col: calc_ratio(self.commodity_holding_cost, col)
            for col in self.commodity_holding_cost.columns
        }

        # ------------------------------------------------
        # 4. Passenger & Crew Costs
        # ------------------------------------------------
        wpi_dict["WPI"]["passengerCrewCost"] = {
            col: calc_ratio(self.passenger_crew_costs, col)
            for col in self.passenger_crew_costs.columns
        }

        # ------------------------------------------------
        # 5. Medical Accessories (Fatal / Major / Minor)
        # ------------------------------------------------
        wpi_dict["WPI"]["medicalCost"] = {
            col: calc_ratio(self.wpi_medical_accessories, col)
            for col in self.wpi_medical_accessories.columns
        }

        # ------------------------------------------------
        # 6. Travel Time (VOT)
        # ------------------------------------------------
        wpi_dict["WPI"]["votCost"] = {
            col: calc_ratio(self.wpi_vot, col)
            for col in self.wpi_vot.columns
        }

        return wpi_dict

if __name__ == "__main__":
    irc_sp_30 = IRC_SP_30()
    print(irc_sp_30.accident_type_costs)
    print(irc_sp_30.vehicle_damage_costs)
    print(irc_sp_30.wpi_medical_accessories)
    print(irc_sp_30.wpi_vot)
    print(irc_sp_30.vot_of_passengers)
    print(irc_sp_30.getWPI(2024)) # add this
