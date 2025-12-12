from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, Qt, QSize, Signal
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLineEdit, QGridLayout, QWidget, QLabel, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QComboBox)
from PySide6.QtGui import QIcon, QDoubleValidator
from ..utils.data import *
import sys

class CarbonEmissionCostData(QWidget):
    closed = Signal()
    next = Signal(str)
    back = Signal(str)
    def __init__(self, database, parent=None):
        super().__init__()
        self.parent = parent
        self.widget = []
        self.database_manager = database
        
        # Store references to K.Ricke widgets for showing/hiding
        self.k_ricke_widgets = []

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
                background-color: #FFFFFF;
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
            QComboBox:disabled {
                background-color: #F0F0F0;
                color: #888888;
            }
            
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
                background-color: #FFFFFF;
            }
            QLineEdit:focus {
                border: 1px solid #DDDCE0;
                background-color: #FFFFFF;
            }
            QLineEdit:disabled {
                background-color: #F0F0F0;
                color: #888888;
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
        self.scroll_content_layout.setContentsMargins(0,0,0,0)
        self.scroll_content_layout.setSpacing(0)

        # --- Add General Info Form at the top of the scroll area ---
        self.general_widget = QWidget()
        self.general_layout = QVBoxLayout(self.general_widget)
        self.general_layout.setContentsMargins(10, 20, 10, 10)
        self.general_layout.setSpacing(10)

        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(10)
        self.grid_layout.setVerticalSpacing(20)

        field_width = 200

        # Validator for numeric inputs
        validator = QDoubleValidator()
        validator.setRange(0.0, 9999999.999, 4)
        validator.setBottom(0.0)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)

        # 1. Source
        label = QLabel("Source")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.grid_layout.addWidget(label, 0, 0, 1, 1)
        
        self.source_combo = QComboBox(self.general_widget)
        self.widget.append(self.source_combo)
        self.source_combo.setFixedWidth(field_width)
        self.source_combo.addItems(KEY_SCC_OPTIONS)
        self.source_combo.currentTextChanged.connect(self.on_source_changed)
        self.grid_layout.addWidget(self.source_combo, 0, 1, 1, 1, alignment=Qt.AlignLeft)

        # 2. Social Cost of Carbon (SCC)
        scc_label = QLabel("Social Cost of Carbon")
        scc_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.grid_layout.addWidget(scc_label, 1, 0, 1, 1)
        
        # Create a QWidget with a horizontal layout for the SCC input and label
        scc_widget = QWidget(self.general_widget)
        scc_h_layout = QHBoxLayout(scc_widget)
        scc_h_layout.setContentsMargins(0,0,0,0)
        scc_h_layout.setSpacing(10)
        
        self.scc_input = QLineEdit()
        self.widget.append(self.scc_input)
        self.scc_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.scc_input.setFixedWidth(field_width)
        self.scc_input.setText("6.3936")
        self.scc_input.setValidator(validator)
        scc_h_layout.addWidget(self.scc_input)
        
        scc_unit_label = QLabel("(INR/kgCO₂e)")
        scc_unit_label.setStyleSheet("color: #707070; font-size: 11px;")
        scc_h_layout.addWidget(scc_unit_label)
        
        self.scc_suggested_label = QLabel("Suggested")
        self.scc_suggested_label.setStyleSheet("color: #B3AEAE; font-size: 10px;")
        scc_h_layout.addWidget(self.scc_suggested_label)
        scc_h_layout.addStretch(1)
        
        self.grid_layout.addWidget(scc_widget, 1, 1, 1, 1, alignment=Qt.AlignLeft)

        # 3. K.Ricke et al. specific fields (initially hidden)
        current_row = 2
        
        # SSP
        ssp_label = QLabel(SCC_SSP)
        ssp_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.grid_layout.addWidget(ssp_label, current_row, 0, 1, 1)
        self.k_ricke_widgets.append(ssp_label)
        
        self.ssp_combo = QComboBox(self.general_widget)
        self.widget.append(self.ssp_combo)
        self.ssp_combo.setFixedWidth(field_width)
        self.ssp_combo.addItems(SCC_SSP_OPTIONS)
        self.grid_layout.addWidget(self.ssp_combo, current_row, 1, 1, 1, alignment=Qt.AlignLeft)
        self.k_ricke_widgets.append(self.ssp_combo)
        current_row += 1
        
        # RCP
        rcp_label = QLabel(SCC_RCP)
        rcp_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.grid_layout.addWidget(rcp_label, current_row, 0, 1, 1)
        self.k_ricke_widgets.append(rcp_label)
        
        self.rcp_combo = QComboBox(self.general_widget)
        self.widget.append(self.rcp_combo)
        self.rcp_combo.setFixedWidth(field_width)
        self.rcp_combo.addItems(SCC_RCP_OPTIONS)
        self.grid_layout.addWidget(self.rcp_combo, current_row, 1, 1, 1, alignment=Qt.AlignLeft)
        self.k_ricke_widgets.append(self.rcp_combo)
        current_row += 1
        
        # Climate
        climate_label = QLabel(SCC_CLIMATE)
        climate_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.grid_layout.addWidget(climate_label, current_row, 0, 1, 1)
        self.k_ricke_widgets.append(climate_label)
        
        self.climate_combo = QComboBox(self.general_widget)
        self.widget.append(self.climate_combo)
        self.climate_combo.setFixedWidth(field_width)
        self.climate_combo.addItems(SSC_CLIMATE_OPTIONS)
        self.grid_layout.addWidget(self.climate_combo, current_row, 1, 1, 1, alignment=Qt.AlignLeft)
        self.k_ricke_widgets.append(self.climate_combo)
        current_row += 1
        
        # Run
        run_label = QLabel(SCC_RUN)
        run_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.grid_layout.addWidget(run_label, current_row, 0, 1, 1)
        self.k_ricke_widgets.append(run_label)
        
        self.run_combo = QComboBox(self.general_widget)
        self.widget.append(self.run_combo)
        self.run_combo.setFixedWidth(field_width)
        self.run_combo.addItems(SCC_RUN_OPTIONS)
        self.grid_layout.addWidget(self.run_combo, current_row, 1, 1, 1, alignment=Qt.AlignLeft)
        self.k_ricke_widgets.append(self.run_combo)
        current_row += 1
        
        # USD to INR Conversion
        usd_inr_label = QLabel("USD to INR Conversion")
        usd_inr_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.grid_layout.addWidget(usd_inr_label, current_row, 0, 1, 1)
        self.k_ricke_widgets.append(usd_inr_label)
        
        self.usd_inr_input = QLineEdit()
        self.widget.append(self.usd_inr_input)
        self.usd_inr_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.usd_inr_input.setFixedWidth(field_width)
        self.usd_inr_input.setPlaceholderText("Enter conversion rate")
        self.usd_inr_input.setValidator(validator)
        self.usd_inr_input.setText("88")
        self.grid_layout.addWidget(self.usd_inr_input, current_row, 1, 1, 1, alignment=Qt.AlignLeft)
        self.k_ricke_widgets.append(self.usd_inr_input)

        self.general_layout.addLayout(self.grid_layout)
        self.general_layout.addStretch(1)
        self.scroll_content_layout.addWidget(self.general_widget, alignment=Qt.AlignLeft)

        # Create the navigation buttons layout
        self.button_h_layout = QHBoxLayout()
        self.button_h_layout.setSpacing(10)
        self.button_h_layout.setContentsMargins(10,10,10,10)

        self.button_h_layout.addStretch(6)

        back_button = QPushButton("Back")
        back_button.setObjectName("nav_button")
        back_button.clicked.connect(lambda: self.back.emit(KEY_CARBON_EMISSION_COST))
        self.button_h_layout.addWidget(back_button)

        next_button = QPushButton("Next")
        next_button.setObjectName("nav_button")
        next_button.clicked.connect(self.collect_data)
        next_button.clicked.connect(lambda: self.next.emit(KEY_CARBON_EMISSION_COST))
        self.button_h_layout.addWidget(next_button)

        self.scroll_content_layout.addLayout(self.button_h_layout)

        self.button_h_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.scroll_content_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        left_panel_vlayout.addWidget(self.scroll_area)
        
        # Initialize the UI state based on default source
        self.on_source_changed(self.source_combo.currentText())
    
    def on_source_changed(self, source):
        """Handle source selection changes"""
        if source == SCC_NITI_Aayog:
            # Set default value and disable input
            self.scc_input.setText("6.3936")
            self.scc_input.setEnabled(False)
            self.scc_suggested_label.show()
            # Hide K.Ricke fields
            for widget in self.k_ricke_widgets:
                widget.hide()
                
        elif source == SCC_CUSTOM:
            # Clear value and enable input
            self.scc_input.clear()
            self.scc_input.setEnabled(True)
            self.scc_suggested_label.hide()
            # Hide K.Ricke fields
            for widget in self.k_ricke_widgets:
                widget.hide()
                
        elif source == SCC_K_Ricke_et_al:
            # Disable SCC input (will be calculated)
            self.scc_input.setEnabled(False)
            self.scc_suggested_label.hide()
            # Show K.Ricke fields
            for widget in self.k_ricke_widgets:
                widget.show()
    
    def collect_data(self):
        from pprint import pprint
        data = {
            KEY_SOURCE: self.source_combo.currentText(),
            KEY_SCC: float(self.scc_input.text()),
            KEY_USD_T_INR: float(self.usd_inr_input.text()) if self.usd_inr_input.text() else 0.0
        }
        print("\nCollected Data from Carbon Emission Cost UI:")
        pprint(data)

        # Save UI Data to Backend
        self.database_manager.carbon_emission_cost_data = data

        # Carbon Emission Cost
        # self.database_manager.carbon_emission_cost()

    def close_widget(self):
        self.closed.emit()
        self.setParent(None)