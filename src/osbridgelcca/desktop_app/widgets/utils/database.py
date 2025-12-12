import sqlite3
from typing import List, Dict, Tuple
from .cost_component import ( BearingAndExpansionJointReplacementCost, CarbonEmissionDueToRerouting, DemolitionCarbonCost, DemolitionCarbonReroutingCost,
                                InitialConstructionCost, MajorInspectionCost, MajorRepairCost,
                                MajorRepairRelCarbonEmissionCost, TimeCost, RoadUserCost,
                                AdditionalCarbonEmissionCost, PeriodicMaintenanceCost,
                                RoutineInspectionCost, RepairAndRehabilitationCost, 
                                DemolitionCost, RecyclingCost, ReconstructionCost,
                                PeriodicMaintenanceCarbonCost
)
from .data import *
from .IRC_SP_30 import IRC_SP_30

# from .core.main import calc_voc


class DatabaseManager:
    """Database manager for Structure Works Data"""
    
    def __init__(self, db_path: str = "widgets/utils/structure_works.db", recreate: bool = True):
        """
        Initialize database connection and create tables if they don't exist
        
        Args:
            db_path: Path to the database file
            recreate: If True, delete existing database and create fresh. If False, use existing database.
        """

        # Instantiate IRC_SP_30
        self.irc_sp_30 = IRC_SP_30()

        self.db_path = db_path
        self.conn = None
        self.create_database(recreate=recreate)

        # Data from UI
        self.financial_data = {
            KEY_DISCOUNT_RATE_IA: 0.067,
            KEY_INFLATION_RATE: 0.0515,
            KEY_INTEREST_RATE: 0.0775,
            KEY_INVESTMENT_RATIO: 0.5,
            KEY_DESIGN_LIFE: 50,
            KEY_CONSTR_TIME: 5,
            KEY_ANALYSIS_PERIOD: 50,
        }
        self.carbon_emission_cost_data = {}
        self.daily_average_traffic_data = {
            KEY_TWO_WHEELER: 100,
            KEY_SMALL_CARS: 100,
            KEY_ORDINARY_BUS: 100,
            KEY_DELUXE_BUS: 100,
            KEY_LCV: 100,
            KEY_HCV: 100,
            KEY_MCV: 100
        }
        self.maintainance_and_repair_data = {}
        self.demolition_and_recycling_data = {}
        self.traffic_data = {
            KEY_ALTER_ROAD_CARRIAGEWAY: "Two Lane Roads", # String
            KEY_ADDIT_REROUTING_DISTANCE: 6.0,
            KEY_ADDIT_TRAVEL_TIME: 1.5, # hours
            KEY_ROAD_ROUGHNESS: 3000, # String
            KEY_ROAD_RISE: 2000, # String
            KEY_ROAD_FALL: 1000, # String
            KEY_ROAD_TYPE: "Urban Road", # String
            KEY_CRASH_RATE: 30.0
        }
        self.accident_distribution = {
            KEY_MINOR_INJURY: 60.0,
            KEY_MAJOR_INJURY: 20.0,
            KEY_FATAL: 20.0
        }
        self.vehicle_distribution = {
            KEY_TWO_WHEELER: 5.0,
            KEY_SMALL_CARS: 10.0,
            KEY_BIG_CARS: 50.0,
            KEY_ORDINARY_BUS: 10.0,
            KEY_DELUXE_BUS: 10.0,
            KEY_LCV: 5.0,
            KEY_MCV: 5.0,
            KEY_HCV: 5.0
        }

        # Constants
        self.PETROL_DIESEL_RATIO_SM_CARS = {
            KEY_PETROL: 0.7,
            KEY_DIESEL: 0.3
        }
        self.PETROL_DIESEL_RATIO_BG_CARS = {
            KEY_PETROL: 0.3,
            KEY_DIESEL: 0.7
        }
        self.WORK_ZONE_MULTIPLIER = 1.0

        # Total Costs
        self.results = {
            COST_TOTAL_INIT_CONST: 7724184.66,
            COST_TOTAL_SUPERSTRUCTURE: None,
            COST_TOTAL_INIT_CARBON_EMISSION: 1217668.46,
            COST_TIME: None,
            COST_CARBON_EMISSION_REROUTING_INIT: None,
            COST_TOTAL_ROUTINE_INSPECTION: None,
            COST_PERIODIC_MAINTAINANCE: None,
            COST_MAJOR_INSPECTION: None,
            COST_MAJOR_REPAIR: None,
            COST_PERIODIC_MAINTAINANCE_CARBON_EMISSION: None,
            COST_MAJOR_REPAIR_RELATED_CARBON_EMISSION: None,
            COST_CARBON_EMISSION_RR_DURING_MAJOR_REPAIR: None,
            COST_DEMOLITION_DISPOSAL: None,
            COST_DEMOLITION_DISPOSAL_CARBON: None,
            COST_DEMOLITION_DISPOSAL_CARBON_REROUTING: None,
            COST_RECYCLING: None,

            COST_TOTAL_ROAD_USER: None,
            COST_ADDITIONAL_CARBON_EMISSION: None,
            COST_REPAIR_REHAB: None,
            COST_RECONSTRUCTION: None
        }

        # Some Constants
        self.CO2_EMISSION_PER_KM = 0.1213
        self.WORKING_DAYS_IN_MONTH = 26
        # Duration of Major Repairs (Month)
        self.DURATION_MAJOR_REPAIRS = 3
        # Duration of Replacement (Month)
        self.DURATION_REPLACEMENT = 2/self.WORKING_DAYS_IN_MONTH
        # Duration of Demolition and Disposal (Month)
        self.DURATION_DEMOLITION_DISPOSAL = 2
    
    def create_database(self, recreate: bool = True):
        """
        Create database tables with proper schema
        
        Args:
            recreate: If True, delete existing database and create fresh
        """
        import os
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Delete existing database if recreate is True
        if recreate and os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"Deleted existing database: {self.db_path}")
        
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Create struct_works_data table first with comp_id as PRIMARY KEY
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS struct_works_data (
                comp_id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK(type IN (
                    'Foundation', 
                    'Sub-Structure', 
                    'Super-Structure', 
                    'Miscellaneous'
                )),
                component_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create component table with comp_id as FOREIGN KEY
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS component (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comp_id INTEGER NOT NULL,
                type_material TEXT NOT NULL,
                grade TEXT NOT NULL,
                quantity REAL NOT NULL DEFAULT 0,
                unit TEXT NOT NULL,
                rate REAL NOT NULL DEFAULT 0.0,
                rate_data_source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (comp_id) REFERENCES struct_works_data(comp_id) ON DELETE CASCADE
            )
        ''')

        # Create financial_data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financial_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                real_discount_rate REAL NOT NULL,
                interest_rate REAL NOT NULL,
                investment_ratio REAL NOT NULL,
                duration_of_study INTEGER NOT NULL,
                time_of_project INTEGER NOT NULL,       
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       
            )
        ''')

        cursor.execute('''
             CREATE TABLE IF NOT EXISTS carbon_emission(
                type_material TEXT NOT NULL,
                grade TEXT NOT NULL,
                quantity REAL NOT NULL DEFAULT 0,
                unit TEXT NOT NULL,
                emission_factor REAL NOT NULL,
                embodied REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (type_material, grade, unit)
            )
        ''')
        
        self.conn.commit()
    
    def insert_structure_work(self, work_type: str, component_type: str) -> int:
        """
        Insert a new structure work entry
        
        Args:
            work_type: Type of structure work (Foundation, Sub-Structure, etc.)
            component_type: Type of component (e.g., 'Pile', 'Beam', etc.)
        
        Returns:
            comp_id: The auto-generated component ID (PRIMARY KEY)
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO struct_works_data (type, component_type)
            VALUES (?, ?)
        ''', (work_type, component_type))
        
        comp_id = cursor.lastrowid
        self.conn.commit()
        return comp_id
    
    def insert_component(self, comp_id: int, type_material: str, grade: str, 
                        quantity: float, unit: str, rate: float, 
                        rate_data_source: str = None) -> int:
        """
        Insert a new component (material row)
        
        Args:
            comp_id: Foreign key referencing struct_works_data.comp_id
            type_material: Type of material (e.g., 'Steel Re', 'Concrete')
            grade: Material grade (e.g., 'Fe415', 'M25')
            quantity: Quantity of material
            unit: Unit of measurement
            rate: Rate per unit
            rate_data_source: Source of rate data (optional)
        
        Returns:
            id: The ID of the newly created component row
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO component (comp_id, type_material, grade, quantity, unit, rate, rate_data_source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (comp_id, type_material, grade, quantity, unit, rate, rate_data_source))
        
        component_id = cursor.lastrowid
        self.conn.commit()
        return component_id
    
    def input_data_row(self, work_type: str, rows_data: List[Dict]) -> List[int]:
        """
        Input complete data row with structure work and multiple components
        
        Args:
            work_type: Type of structure work (Foundation, Sub-Structure, etc.)
            rows_data: List of dictionaries containing component data
        
        Returns:
            List of comp_id values created in struct_works_data for the provided rows
        
        Example:
            rows_data = [
                [
                    {
                        KEY_COMPONENT: "Pile",
                        KEY_TYPE: "Steel Re",
                        KEY_GRADE: "Fe415",
                        KEY_QUANTITY: "100",
                        KEY_UNIT_M3: "cum",
                        KEY_RATE: "5000.00",
                        KEY_RATE_DATA_SOURCE: "Market Survey"
                    },
                    ...
                ],
                ...
            ]
        """
        if not rows_data:
            raise ValueError("rows_data cannot be empty")
        
        created_comp_ids: List[int] = []
        for row in rows_data:
            # Get component type from first row
            component_type = row[0].get(KEY_COMPONENT, "Unknown")

            # Create structure work entry - this generates comp_id
            comp_id = self.insert_structure_work(work_type, component_type)
            created_comp_ids.append(comp_id)

            # Insert all component rows with the generated comp_id
            for row_dict in row:
                type_material = row_dict.get(KEY_TYPE, "")
                grade = row_dict.get(KEY_GRADE, "")
                quantity = float(row_dict.get(KEY_QUANTITY, 0))
                unit = row_dict.get(KEY_UNIT_M3, "")
                rate = float(row_dict.get(KEY_RATE, 0.0))
                rate_data_source = row_dict.get(KEY_RATE_DATA_SOURCE, "")
                
                self.insert_component(
                    comp_id=comp_id,
                    type_material=type_material,
                    grade=grade,
                    quantity=quantity,
                    unit=unit,
                    rate=rate,
                    rate_data_source=rate_data_source
                )
        
        return created_comp_ids

    def replace_structure_work_rows(self, work_type: str, rows_data: List[Dict], old_comp_ids: List[int]) -> List[int]:
        """
        Delete existing structure work rows by comp_id and insert new rows.
        
        Args:
            work_type: Type of structure work (Foundation, Sub-Structure, etc.)
            rows_data: New rows data to insert (same structure as input_data_row)
            old_comp_ids: List of comp_id values to delete before inserting new data
        
        Returns:
            List[int]: Newly created comp_id values for the inserted data
        """
        if old_comp_ids:
            for comp_id in old_comp_ids:
                self.delete_structure_work(comp_id)
                self.delete_component(comp_id)
        
        return self.input_data_row(work_type, rows_data)

    def delete_structure_work(self, comp_id: int):
        """Delete a structure work and all its components (CASCADE)"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM struct_works_data WHERE comp_id = ?', (comp_id,))
        self.conn.commit()
    
    def delete_component(self, component_id: int):
        """Delete a specific component by its ID"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM component WHERE comp_id = ?', (component_id,))
        self.conn.commit()

    def get_all_materials_info(self) -> List[Dict]:
        """
        Retrieve all material types, grades, and quantities from the component table
        
        Returns:
            List of dictionaries containing material information with keys:
            - type_material: The type of material
            - grade: The grade of the material
            - quantity: The quantity used
            - unit: The unit of measurement
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT type_material, grade, quantity, unit, rate
            FROM component
            ORDER BY type_material, grade
        ''')
        
        results = []
        for row in cursor.fetchall():
            material_info = {
                KEY_TYPE: row[0],
                KEY_GRADE: row[1],
                KEY_QUANTITY: row[2],
                KEY_UNIT_M3: row[3],
                KEY_RATE: row[4]
            }
            results.append(material_info)
        
        return results
    
    def get_all_superstructures_data(self) -> List[Dict]:
        """
        Retrieve all material types, grades, and quantities from the component table
        only for superstructure
        
        Returns:
            List of dictionaries containing material information with keys:
            - type_material: The type of material
            - grade: The grade of the material
            - quantity: The quantity used
            - unit: The unit of measurement
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT comp_id, type_material, grade, quantity, unit, rate
            FROM component
            WHERE comp_id IN
            (SELECT comp_id
             FROM struct_works_data
             WHERE type = ?);
        ''', (KEY_SUPERSTRUCTURE,))
        
        results = []
        for row in cursor.fetchall():
            material_info = {
                KEY_TYPE: row[1],
                KEY_GRADE: row[2],
                KEY_QUANTITY: row[3],
                KEY_UNIT_M3: row[4],
                KEY_RATE: row[5]
            }
            results.append(material_info)
        
        return results

    def get_unique_materials_and_grades(self) -> List[List[str]]:
        """
        Retrieve all unique material and grade pairs from the component table
        as a list of lists: [[type_material, grade], ...]
        """

        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT DISTINCT type_material, grade, unit, SUM(quantity) as total_quantity
            FROM component
            GROUP BY type_material, grade, unit
        ''')


        output =[[row[0], row[1], row[2], row[3]] for row in cursor.fetchall()]
        p = []
        for item in output:
            if item[1]:
                s = item[0] + " (" + item[1] + ")"
            else:
                s = item[0]
            p.append([s, item[2], item[3], item[0], item[1]])
        return p

    def insert_carbon_emission_data(self, data_list):
        """
        Insert multiple records into CARBON_EMISSION table
        
        Args:
            data_list: List of dictionaries containing carbon emission data
        """
        try:
            cursor = self.conn.cursor()
            
            # SQL insert statement
            insert_query = '''
                INSERT INTO CARBON_EMISSION 
                (type_material, grade, quantity, unit, emission_factor, embodied)
                VALUES (?, ?, ?, ?, ?, ?)
            '''

            # Prepare data for batch insert
            records = []
            for data in data_list:
                print(data)
                record = (
                    data.get(KEY_TYPE, ''),
                    data.get(KEY_GRADE, ''),
                    float(data.get(KEY_QUANTITY, 0)),
                    data.get(KEY_UNIT_M3, ''),
                    float(data.get(KEY_CARBON_EMISSION_FACTOR, 0)),
                    float(data.get(KEY_EMBODIED_CARBON_ENERGY, 0))
                )
                records.append(record)
            # Execute batch insert
            cursor.executemany(insert_query, records)
            self.conn.commit()
            
            print(f"Successfully inserted {len(records)} records")
            return True
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.conn.rollback()
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def get_carbon_emission_data(self) -> List[Dict]:        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT type_material, unit, quantity, emission_factor
            FROM carbon_emission
        ''')

        results = []
        for row in cursor.fetchall():
            material_info = {
                KEY_TYPE: row[0],
                KEY_UNIT_M3: row[1],
                KEY_QUANTITY: row[2],
                KEY_RATE: row[3],
                KEY_CARBON_EMISSION_FACTOR: row[3]
            }
            results.append(material_info)
        return results

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    #========================Calculations========================

    #=================Initial-Stage-Cost-Start===================
    # 1. Initial Cost Calculation 
    def calculate_total_initial_cost(self) -> float:
        obj = InitialConstructionCost()
        data = self.get_all_materials_info()
        total_cost = 0.0
        for item in data:
            cost = obj.calculate_cost(
                quantity=item.get(KEY_QUANTITY),
                rate=item.get(KEY_RATE)
            )
            print(f"\nMaterial={item.get(KEY_TYPE)}\nQuantity={item.get(KEY_QUANTITY)}\nRate={item.get(KEY_RATE)}\nCost={cost}")
            total_cost += cost

        print("\n1.Total Initial Construction Cost:", total_cost)

        # Store Total Initial cost
        self.results[COST_TOTAL_INIT_CONST] = total_cost
        return total_cost

    # 2. Initial Carbon Emission Cost
    def carbon_emission_cost(self) -> float:

        # Get carbon emission data from the database
        data = self.get_carbon_emission_data()

        # SCC
        if self.carbon_emission_cost_data.get(KEY_SOURCE) == SCC_K_Ricke_et_al:
            SCC = self.carbon_emission_cost_data.get(KEY_SCC) * self.carbon_emission_cost_data.get(KEY_USD_T_INR)
        else:
            SCC = self.carbon_emission_cost_data.get(KEY_SCC)
        
        print(f"\nSCC considered is.\nSource={self.carbon_emission_cost_data.get(KEY_SOURCE)}\nSCC={SCC}")

        total_carbon_emission_cost= 0.0
        for item in data:
            qty = float(item.get(KEY_QUANTITY))
            emission_factor = float(item.get(KEY_CARBON_EMISSION_FACTOR))
            carbon_emission_cost = (qty * emission_factor) * SCC
            total_carbon_emission_cost += carbon_emission_cost
            print(f"Carbon Emission Cost for {item.get(KEY_TYPE)}:", carbon_emission_cost)
        
        print("\n2.Total Carbon Emission Cost:", total_carbon_emission_cost)
        self.results[COST_TOTAL_INIT_CARBON_EMISSION] = total_carbon_emission_cost
        return total_carbon_emission_cost
    
    # 3. Time Cost
    def calculate_time_cost(self) -> float:

        component = TimeCost()
        cost = component.calculate_cost(
            construction_cost=self.results.get(COST_TOTAL_INIT_CONST),
            interest_rate=self.financial_data.get(KEY_INTEREST_RATE),
            time=self.financial_data.get(KEY_CONSTR_TIME),
            investment_ratio=self.financial_data.get(KEY_INVESTMENT_RATIO)
        )
        print("\n3.Time Cost: ", cost)
        # Save the time cost
        self.results[COST_TIME] = cost
        return cost

    # Helper function to get total traffic
    def _get_total_traffic(self)->float:
        total_traffic = 0
        for count in self.daily_average_traffic_data.values():
            total_traffic += count
        return total_traffic

    # 5. Carbon Emission due to Rerouting during Initial Construction
    def init_carbon_emission_rerouting(self) -> float:

        total_traffic = self._get_total_traffic()
        rerouting_dist = self.traffic_data.get(KEY_ADDIT_REROUTING_DISTANCE)
        
        init_const_time = self.financial_data.get(KEY_CONSTR_TIME)
        SCC = self.carbon_emission_cost_data.get(KEY_SCC)
        cost = total_traffic * init_const_time * 12 * self.WORKING_DAYS_IN_MONTH * SCC * self.CO2_EMISSION_PER_KM * rerouting_dist

        self.results[COST_CARBON_EMISSION_REROUTING_INIT] = cost
        print(f"\n5.Carbon Emission due to Rerouting during Initial Construction. {cost}")
        return cost
    
    #=================Initial-Stage-Cost-End===================

    #=================Use-Stage-Cost-Start=====================
    # 1. Routine Inspection Cost Calculation
    def routine_inspection_cost(self) -> float:

        component = RoutineInspectionCost()

        cost = component.calculate_cost(
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            init_construction_cost=self.results.get(COST_TOTAL_INIT_CONST),
            cost=self.maintainance_and_repair_data.get(KEY_ROUTINE_INSP_COST),
            frequency=self.maintainance_and_repair_data.get(KEY_ROUTINE_INSP_FREQ),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA),
            design_life=self.financial_data.get(KEY_DESIGN_LIFE)
        )

        self.results[COST_TOTAL_ROUTINE_INSPECTION] = cost
        print("\n1.Routine Inspection Cost: ", cost)
        return cost


    # 2. Periodic Maintainance Cost
    def periodic_maintainance_cost(self) -> float:

        component = PeriodicMaintenanceCost()

        cost = component.calculate_cost(
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            init_construction_cost=self.results.get(COST_TOTAL_INIT_CONST),
            cost=self.maintainance_and_repair_data.get(KEY_PERIODIC_MAINT_COST),
            frequency=self.maintainance_and_repair_data.get(KEY_PERIODIC_MAINT_FREQ),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA),
            design_life=self.financial_data.get(KEY_DESIGN_LIFE)
        )

        self.results[COST_PERIODIC_MAINTAINANCE] = cost
        print("\n2.Periodic Maintenance Cost: ", cost)
        return cost
    
    # 3. Periodic Maintenance Carbon Emission Cost Calculation
    def periodic_maintainance_carbon_emission_cost(self):

        component = PeriodicMaintenanceCarbonCost()

        cost = component.calculate_cost(
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            total_carbon_emission_cost=self.results.get(COST_TOTAL_INIT_CARBON_EMISSION),
            cost=self.maintainance_and_repair_data.get(KEY_PERIODIC_MAINT_COST),
            frequency=self.maintainance_and_repair_data.get(KEY_PERIODIC_MAINT_FREQ),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA),
            design_life=self.financial_data.get(KEY_DESIGN_LIFE)
        )

        self.results[COST_PERIODIC_MAINTAINANCE_CARBON_EMISSION] = cost
        print("\n3.Periodic Maintenance Carbon Emission Cost:", cost)
        return cost
    
    # 4. Major Inspection Cost
    def major_inspection_cost(self) -> float:

        component = MajorInspectionCost()

        cost = component.calculate_cost(
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            init_construction_cost=self.results.get(COST_TOTAL_INIT_CONST),
            cost=self.maintainance_and_repair_data.get(KEY_MAJOR_INSP_COST),
            frequency=self.maintainance_and_repair_data.get(KEY_MAJOR_INSP_FREQ),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA),
            design_life=self.financial_data.get(KEY_DESIGN_LIFE)
        )

        self.results[COST_MAJOR_INSPECTION] = cost
        print("\n4.Major Inspection Cost: ", cost)
        return cost
    
    # 5. Major Repair Cost
    def major_repair_cost(self) -> float:

        component = MajorRepairCost()

        cost = component.calculate_cost(
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            init_construction_cost=self.results.get(COST_TOTAL_INIT_CONST),
            cost=self.maintainance_and_repair_data.get(KEY_MAJOR_REPAIR_COST),
            frequency=self.maintainance_and_repair_data.get(KEY_MAJOR_REPAIR_FREQ),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA),
            design_life=self.financial_data.get(KEY_DESIGN_LIFE)
        )

        self.results[COST_MAJOR_REPAIR] = cost
        print("\n5.Major Repair Cost: ", cost)
        return cost
    
    # 6. Major Repair Related Carbon Emisson Cost
    def major_repair_related_carbon_emission_cost(self):

        component = MajorRepairRelCarbonEmissionCost()

        cost = component.calculate_cost(
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            total_carbon_emission_cost=self.results.get(COST_TOTAL_INIT_CARBON_EMISSION),
            cost=self.maintainance_and_repair_data.get(KEY_MAJOR_REPAIR_COST),
            frequency=self.maintainance_and_repair_data.get(KEY_MAJOR_REPAIR_FREQ),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA),
            design_life=self.financial_data.get(KEY_DESIGN_LIFE)
        )

        self.results[COST_MAJOR_REPAIR_RELATED_CARBON_EMISSION] = cost
        print("\n6.Major Repair Related Carbon Emisson Cost: ", cost)
        return cost
    
    # 8. Carbon Emission due to rerouting during Major Repairs
    def carbon_emission_rerouting_during_major_repairs(self):

        component = CarbonEmissionDueToRerouting()

        total_traffic = self._get_total_traffic()
        SCC = self.carbon_emission_cost_data.get(KEY_SCC)
        rerouting_dist = self.traffic_data.get(KEY_ADDIT_REROUTING_DISTANCE)

        cost = component.calculate_cost(
            additional_rerouting_dist=rerouting_dist,
            duration_major_repair=self.DURATION_MAJOR_REPAIRS,
            working_days_month=self.WORKING_DAYS_IN_MONTH,
            total_traffic=total_traffic,
            scc=SCC,
            co2_emission_per_km=self.CO2_EMISSION_PER_KM,
            repair_freq=self.maintainance_and_repair_data.get(KEY_MAJOR_REPAIR_FREQ),
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA),
            design_life=self.financial_data.get(KEY_DESIGN_LIFE)
        )

        self.results[COST_CARBON_EMISSION_RR_DURING_MAJOR_REPAIR] = cost
        print("\n8.Carbon Emission due to rerouting during Major Repairs: ", cost)
        return cost
    
    # Helper function for 9
    def _calculate_superstructure_cost(self) -> float:
        obj = InitialConstructionCost()
        data = self.get_all_superstructures_data()
        print("\nCalculating Total of SuperStructures")
        total_cost = 0.0
        print(data)
        for item in data:
            print(item.get(KEY_QUANTITY),item.get(KEY_RATE))
            cost = obj.calculate_cost(
                quantity=item.get(KEY_QUANTITY),
                rate=item.get(KEY_RATE)
            )
            print(f"\nMaterial={item.get(KEY_TYPE)}\nQuantity={item.get(KEY_QUANTITY)}\nRate={item.get(KEY_RATE)}\nCost={cost}")
            total_cost += cost

        print("\nTotal SuperStructures Cost:", total_cost)

        # Store Total SuperStructures cost
        self.results[COST_TOTAL_SUPERSTRUCTURE] = total_cost
        return total_cost
    
    # 9. Replacement cost of Bearing and Expansion Joints
    def bearing_expansion_joint_replacement_cost(self) -> float:

        component = BearingAndExpansionJointReplacementCost()
        total_superstructure_cost = self._calculate_superstructure_cost()

        cost = component.calculate_cost(
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            total_superstructure_cost=total_superstructure_cost,
            cost=self.maintainance_and_repair_data.get(KEY_MAJOR_INSP_COST),
            frequency=self.maintainance_and_repair_data.get(KEY_MAJOR_REPAIR_FREQ),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA),
            design_life=self.financial_data.get(KEY_DESIGN_LIFE)
        )

        self.results[COST_MAJOR_INSPECTION] = cost
        print("\n9.Replacement cost of Bearing and Expansion Joints: ", cost)
        return cost

    # 11. Carbon Emission due to rerouting during Replacement
    def carbon_emission_rerouting_during_replacement(self):

        component = CarbonEmissionDueToRerouting()

        total_traffic = self._get_total_traffic()
        SCC = self.carbon_emission_cost_data.get(KEY_SCC)
        rerouting_dist = self.traffic_data.get(KEY_ADDIT_REROUTING_DISTANCE)

        cost = component.calculate_cost(
            additional_rerouting_dist=rerouting_dist,
            duration_major_repair=self.DURATION_REPLACEMENT,
            working_days_month=self.WORKING_DAYS_IN_MONTH,
            total_traffic=total_traffic,
            scc=SCC,
            co2_emission_per_km=self.CO2_EMISSION_PER_KM,
            repair_freq=self.maintainance_and_repair_data.get(KEY_BEARING_EXP_JOINT_REPAIR_FREQ),
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA),
            design_life=self.financial_data.get(KEY_DESIGN_LIFE)
        )

        self.results[COST_CARBON_EMISSION_RR_DURING_REPLACEMENT] = cost
        print("\n11.Carbon Emission due to rerouting during Replacement: ", cost)
        return cost
    #=================Use-Stage-Cost-End=====================
    
    #==========End-Of-Life-Stage-Cost-Start==================
    # Helper function to get sum(quantity*rate) for given Type(Material)
    def _get_total_cost_material(self, type:str)->float:
        obj = InitialConstructionCost()
        data = self.get_all_materials_info()
        total_cost = 0.0
        for item in data:
            if item.get(KEY_TYPE) == type:
                cost = obj.calculate_cost(
                    quantity=item.get(KEY_QUANTITY),
                    rate=item.get(KEY_RATE)
                )
                total_cost += cost
        
        print(f"\nMaterial={type}\nTotal Cost={total_cost}")
        return total_cost
    
    # 1. Demolition and Disposal Cost
    def demolition_and_disposal_cost(self) -> float:
        
        component = DemolitionCost()
        
        cost = component.calculate_cost(
            init_constr_cost=self.results.get(COST_TOTAL_INIT_CONST),
            demolition_disposal_cost=self.demolition_and_recycling_data.get(KEY_DEMOLITION_DISPOSAL_COST),
            analysis_period=self.financial_data.get(KEY_ANALYSIS_PERIOD),
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA)
        )
        self.results[COST_DEMOLITION_DISPOSAL] = cost
        print("\n1.Demolition and Disposal Cost:", cost)
        return cost
    
    # 2. Demolition and Disposal related Carbon Emission
    def demolition_disposal_carbon_emission_cost(self) -> float:
        
        component = DemolitionCarbonCost()
        
        cost = component.calculate_cost(
            init_carbon_emission_cost=self.results.get(COST_TOTAL_INIT_CARBON_EMISSION),
            demolition_disposal_cost=self.demolition_and_recycling_data.get(KEY_DEMOLITION_DISPOSAL_COST),
            analysis_period=self.financial_data.get(KEY_ANALYSIS_PERIOD),
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA)
        )
        self.results[COST_DEMOLITION_DISPOSAL_CARBON] = cost
        print("\n2.Demolition and Disposal related Carbon Emission:", cost)
        return cost
    
    # 4. Carbon Emission due to Rerouting during Demolition and Disposal
    def demolition_disposal_rerouting_carbon_emission_cost(self) -> float:
        
        component = DemolitionCarbonReroutingCost()
        SCC = self.carbon_emission_cost_data.get(KEY_SCC)
        addit_rerouting = self.traffic_data.get(KEY_ADDIT_REROUTING_DISTANCE)

        cost = component.calculate_cost(
            additional_rerouting_dist=addit_rerouting,
            init_constr_cost=self.results.get(COST_TOTAL_INIT_CONST),
            demolition_disposal_time=self.DURATION_DEMOLITION_DISPOSAL,
            working_days_month=self.WORKING_DAYS_IN_MONTH,
            scc=SCC,
            co2_emission_per_km=self.CO2_EMISSION_PER_KM,
            design_life=self.financial_data.get(KEY_DESIGN_LIFE),
            analysis_period=self.financial_data.get(KEY_ANALYSIS_PERIOD),
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA)
        )
        self.results[COST_DEMOLITION_DISPOSAL_CARBON_REROUTING] = cost
        print("\n4.Carbon Emission due to Rerouting during Demolition and Disposal:", cost)
        return cost
    
    # 5. Recycling Cost
    def recycling_cost(self) -> float:
        total_recycling_cost = 0.0

        steel_rebar_cost = self._get_total_cost_material(type="Steel Rebar")
        struct_steel_cost = self._get_total_cost_material(type="Structural Steel")
        pre_stressed_tendons_cost = self._get_total_cost_material(type="Tendons")
        
        component = RecyclingCost()

        #-------Steel-Rebar-Cost-----------------------------------
        steel_rebar_recycle_cost = component.calculate_cost(
            total_material_cost=steel_rebar_cost,
            material_scrap_rate=self.demolition_and_recycling_data.get(KEY_STEEL_REBAR_SCRAP_RATE),
            material_recyclability=self.demolition_and_recycling_data.get(KEY_STEEL_REBAR_RECYLABILITY),
            design_life=self.financial_data.get(KEY_DESIGN_LIFE),
            analysis_period=self.financial_data.get(KEY_ANALYSIS_PERIOD),
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA)
        )
        print(f"\nRecycling Cost of Steel Rebar: ", steel_rebar_recycle_cost)

        #-------Structural-Steel-Cost-----------------------------------
        struct_steel_recycle_cost = component.calculate_cost(
            total_material_cost=struct_steel_cost,
            material_scrap_rate=self.demolition_and_recycling_data.get(KEY_STRUCT_STEEL_SCRAP_RATE),
            material_recyclability=self.demolition_and_recycling_data.get(KEY_STRUCT_STEEL_RECYLABILITY),
            design_life=self.financial_data.get(KEY_DESIGN_LIFE),
            analysis_period=self.financial_data.get(KEY_ANALYSIS_PERIOD),
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA)
        )
        print(f"\nRecycling Cost of Structural Steel: ", struct_steel_recycle_cost)

        #-------PreStressed-Tendons-Cost-----------------------------------
        pre_stressed_tendons_recycle_cost = component.calculate_cost(
            total_material_cost=pre_stressed_tendons_cost,
            material_scrap_rate=self.demolition_and_recycling_data.get(KEY_PS_TENDONS_SCRAP_RATE),
            material_recyclability=self.demolition_and_recycling_data.get(KEY_PS_TENDONS_RECYLABILITY),
            design_life=self.financial_data.get(KEY_DESIGN_LIFE),
            analysis_period=self.financial_data.get(KEY_ANALYSIS_PERIOD),
            inflation_rate=self.financial_data.get(KEY_INFLATION_RATE),
            discount_rate=self.financial_data.get(KEY_DISCOUNT_RATE_IA)
        )
        print(f"\nRecycling Cost of Pre Stressed Tendon Cost: ", pre_stressed_tendons_recycle_cost)

        total_recycling_cost = steel_rebar_recycle_cost + struct_steel_recycle_cost + pre_stressed_tendons_recycle_cost

        self.results[COST_RECYCLING] = total_recycling_cost
        print(f"\n5.Total Recycling Cost: ", total_recycling_cost)
        return total_recycling_cost


    #==========End-Of-Life-Stage-Cost-End====================

    #==========IRC-Road_User-Cost-Start======================
    
    #==========2. Accident-Related-Cost-Start==========

    #==========2.1 Human-Injury-Cost-Start==========
    
    def _no_of_accidents(self) -> float: # Per Day
        crash_rate = self.traffic_data.get(KEY_CRASH_RATE) 
        adt = self._get_total_traffic()
        multiplier = self.WORK_ZONE_MULTIPLIER
        rerouting_dist = self.traffic_data.get(KEY_ADDIT_REROUTING_DISTANCE)
        return crash_rate * adt * multiplier * rerouting_dist * (10**-6)
    
    def _accident_in_constr_time(self) -> float:
        no_of_accidents = self._no_of_accidents()
        month = self.financial_data.get(KEY_CONSTR_TIME) * 12
        days = self.WORKING_DAYS_IN_MONTH * month
        return no_of_accidents * days

    def _wpi_adj_economic_cost_of_accident_category(self, accident_category:str) -> float:
        wpi = self.irc_sp_30._get_wpi(table=TABLE_WPI_MEDICAL,
                                       column=accident_category,
                                       current_year=2024, # Hard Coded
                                       base_year=BASE_YEAR)
        economic_cost_of_accident = self.irc_sp_30._get_accident_cost(accident_category)
        return economic_cost_of_accident * wpi

    def _count_accident_type(self, accident_category:str) -> float:
        accident_dist = self.accident_distribution.get(accident_category)
        return self._accident_in_constr_time() * accident_dist

    def _injury_cost(self, accident_category:str) -> float:
        cost = self._wpi_adj_economic_cost_of_accident_category(accident_category)
        return cost * self._count_accident_type(accident_category)
    
    def total_human_injury_cost(self) -> float:
        cost = 0.0
        for injury in [KEY_MINOR_INJURY, KEY_MAJOR_INJURY, KEY_FATAL]:
            cost += self._injury_cost(injury)
        return cost
    #==========2.1 Human-Injury-Cost-End==========

    #==========2.2 Vehicle-Damage-Cost-Start==========
    def _wpi_adj_economic_cost_of_quantum_damage(self, vehicle_category:str) -> float:
        wpi = self.irc_sp_30._get_wpi(table=TABLE_VOT,
                                       column=vehicle_category,
                                       current_year=2024, # Hard Coded
                                       base_year=BASE_YEAR)
        economic_cost_of_quantum_damage = self.irc_sp_30._get_vehicle_damage_cost(vehicle_category)
        return economic_cost_of_quantum_damage * wpi
    
    def _count_vehicle_damage(self, vehicle_category:str) -> float:
        vehicle_dist = self.vehicle_distribution.get(vehicle_category)
        return self._accident_in_constr_time() * vehicle_dist

    def _vehicle_damage_cost(self, vehicle_category:str):
        cost = self._wpi_adj_economic_cost_of_quantum_damage(vehicle_category)
        return cost * self._count_vehicle_damage(vehicle_category)

    def total_vehicle_damage_cost(self) -> float:
        cost = 0.0
        for vehicle in [KEY_TWO_WHEELER,
                        KEY_SMALL_CARS,
                        KEY_BIG_CARS,
                        KEY_ORDINARY_BUS,
                        KEY_DELUXE_BUS,
                        KEY_LCV,
                        KEY_HCV,
                        KEY_MCV]:
            cost += self._vehicle_damage_cost(vehicle)
        return cost
    #==========2.2 Vehicle-Damage-Cost-End==========

    def accident_related_cost(self) -> float:
        return self.total_human_injury_cost() + self.total_vehicle_damage_cost()
    #==========2. Accident-Related-Cost-End==========

    #==========3. VOT-Start==========================
    def _wpi_adj_vot(self, vehicle_type:str, type_of_road:str) -> float:
        wpi = self.irc_sp_30._get_wpi(table=TABLE_VOT,
                            column=vehicle_type,
                            current_year=2024, # Hard Coded
                            base_year=BASE_YEAR)
        time_value = self.irc_sp_30._get_vot(column=type_of_road,
                                             vehicle_type=vehicle_type)
        return time_value * wpi
    
    def _vot_per_day(self, vehicle_type: str, type_of_road: str) -> float:
        time_value = self._wpi_adj_vot(vehicle_type=vehicle_type,
                                       type_of_road=type_of_road)
        vehicle_per_day = self.daily_average_traffic_data.get(vehicle_type)
        addit_travel_time = self.traffic_data.get(KEY_ADDIT_TRAVEL_TIME)
        occupancy = self.irc_sp_30._get_occupancy(vehicle_type=vehicle_type)
        return time_value * vehicle_per_day * addit_travel_time * occupancy

    def vot_per_year(self) -> float:
        month = self.financial_data.get(KEY_CONSTR_TIME) * 12
        days = self.WORKING_DAYS_IN_MONTH * month
        road_type = self.traffic_data.get(KEY_ALTER_ROAD_CARRIAGEWAY)

        total_vot = 0.0
        for vehicle_type in self.daily_average_traffic_data.keys():
            total_vot += self._vot_per_day(vehicle_type=vehicle_type,
                                       type_of_road=road_type)

        return total_vot * days

    #==========3. VOT-End============================

    def total_road_user_cost(self) -> float:
        vot = self.vot_per_year()
        accident_cost = self.accident_related_cost()


        ui_inputs = {
            "vehicle_info": self.daily_average_traffic_data,
            # "carriageway_width": 10, ### ONLY REQUIRED WHEN "lane_type" = "EW"
            "rg_roughness_factor": 2000,
            "fl_fall_factor": 0,
            "rs_rise_factor": 0,
            "lane_type": "2L",
            "power_weight_ratio_pwr": {
                "mcv": 8,
                "hcv": 7.22
            }
        }

        

        voc = calc_voc(
            inputs=ui_inputs,
            all_wpi=self.irc_sp_30.getWPI(),
            vehicle_cost=23
        )



    

    #==========IRC-Road_User-Cost-End====================

    # 9. Repair and Rehabilitation Cost Calculation
    def repair_and_rehabilitation_cost(self, total_initial_construction_cost: float, data: List) -> float:
        repair_period = data[5]
        repair_cost_rate = data[2]

        repair_component = RepairAndRehabilitationCost(
            repair_cost_rate=repair_cost_rate,
            construction_cost=total_initial_construction_cost,
            discount_rate=self.discount_rate,
            period=repair_period,
            design_life=self.design_life
        )
        print("\nRepair and Rehabilitation Cost:", repair_component.calculate_cost())  # INR
        return repair_component.calculate_cost()
    
    # 12. Reconstruction Cost Calculation 
    def reconstruction_cost(self, initial_construction_cost: float,
                            demolition_cost: float,
                            carbon_emission_cost: float,
                            time_cost: float,
                            roaduser_cost: float,
                            rerouting_carbon_cost: float) -> float:

        reconstruction_cost = initial_construction_cost
        demolition_cost = demolition_cost
        reconstruction_carbon_cost = carbon_emission_cost
        reconstruction_time_cost = time_cost
        reconstruction_roaduser_cost = roaduser_cost
        reconstruction_rerouting_carbon_cost = rerouting_carbon_cost

        reconstruction_result = 0

        if self.analysis_period > self.design_life:
            reconstruction_component = ReconstructionCost(
                demolition_cost=demolition_cost,
                reconstruction_cost=reconstruction_cost,
                reconstruction_carbon_cost=reconstruction_carbon_cost,
                reconstruction_time_cost=reconstruction_time_cost,
                reconstruction_roaduser_cost=reconstruction_roaduser_cost,
                reconstruction_rerouting_carbon_cost=reconstruction_rerouting_carbon_cost,
                design_life=self.design_life,
                discount_rate=self.discount_rate
            )
            reconstruction_result = reconstruction_component.calculate_cost()
        else:
            reconstruction_result = 0
        print("\nReconstruction Cost:", reconstruction_result)  # INR
        return reconstruction_result
    
if __name__ == "__main__":
    d = DatabaseManager()
    print("vot=",d.vot_per_year())
    print("acccident_cost=",d.accident_related_cost())

        
        