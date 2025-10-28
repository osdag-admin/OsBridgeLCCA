import sqlite3
from typing import List, Dict, Tuple
from .data import *

class DatabaseManager:
    """Database manager for Structure Works Data"""
    
    def __init__(self, db_path: str = "widgets/utils/structure_works.db", recreate: bool = True):
        """
        Initialize database connection and create tables if they don't exist
        
        Args:
            db_path: Path to the database file
            recreate: If True, delete existing database and create fresh. If False, use existing database.
        """
        self.db_path = db_path
        self.conn = None
        self.create_database(recreate=recreate)
    
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
    
    def input_data_row(self, work_type: str, rows_data: List[Dict]) -> int:
        """
        Input complete data row with structure work and multiple components
        
        Args:
            work_type: Type of structure work (Foundation, Sub-Structure, etc.)
            rows_data: List of dictionaries containing component data
        
        Returns:
            comp_id: The auto-generated component ID from struct_works_data
        
        Example:
            rows_data = [
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
            ]
        """
        if not rows_data:
            raise ValueError("rows_data cannot be empty")
        
        for row in rows_data:
            # Get component type from first row
            component_type = row[0].get(KEY_COMPONENT, "Unknown")

            # Create structure work entry - this generates comp_id
            comp_id = self.insert_structure_work(work_type, component_type)

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
    
    def retrieve_data_by_comp_id(self, comp_id: int) -> Dict:
        """
        Retrieve complete data for a specific comp_id in the same format as input
        
        Args:
            comp_id: The structure work ID (PRIMARY KEY)
        
        Returns:
            Dictionary containing structure work info and list of component rows
        """
        cursor = self.conn.cursor()
        
        # Get structure work data
        cursor.execute('''
            SELECT comp_id, type, component_type, created_at, updated_at
            FROM struct_works_data
            WHERE comp_id = ?
        ''', (comp_id,))
        
        struct_work = cursor.fetchone()
        if not struct_work:
            return None
        
        # Get all components for this comp_id
        cursor.execute('''
            SELECT id, type_material, grade, quantity, unit, rate, rate_data_source
            FROM component
            WHERE comp_id = ?
            ORDER BY id
        ''', (comp_id,))
        
        components = cursor.fetchall()
        
        # Format as list of dictionaries (same as input format)
        rows_data = []
        for comp in components:
            row_dict = {
                KEY_COMPONENT: struct_work[2],  # component_type
                KEY_TYPE: comp[1],  # type_material
                KEY_GRADE: comp[2],  # grade
                KEY_QUANTITY: str(comp[3]),  # quantity
                KEY_UNIT_M3: comp[4],  # unit
                KEY_RATE: str(comp[5]),  # rate
                KEY_RATE_DATA_SOURCE: comp[6] if comp[6] else ""  # rate_data_source
            }
            rows_data.append(row_dict)
        
        return {
            'work_type': struct_work[1],
            'component_type': struct_work[2],
            'comp_id': struct_work[0],
            'rows_data': rows_data
        }
    
    def retrieve_all_by_work_type(self, work_type: str) -> List[Dict]:
        """
        Retrieve all structure works of a specific type
        
        Args:
            work_type: Type of structure work (Foundation, Sub-Structure, etc.)
        
        Returns:
            List of dictionaries containing all structure works of the specified type
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT comp_id
            FROM struct_works_data
            WHERE type = ?
            ORDER BY comp_id
        ''', (work_type,))
        
        comp_ids = [row[0] for row in cursor.fetchall()]
        
        results = []
        for comp_id in comp_ids:
            data = self.retrieve_data_by_comp_id(comp_id)
            if data:
                results.append(data)
        
        return results
    
    def update_component(self, component_id: int, **kwargs):
        """
        Update specific fields of a component
        
        Args:
            component_id: ID of the component to update
            **kwargs: Fields to update (type_material, grade, quantity, unit, rate, rate_data_source)
        """
        cursor = self.conn.cursor()
        
        allowed_fields = ['type_material', 'grade', 'quantity', 'unit', 'rate', 'rate_data_source']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            return
        
        set_clause = ', '.join([f"{field} = ?" for field in update_fields.keys()])
        values = list(update_fields.values())
        values.append(component_id)
        
        query = f'''
            UPDATE component 
            SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        '''
        
        cursor.execute(query, values)
        self.conn.commit()
    
    def update_structure_work(self, comp_id: int, **kwargs):
        """
        Update specific fields of a structure work
        
        Args:
            comp_id: Component ID (PRIMARY KEY)
            **kwargs: Fields to update (type, component_type)
        """
        cursor = self.conn.cursor()
        
        allowed_fields = ['type', 'component_type']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            return
        
        set_clause = ', '.join([f"{field} = ?" for field in update_fields.keys()])
        values = list(update_fields.values())
        values.append(comp_id)
        
        query = f'''
            UPDATE struct_works_data 
            SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE comp_id = ?
        '''
        
        cursor.execute(query, values)
        self.conn.commit()
    
    def delete_structure_work(self, comp_id: int):
        """Delete a structure work and all its components (CASCADE)"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM struct_works_data WHERE comp_id = ?', (comp_id,))
        self.conn.commit()
    
    def delete_component(self, component_id: int):
        """Delete a specific component by its ID"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM component WHERE id = ?', (component_id,))
        self.conn.commit()
    
    def get_all_structure_works(self) -> List[Tuple]:
        """Get summary of all structure works"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT sw.comp_id, sw.type, sw.component_type, COUNT(c.id) as component_count
            FROM struct_works_data sw
            LEFT JOIN component c ON sw.comp_id = c.comp_id
            GROUP BY sw.comp_id
            ORDER BY sw.type, sw.comp_id
        ''')
        return cursor.fetchall()
    
    def get_components_by_comp_id(self, comp_id: int) -> List[Tuple]:
        """Get all component rows for a specific comp_id"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, comp_id, type_material, grade, quantity, unit, rate, rate_data_source
            FROM component
            WHERE comp_id = ?
            ORDER BY id
        ''', (comp_id,))
        return cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()