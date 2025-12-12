from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, Qt, QSize, Signal
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLineEdit, QComboBox, QGridLayout, QWidget, QLabel, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QFrame)
from PySide6.QtGui import QIcon
from ..utils.data import *
import sys

class ComponentWidget(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.widgets = []
        self.data = data
        self.material_rows = []
        self.current_material_row_idx = 1

        self.init_ui()

    def init_ui(self):
        self.component_first_scroll_content_layout = QVBoxLayout(self)
        self.component_first_scroll_content_layout.setContentsMargins(10, 10, 10, 10)
        self.component_first_scroll_content_layout.setSpacing(10)

        # --- Material Details Grid Layout ---
        self.material_grid_layout = QGridLayout()
        self.material_grid_layout.setHorizontalSpacing(10)
        self.material_grid_layout.setVerticalSpacing(10)  # Changed from 5 to 10

        # Header Row
        headers = ["Type of Material and Grade", "Quantity", "Unit", "Embodied Carbon Energy", "Carbon Emission Factor"]
        for col, header_text in enumerate(headers):
            label = QLabel(header_text)
            label.setAlignment(Qt.AlignCenter)
            label.setObjectName("MaterialGridLabel")
            self.material_grid_layout.addWidget(label, 0, col, alignment=Qt.AlignmentFlag.AlignCenter)

        self.component_first_scroll_content_layout.addLayout(self.material_grid_layout)
    
        # Add initial material rows
        for item in self.data:
            self.widgets.append(self.add_material_row(item))
            
        # --- Add Material Button ---
        self.add_material_button = QPushButton("+ Add Material")
        self.add_material_button.setObjectName("add_material_button")
        self.add_material_button.clicked.connect(self.add_material_row)
        
        # Add spacing before the button
        self.component_first_scroll_content_layout.addSpacing(10)
        self.component_first_scroll_content_layout.addWidget(self.add_material_button, alignment=Qt.AlignCenter)
        
    def add_material_row(self, item=[]):
        row_idx = self.current_material_row_idx
        row_widgets = []

        # Type of Material (Column 0)
        if item:
            type_material = QComboBox()
            type_material.addItem(item[0])
        else:
            type_material = QLineEdit()
            type_material.setPlaceholderText("Material...")
        type_material.setObjectName("MaterialGridInput")
        type_material.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        type_material.setMinimumWidth(200)
        self.material_grid_layout.addWidget(type_material, row_idx, 0)

        # Quantity (Column 1)
        quantity_edit = QLineEdit()
        if item:
            quantity_edit.setText(str(item[2]))
            quantity_edit.setReadOnly(True)
        quantity_edit.setObjectName("MaterialGridInput")
        quantity_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        quantity_edit.setMinimumWidth(100)
        quantity_edit.setMaximumWidth(100)
        self.material_grid_layout.addWidget(quantity_edit, row_idx, 1)

        # Unit (Column 2)
        if item:
            unit_combo = QComboBox()
            unit_combo.addItem(str(item[1]))
        else:
            unit_combo = QLineEdit()
            unit_combo.setPlaceholderText("Unit...")
        unit_combo.setObjectName("MaterialGridInput")
        unit_combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        unit_combo.setMinimumWidth(100)
        unit_combo.setMaximumWidth(100)
        self.material_grid_layout.addWidget(unit_combo, row_idx, 2)

        # Build row_widgets array
        if item:
            row_widgets = [item[1], item[2], item[3], item[4]]
        else:
            row_widgets = [unit_combo, quantity_edit, type_material, None]

        # --- Embodied Carbon Energy - Column 3 ---
        embodied_carbon_layout = QHBoxLayout()
        embodied_carbon_layout.setContentsMargins(0, 0, 0, 0)
        embodied_carbon_layout.setSpacing(5)

        embodied_carbon_edit = QLineEdit()
        embodied_carbon_edit.setPlaceholderText("0.00")
        embodied_carbon_edit.setObjectName("MaterialGridInput")
        embodied_carbon_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        embodied_carbon_edit.setMinimumWidth(100)
        embodied_carbon_edit.setMaximumWidth(100)
        embodied_carbon_layout.addWidget(embodied_carbon_edit)

        embodied_carbon_unit_label = QLabel("(MJ/kg)")
        embodied_carbon_unit_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        embodied_carbon_unit_label.setStyleSheet("color: #3F3E5E; font-size: 11px;")
        embodied_carbon_unit_label.setFixedWidth(60)
        embodied_carbon_layout.addWidget(embodied_carbon_unit_label)

        self.material_grid_layout.addLayout(embodied_carbon_layout, row_idx, 3)
        
        row_widgets.append(embodied_carbon_edit)

        # --- Carbon Emission Factor - Column 4 ---
        carbon_emission_layout = QHBoxLayout()
        carbon_emission_layout.setContentsMargins(0, 0, 0, 0)
        carbon_emission_layout.setSpacing(5)

        carbon_emission_edit = QLineEdit()
        carbon_emission_edit.setPlaceholderText("0.00")
        carbon_emission_edit.setObjectName("MaterialGridInput")
        carbon_emission_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        carbon_emission_edit.setMinimumWidth(100)
        carbon_emission_edit.setMaximumWidth(100)
        carbon_emission_layout.addWidget(carbon_emission_edit)

        if item:
            carbon_emission_unit_label = QLabel("kg CO2e/" + str(item[1]))
        else:
            carbon_emission_unit_label = QLabel("kg CO2e/kg")
        carbon_emission_unit_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        carbon_emission_unit_label.setStyleSheet("color: #3F3E5E; font-size: 11px;")
        carbon_emission_unit_label.setFixedWidth(80)
        carbon_emission_layout.addWidget(carbon_emission_unit_label)

        self.material_grid_layout.addLayout(carbon_emission_layout, row_idx, 4)
        
        row_widgets.append(carbon_emission_edit)

        # Connect unit changes to update carbon emission label
        if not item:
            def update_carbon_unit(text):
                unit_text = text.strip() if text.strip() else "kg"
                carbon_emission_unit_label.setText(f"kg CO2e/{unit_text}")
            
            unit_combo.textChanged.connect(update_carbon_unit)

        self.material_rows.append(row_widgets)
        self.current_material_row_idx += 1
        self.updateGeometry()
        self.adjustSize()

        if not item:
            self.widgets.append(row_widgets)

        return row_widgets

    def remove_material_row_by_widgets(self, row_widgets_to_remove):
        if row_widgets_to_remove not in self.material_rows:
            return

        row_idx_in_grid = -1
        for i, row_dict in enumerate(self.material_rows):
            if row_dict == row_widgets_to_remove:
                row_idx_in_grid = i + 1
                break

        if row_idx_in_grid == -1:
            return

        for col in range(self.material_grid_layout.columnCount()):
            item = self.material_grid_layout.itemAtPosition(row_idx_in_grid, col)
            if item:
                if item.widget():
                    widget = item.widget()
                    self.material_grid_layout.removeWidget(widget)
                    widget.deleteLater()
                elif item.layout():
                    layout = item.layout()
                    while layout.count():
                        sub_item = layout.takeAt(0)
                        if sub_item.widget():
                            sub_item.widget().deleteLater()
                    self.material_grid_layout.removeItem(layout)

        self.material_rows.remove(row_widgets_to_remove)
        self.current_material_row_idx -= 1

        # Re-arrange remaining rows
        for r_idx in range(row_idx_in_grid, self.current_material_row_idx + 1):
            for c_idx in range(self.material_grid_layout.columnCount()):
                item = self.material_grid_layout.itemAtPosition(r_idx + 1, c_idx)
                if item:
                    if item.widget():
                        widget = item.widget()
                        self.material_grid_layout.removeWidget(widget)
                        self.material_grid_layout.addWidget(widget, r_idx, c_idx)
                    elif item.layout():
                        layout = item.layout()
                        self.material_grid_layout.removeItem(layout)
                        self.material_grid_layout.addLayout(layout, r_idx, c_idx)

        self.updateGeometry()
        self.update()
        self.material_grid_layout.invalidate()
        self.adjustSize()

    def collect_data(self):
        p = []
        for row in self.widgets:
            data = {
                KEY_TYPE: row[2] if not isinstance(row[2], QLineEdit) else row[2].text(),
                KEY_GRADE: row[3] if not isinstance(row[3], QLineEdit) else row[3].text(),
                KEY_QUANTITY: float(row[1]) if not isinstance(row[1], QLineEdit) else (0.0 if not row[1].text() else float(row[1].text())),
                KEY_UNIT_M3: row[0] if not isinstance(row[0], QLineEdit) else ("kg" if not row[1].text() else row[1].text()),
                KEY_EMBODIED_CARBON_ENERGY: 0.0 if not row[4].text() else float(row[4].text()),
                KEY_CARBON_EMISSION_FACTOR: 0.0 if not row[4].text() else float(row[5].text()),
            }
            p.append(data)
        return p


class CarbonEmissionData(QWidget):
    closed = Signal()
    next = Signal(str)
    back = Signal(str)
    
    def __init__(self, database, parent=None):
        super().__init__()
        self.database_manager = database
        self.material_store = self.database_manager.get_unique_materials_and_grades()
        from pprint import pprint
        pprint(self.material_store)
        self.component_widgets = []

        self.setStyleSheet("""
            #central_panel_widget {
                background-color: #F8F8F8;
                border-radius: 8px;
            }
            #central_panel_widget QLabel {
                color: #333333;
                font-size: 12px;
            }
            #central_panel_widget QLabel#page_number_label {
                font-size: 14px;
                font-weight: bold;
                color: #555555;
            }

            QScrollArea {
                background-color: transparent;
                outline: none;
            }
            #scroll_content_widget {
                background-color: #FFF9F9;
                border: 1px solid #000000;
                padding-bottom: 20px;
            }

            QScrollBar:vertical {
                border: 1px solid #E0E0E0;
                background: #F0F0F0;
                width: 12px;
                margin: 18px 0px 18px 0px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #C0C0C0;
                border: 1px solid #A0A0A0;
                min-height: 20px;
                border-radius: 5px;
            }

            QScrollBar::add-line:vertical {
                border: 1px solid #E0E0E0;
                background: #E8E8E8;
                height: 18px;
                subcontrol-origin: bottom;
                subcontrol-position: bottom;
                border-bottom-left-radius: 6px;
                border-bottom-right-radius: 6px;
            }

            QScrollBar::sub-line:vertical {
                border: 1px solid #E0E0E0;
                background: #E8E8E8;
                height: 18px;
                subcontrol-origin: top;
                subcontrol-position: top;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                width: 10px;
                height: 10px;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar::up-arrow:vertical {
                image: url(resources/arrow_up.png);
            }
            QScrollBar::down-arrow:vertical {
                image: url(resources/arrow_down.png);
            }

            QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {
                background: #D0D0D0;
            }

            QPushButton#top_button_left_panel {
                background-color: #FDEFEF;
                border-top: 1px solid #000000;
                border-left: 1px solid #000000;
                border-right: 1px solid #000000;
                text-align: left;
                padding: 4px 10px;
                color: #000000;
            }
            QPushButton#top_button_left_panel:hover {
                background-color: #F0E6E6;
                border-color: #808080;
            }
            QPushButton#top_button_left_panel:pressed {
                background-color: #FFF3F3;
                border-color: #606060;
            }

            #component_first_widget {
                background-color: transparent;
                margin-top: 10px;
            }

            #component_first_scroll_content_widget {
                background-color: #FFFFFF;
                padding: 10px;
                border-radius: 8px;
            }

            QPushButton#nav_button {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                color: #3F3E5E;
                padding: 6px 15px;
                text-align: center;
                min-width: 80px;
            }
            QPushButton#nav_button:hover {
                background-color: #F8F8F8;
                border-color: #C0C0C0;
            }
            QPushButton#nav_button:pressed {
                background-color: #E8E8E8;
                border-color: #A0A0A0;
            }

            QComboBox {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 5px;
            }
            QComboBox::down-arrow {
                image: url(resources/country_arrow.png);
                width: 30px;
                height: 30px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #DDDCE0;
                border-radius: 5px;
                background-color: #FFFFFF;
                outline: none;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #FDEFEF;
                color: #000000;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #FDEFEF;
            }

            #MaterialGridLabel {
                font-weight: bold;
                color: #3F3E5E;
                padding: 5px;
                text-align: center;
            }
            #MaterialGridInput {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
                background-color: #FFFFFF;
            }
            #MaterialGridInput:focus {
                border: 1px solid #DDDCE0;
                background-color: #FFFFFF;
            }

            QPushButton#add_material_button, QPushButton#add_component_button {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                color: #3F3E5E;
                padding: 6px 15px;
                text-align: center;
            }
            QPushButton#add_material_button:hover, QPushButton#add_component_button:hover {
                background-color: #F8F8F8;
                border-color: #C0C0C0;
            }
            QPushButton#add_material_button:pressed, QPushButton#add_component_button:pressed {
                background-color: #E8E8E8;
                border-color: #A0A0A0;
            }
        """)

        self.setObjectName("central_panel_widget")
        left_panel_vlayout = QVBoxLayout(self)
        left_panel_vlayout.setContentsMargins(0, 0, 0, 0)
        left_panel_vlayout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        scroll_content_widget = QWidget()
        scroll_content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        scroll_content_widget.setObjectName("scroll_content_widget")
        self.scroll_area.setWidget(scroll_content_widget)

        self.scroll_content_layout = QVBoxLayout(scroll_content_widget)
        self.scroll_content_layout.setContentsMargins(15, 15, 15, 15)  # Added margins
        self.scroll_content_layout.setSpacing(15)  # Increased spacing

        # Create the navigation buttons layout
        self.button_h_layout = QHBoxLayout()
        self.button_h_layout.setSpacing(10)
        self.button_h_layout.setContentsMargins(0, 10, 0, 0)  # Top margin only

        self.button_h_layout.addStretch()

        back_button = QPushButton("Back")
        back_button.setObjectName("nav_button")
        back_button.clicked.connect(lambda: self.back.emit(KEY_CARBON_EMISSION))
        self.button_h_layout.addWidget(back_button)

        next_button = QPushButton("Next")
        next_button.setObjectName("nav_button")
        next_button.clicked.connect(self.collect_data)
        next_button.clicked.connect(lambda: self.next.emit(KEY_CARBON_EMISSION))
        self.button_h_layout.addWidget(next_button)

        # Add the initial component layout
        self.add_component_layout()

        # Add navigation buttons
        self.scroll_content_layout.addLayout(self.button_h_layout)

        # Add vertical spacer at the end
        self.scroll_content_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        left_panel_vlayout.addWidget(self.scroll_area)

    def add_component_layout(self):
        new_component = ComponentWidget(data=self.material_store, parent=self)
        self.component_widgets.append(new_component)

        # Remove spacer and button layout temporarily
        vertical_spacer_item = None
        for i in range(self.scroll_content_layout.count()):
            item = self.scroll_content_layout.itemAt(i)
            if isinstance(item, QSpacerItem) and item.sizeHint().width() == 0:
                vertical_spacer_item = self.scroll_content_layout.takeAt(i)
                break

        if self.scroll_content_layout.indexOf(self.button_h_layout) != -1:
            self.scroll_content_layout.removeItem(self.button_h_layout)

        # Insert the new component
        self.scroll_content_layout.addWidget(new_component)

        # Re-add the navigation buttons layout
        self.scroll_content_layout.addLayout(self.button_h_layout)
        
        # Re-add the vertical spacer
        if vertical_spacer_item:
            self.scroll_content_layout.addItem(vertical_spacer_item)

        self.scroll_area.widget().updateGeometry()
        self.scroll_area.widget().adjustSize()

    def remove_component_layout(self, component_to_remove):
        if component_to_remove in self.component_widgets:
            self.scroll_content_layout.removeWidget(component_to_remove)
            self.component_widgets.remove(component_to_remove)
            component_to_remove.deleteLater()
            self.scroll_area.widget().updateGeometry()
            self.scroll_area.widget().adjustSize()

    def expand_scroll_area(self):
        self.central_widget.layout().invalidate()   

    def close_widget(self):
        self.closed.emit()
        self.setParent(None)

    def collect_data(self):
        from pprint import pprint
        data = self.component_widgets[0].collect_data()
        print("\nCollected Data from Carbon Emission UI:")
        pprint(data)
        # Insert Carbon Emission Data
        self.database_manager.insert_carbon_emission_data(data)