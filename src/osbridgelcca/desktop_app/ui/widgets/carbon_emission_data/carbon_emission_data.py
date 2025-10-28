from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, Qt, QSize, Signal
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLineEdit, QComboBox, QGridLayout, QWidget, QLabel, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QFrame)
from PySide6.QtGui import QIcon
import sys

class ComponentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.material_rows = [] # To store references to widgets in each material row
        self.current_material_row_idx = 1 # Start index for material rows (0 is header)    

        self.init_ui()

    def init_ui(self):
        self.component_first_scroll_content_layout = QVBoxLayout(self) # Set QVBoxLayout directly on self
        self.component_first_scroll_content_layout.setContentsMargins(10, 10, 10, 10)
        self.component_first_scroll_content_layout.setSpacing(10)

        # --- Material Details Grid Layout ---
        self.material_grid_layout = QGridLayout()
        self.material_grid_layout.setHorizontalSpacing(10)
        self.material_grid_layout.setVerticalSpacing(5)

        # Header Row - Updated headers for clarity (no specific unit in header now)
        headers = ["Type of Material and Grade", "Quantity", "Unit", "Embodied Carbon Energy", "Carbon Emission Factor"]
        for col, header_text in enumerate(headers):
            label = QLabel(header_text)
            label.setAlignment(Qt.AlignCenter)
            label.setObjectName("MaterialGridLabel")
            if header_text=="Embodied Carbon Energy":
               self.material_grid_layout.addWidget(label, 0, col, alignment=Qt.AlignmentFlag.AlignRight)
            else: 

               self.material_grid_layout.addWidget(label, 0, col, alignment=Qt.AlignmentFlag.AlignCenter)   

        self.component_first_scroll_content_layout.addLayout(self.material_grid_layout)
    
        # Add initial two material rows
        self.add_material_row()
        self.add_material_row()

        # --- Add Material Button ---
        self.add_material_button = QPushButton("+ Add Material")
        self.add_material_button.setObjectName("add_material_button")
        self.add_material_button.clicked.connect(self.add_material_row)
        self.component_first_scroll_content_layout.addWidget(self.add_material_button, alignment=Qt.AlignCenter)
        

    def add_material_row(self):
        row_widgets = {}
        row_idx = self.current_material_row_idx

        # Set fixed width for input widgets.
        fixed_input_width_combo = 80 # Width for individual combo boxes
        fixed_input_width_line_edit = 80 # Width for individual line edits

        type_material_combo = QComboBox()
        type_material_combo.addItems(["Sand", "Gravel", "Cement", "Water", "Admixture", "Rebar", "Other"])
        type_material_combo.setObjectName("MaterialGridInput")
        type_material_combo.setFixedWidth(fixed_input_width_combo)
        self.material_grid_layout.addWidget(type_material_combo, row_idx, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        row_widgets['type'] = type_material_combo

        quantity_edit = QLineEdit()
        quantity_edit.setPlaceholderText("0")
        quantity_edit.setObjectName("MaterialGridInput")
        quantity_edit.setFixedWidth(fixed_input_width_line_edit)
        self.material_grid_layout.addWidget(quantity_edit, row_idx, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        row_widgets['quantity'] = quantity_edit

        unit_combo_m3 = QComboBox()
        unit_combo_m3.addItems(["m³", "ft³", "kg", "ton", "litre"])
        unit_combo_m3.setObjectName("MaterialGridInput")
        unit_combo_m3.setFixedWidth(fixed_input_width_combo)
        self.material_grid_layout.addWidget(unit_combo_m3, row_idx, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        row_widgets['unit_m3'] = unit_combo_m3


        # --- Embodied Carbon Energy (LineEdit + QLabel for unit text) - Column 3 ---
        embodied_carbon_layout = QHBoxLayout()
        embodied_carbon_layout.addStretch()
        embodied_carbon_layout.setContentsMargins(0, 0, 0, 0)
        embodied_carbon_layout.setSpacing(5) # Small spacing between line edit and label

        embodied_carbon_edit = QLineEdit()
        embodied_carbon_edit.setPlaceholderText("0.00")
        embodied_carbon_edit.setObjectName("MaterialGridInput")
        embodied_carbon_edit.setFixedWidth(fixed_input_width_combo) # Changed to fixed_input_width_combo
        embodied_carbon_layout.addWidget(embodied_carbon_edit)

        # Replaced QComboBox with QLabel for static text
        embodied_carbon_unit_label = QLabel("(MJ/kg)")
        embodied_carbon_unit_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        embodied_carbon_unit_label.setStyleSheet("color: #3F3E5E; font-size: 11px;") # Style to match other text
        embodied_carbon_layout.addWidget(embodied_carbon_unit_label)


        self.material_grid_layout.addLayout(embodied_carbon_layout, row_idx, 3, alignment=Qt.AlignmentFlag.AlignHCenter)
        row_widgets['embodied_carbon_edit'] = embodied_carbon_edit
        row_widgets['embodied_carbon_unit_label'] = embodied_carbon_unit_label


        # --- Carbon Emission Factor (LineEdit + QLabel for unit text) - Column 4 ---
        carbon_emission_layout = QHBoxLayout()
        carbon_emission_layout.setContentsMargins(0, 0, 0, 0)
        carbon_emission_layout.setSpacing(5) # Small spacing between line edit and label

        carbon_emission_layout.addStretch()

        carbon_emission_edit = QLineEdit()
        carbon_emission_edit.setPlaceholderText("0.00")
        carbon_emission_edit.setObjectName("MaterialGridInput")
        carbon_emission_edit.setFixedWidth(fixed_input_width_combo) # Changed to fixed_input_width_combo
        carbon_emission_layout.addWidget(carbon_emission_edit)

        # Replaced QComboBox with QLabel for static text
        carbon_emission_unit_label = QLabel("kg CO2e/kg")
        carbon_emission_unit_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        carbon_emission_unit_label.setStyleSheet("color: #3F3E5E; font-size: 11px;") # Style to match other text
        carbon_emission_layout.addWidget(carbon_emission_unit_label)

        carbon_emission_layout.addStretch()

        self.material_grid_layout.addLayout(carbon_emission_layout, row_idx, 4)
        row_widgets['carbon_emission_edit'] = carbon_emission_edit
        row_widgets['carbon_emission_unit_label'] = carbon_emission_unit_label


        self.material_rows.append(row_widgets)
        self.current_material_row_idx += 1
        self.updateGeometry()
        self.adjustSize()


    def remove_material_row_by_widgets(self, row_widgets_to_remove):
        if row_widgets_to_remove not in self.material_rows:
            return

        row_idx_in_grid = -1
        for i, row_dict in enumerate(self.material_rows):
            if row_dict == row_widgets_to_remove:
                row_idx_in_grid = i + 1  # +1 because row 0 is header
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
                    # Iterate and delete widgets within the layout
                    while layout.count():
                        sub_item = layout.takeAt(0)
                        if sub_item.widget():
                            sub_item.widget().deleteLater()
                    self.material_grid_layout.removeItem(layout) # Remove the layout itself

        self.material_rows.remove(row_widgets_to_remove)
        self.current_material_row_idx -= 1

        # Re-arrange remaining rows
        for r_idx in range(row_idx_in_grid, self.current_material_row_idx + 1):
            for c_idx in range(self.material_grid_layout.columnCount()):
                item = self.material_grid_layout.itemAtPosition(r_idx + 1, c_idx) # Look at the row below
                if item:
                    if item.widget():
                        widget = item.widget()
                        self.material_grid_layout.removeWidget(widget)
                        self.material_grid_layout.addWidget(widget, r_idx, c_idx, alignment=Qt.AlignmentFlag.AlignHCenter) # Re-add with original alignment
                    elif item.layout():
                        layout = item.layout()
                        self.material_grid_layout.removeItem(layout)
                        self.material_grid_layout.addLayout(layout, r_idx, c_idx, alignment=Qt.AlignmentFlag.AlignHCenter) # Re-add with original alignment

        self.updateGeometry()
        self.update()
        self.material_grid_layout.invalidate()
        self.adjustSize()

class CarbonEmissionData(QWidget):
    closed = Signal()
    def __init__(self):
        super().__init__()

        self.component_widgets = [] # To store references to each ComponentWidget instance

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

            /* Styling for component_first_widget (the container for the nested scroll area) */
            #component_first_widget {
                background-color: transparent;
                margin-top: 10px; /* Add some space above each component block */
            }

            #component_first_scroll_content_widget { /* This now applies directly to ComponentWidget itself */
                background-color: #FFFFFF;
                padding: 10px;

                border-radius: 8px;
            }

            /* Updated Styling for navigation buttons to match the Add Material/Component buttons */
            QPushButton#nav_button {
                background-color: #FFFFFF; /* White background */
                border: 1px solid #E0E0E0; /* Light grey border */
                border-radius: 8px; /* Slightly more rounded corners */
                color: #3F3E5E; /* Dark text color */
                padding: 6px 15px; /* Increased padding */
                text-align: center;
                min-width: 80px; /* Ensure a minimum width */
            }
            QPushButton#nav_button:hover {
                background-color: #F8F8F8; /* Very subtle light grey on hover */
                border-color: #C0C0C0; /* Darker border on hover */
            }
            QPushButton#nav_button:pressed {
                background-color: #E8E8E8; /* Darker grey on pressed */
                border-color: #A0A0A0; /* Even darker border */
            }
            /* Styling for QComboBox */
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

            /* Styling for material grid elements */
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
            /* IMPROVED CSS FOR ADD MATERIAL/COMPONENT BUTTONS */
            QPushButton#add_material_button, QPushButton#add_component_button {
                background-color: #FFFFFF; /* White background */
                border: 1px solid #E0E0E0; /* Light grey border */
                border-radius: 8px; /* Slightly more rounded corners */
                color: #3F3E5E; /* Dark text color */
                padding: 6px 15px; /* Increased padding */
                text-align: center;
            }
            QPushButton#add_material_button:hover, QPushButton#add_component_button:hover {
                background-color: #F8F8F8; /* Very subtle light grey on hover */
                border-color: #C0C0C0; /* Darker border on hover */
            }
            QPushButton#add_material_button:pressed, QPushButton#add_component_button:pressed {
                background-color: #E8E8E8; /* Darker grey on pressed */
                border-color: #A0A0A0; /* Even darker border */
            }
            /* END IMPROVED CSS */
        """)

        self.setObjectName("central_panel_widget")
        left_panel_vlayout = QVBoxLayout(self)
        left_panel_vlayout.setContentsMargins(0, 0, 0, 0)
        left_panel_vlayout.setSpacing(0)

        top_h_layout_left_panel = QHBoxLayout()
        top_button_left_panel = QPushButton("Carbon Emission Data")
        top_h_layout_left_panel.addWidget(top_button_left_panel)
        top_button_left_panel.setIcon(QIcon("resources/close.png"))
        top_button_left_panel.setIconSize(QSize(13, 13))
        top_button_left_panel.setObjectName("top_button_left_panel")
        top_button_left_panel.clicked.connect(self.close_widget)
        top_button_left_panel.setLayoutDirection(Qt.RightToLeft)
        top_h_layout_left_panel.addWidget(top_button_left_panel)

        top_h_layout_left_panel.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Preferred))
        left_panel_vlayout.addLayout(top_h_layout_left_panel)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        scroll_content_widget = QWidget()
        scroll_content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        scroll_content_widget.setObjectName("scroll_content_widget")
        self.scroll_area.setWidget(scroll_content_widget)

        self.scroll_content_layout = QVBoxLayout(scroll_content_widget)
        self.scroll_content_layout.setContentsMargins(0,0,0,0)
        self.scroll_content_layout.setSpacing(0)

        # Create the navigation buttons layout
        self.button_h_layout = QHBoxLayout()
        self.button_h_layout.setSpacing(10)
        self.button_h_layout.setContentsMargins(10,10,10,10)

        # Adjust these stretch factors to control the position
        self.button_h_layout.addStretch(6) # Larger stretch on the left to push it more right

        back_button = QPushButton("Back")
        back_button.setObjectName("nav_button")
        self.button_h_layout.addWidget(back_button)

        next_button = QPushButton("Next")
        next_button.setObjectName("nav_button")
        self.button_h_layout.addWidget(next_button)


        # Add the initial component layout
        self.add_component_layout()

        # Add initial spacing before the navigation buttons
        self.scroll_content_layout.addLayout(self.button_h_layout)

        # --- Add a corner spacer to the scroll_content_layout ---
        self.button_h_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.scroll_content_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        left_panel_vlayout.addWidget(self.scroll_area)


    def add_component_layout(self):
        new_component = ComponentWidget(self)
        self.component_widgets.append(new_component)

        # Temporarily remove button_h_layout and the vertical spacer for insertion
        # Find the vertical spacer and remove it if it exists
        vertical_spacer_item = None
        for i in range(self.scroll_content_layout.count()):
            item = self.scroll_content_layout.itemAt(i)
            if isinstance(item, QSpacerItem) and item.sizeHint().width() == 0: # This identifies the vertical spacer
                vertical_spacer_item = self.scroll_content_layout.takeAt(i)
                break

        if self.scroll_content_layout.indexOf(self.button_h_layout) != -1:
            self.scroll_content_layout.removeItem(self.button_h_layout)

        # Insert the new component
        self.scroll_content_layout.addWidget(new_component)

        # Re-add the navigation buttons layout
        self.scroll_content_layout.addLayout(self.button_h_layout)
        
        # Re-add the vertical spacer if it was found
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

#----------------Standalone-Test-Code--------------------------------

# class MyMainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setStyleSheet("border: none")

#         self.central_widget = QWidget()
#         self.central_widget.setObjectName("central_widget")
#         self.setCentralWidget(self.central_widget)

#         self.main_h_layout = QHBoxLayout(self.central_widget)
#         self.main_h_layout.addStretch(1)

#         self.main_h_layout.addWidget(CarbonEmissionData(), 2)

#         self.setWindowState(Qt.WindowMaximized)


# if __name__ == "__main__":
#     QCoreApplication.setAttribute(Qt.AA_DontShowIconsInMenus, False)
#     app = QApplication(sys.argv)
#     window = MyMainWindow()
#     window.show()
#     sys.exit(app.exec())