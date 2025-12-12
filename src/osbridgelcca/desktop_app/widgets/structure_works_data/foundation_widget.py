from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, Qt, QSize, Signal
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLineEdit, QComboBox, QGridLayout, QWidget, QLabel, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QFrame, QMessageBox)
from PySide6.QtGui import QIcon
from PySide6.QtGui import QDoubleValidator
from ..utils.data import *
import sys

class ComponentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self._initializing = True
        self.data = construction_materials.get(KEY_FOUNDATION)
        self.material_rows = []
        self.current_material_row_idx = 1

        self.init_ui()
        self._initializing = False

    def init_ui(self):
        self.component_first_scroll_content_layout = QVBoxLayout(self)
        self.component_first_scroll_content_layout.setContentsMargins(10, 10, 10, 10)
        self.component_first_scroll_content_layout.setSpacing(10)

        component_header_layout = QHBoxLayout()
        component_label = QLabel("Component:")
        component_label.setContentsMargins(0, 5, 0, 5)
        component_header_layout.addWidget(component_label)

        self.component_combobox = QComboBox()
        self.component_combobox.currentTextChanged.connect(self.update_comp_material)
        self.component_combobox.addItems(self.data.keys())
        self.component_combobox.currentTextChanged.connect(self._on_value_changed)
        self.component_combobox.setContentsMargins(0, 5, 0, 5)
        component_header_layout.addWidget(self.component_combobox)

        self.remove_component_button = QPushButton("x")
        self.remove_component_button.setFixedSize(24, 24)
        self.remove_component_button.setStyleSheet("""
            QPushButton {
                background-color: #FFCCCC;
                border: 1px solid #FF9999;
                border-radius: 12px;
                font-weight: bold;
                line-height:12px;
                color: #CC0000;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #FF9999;
                color: white;
            }
            QPushButton:pressed {
                background-color: #FF6666;
            }
        """)
        component_header_layout.addWidget(self.remove_component_button)
        component_header_layout.addStretch(1)

        self.component_first_scroll_content_layout.addLayout(component_header_layout)

        self.material_grid_layout = QGridLayout()
        self.material_grid_layout.setHorizontalSpacing(10)
        self.material_grid_layout.setVerticalSpacing(5)

        headers = ["Type of Material", "Grade", "Quantity", "Unit", "Rate", "Rate Data Source"]
        for col, header_text in enumerate(headers):
            label = QLabel(header_text)
            label.setAlignment(Qt.AlignCenter)
            label.setObjectName("MaterialGridLabel")
            self.material_grid_layout.addWidget(label, 0, col)

        self.component_first_scroll_content_layout.addLayout(self.material_grid_layout)

        self.add_material_row()
        self.add_material_row()

        self.update_comp_material(self.component_combobox.currentText())

        self.add_material_button = QPushButton("+ Add Material")
        self.add_material_button.setObjectName("add_material_button")
        self.add_material_button.clicked.connect(self.add_material_row)
        self.component_first_scroll_content_layout.addWidget(self.add_material_button, alignment=Qt.AlignCenter)
        
    def set_locked(self, locked):
        self.component_combobox.setEnabled(not locked)
        self.add_material_button.setEnabled(not locked)
        self.remove_component_button.setEnabled(not locked)
        
        for row in self.material_rows:
            row[KEY_TYPE].setEnabled(not locked)
            row[KEY_GRADE].setEnabled(not locked)
            row[KEY_QUANTITY].setEnabled(not locked)
            row[KEY_UNIT_M3].setEnabled(not locked)
            row[KEY_RATE].setEnabled(not locked)
            row[KEY_RATE_DATA_SOURCE].setEnabled(not locked)
            row['remove_button'].setEnabled(not locked)
    
    def collect_data(self):
        rows_data = []
        for row in self.material_rows:
            component = self.component_combobox.currentText()
            material_type = row[KEY_TYPE].currentText()
            material_grade = row[KEY_GRADE].currentText()
            quantity = row[KEY_QUANTITY].text()
            unit_m3 = row[KEY_UNIT_M3].currentText()
            rate = row[KEY_RATE].text()
            rate_data_source = row[KEY_RATE_DATA_SOURCE].text()
            row_dict = { KEY_COMPONENT: component,
                         KEY_TYPE: material_type,
                         KEY_GRADE: material_grade,
                         KEY_QUANTITY: quantity if quantity.strip() else "0",
                         KEY_UNIT_M3: unit_m3,
                         KEY_RATE: rate if rate.strip() else "0.00",
                         KEY_RATE_DATA_SOURCE: rate_data_source
                        }
            rows_data.append(row_dict)
        return rows_data

    def _on_value_changed(self, *_args):
        if getattr(self, "_initializing", False):
            return
        if self.parent_widget and hasattr(self.parent_widget, "mark_state_changed"):
            self.parent_widget.mark_state_changed()

    def _on_type_material_changed(self, text, grade_widget, unit_widget):
        self.update_comp_grades(text, grade_widget)
        self.update_comp_units(text, unit_widget)
        self._on_value_changed()

    def update_comp_material(self, selected_component):
        materials = self.data.get(selected_component).keys()
        for i in range(len(self.material_rows)):
            material_combo = self.material_rows[i][KEY_TYPE]
            grade_combo = self.material_rows[i][KEY_GRADE]
            unit_combo = self.material_rows[i][KEY_UNIT_M3]
            material_combo.clear()
            material_combo.addItems(materials)
            current_text = material_combo.currentText()
            if current_text:
                self.update_comp_grades(current_text, grade_combo)
                self.update_comp_units(current_text, unit_combo)
        self._on_value_changed()
    
    def update_comp_grades(self, selected_material, widget):
        selected_component = self.component_combobox.currentText()
        grades = self.data.get(selected_component,{}).get(selected_material,{}).get(KEY_GRADE,[])
        widget.clear()
        widget.addItems(grades)
    
    def update_comp_units(self, selected_material, widget):
        selected_component = self.component_combobox.currentText()
        units = self.data.get(selected_component,{}).get(selected_material,{}).get(KEY_UNITS,[])
        widget.clear()
        widget.addItems(units)

    def add_material_row(self):
        validator = QDoubleValidator()
        validator.setRange(0.0, 9999999.999, 3)
        validator.setBottom(0.0)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
    
        row_widgets = {}
        row_idx = self.current_material_row_idx
        fixed_input_width = 80

        type_material_combo = QComboBox()
        type_material_combo.setObjectName("MaterialGridInput")
        type_material_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(type_material_combo, row_idx, 0)
        row_widgets[KEY_TYPE] = type_material_combo

        grade_combo = QComboBox()
        grade_combo.setObjectName("MaterialGridInput")
        grade_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(grade_combo, row_idx, 1)
        row_widgets[KEY_GRADE] = grade_combo
        grade_combo.currentTextChanged.connect(self._on_value_changed)

        quantity_edit = QLineEdit()
        quantity_edit.setValidator(validator)
        quantity_edit.setPlaceholderText("0")
        quantity_edit.setObjectName("MaterialGridInput")
        quantity_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(quantity_edit, row_idx, 2)
        row_widgets[KEY_QUANTITY] = quantity_edit
        quantity_edit.textChanged.connect(self._on_value_changed)

        unit_combo_m3 = QComboBox()
        unit_combo_m3.setObjectName("MaterialGridInput")
        unit_combo_m3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(unit_combo_m3, row_idx, 3)
        row_widgets[KEY_UNIT_M3] = unit_combo_m3
        unit_combo_m3.currentTextChanged.connect(self._on_value_changed)

        rate_edit = QLineEdit()
        rate_edit.setValidator(validator)
        rate_edit.setPlaceholderText("0.00")
        rate_edit.setObjectName("MaterialGridInput")
        rate_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(rate_edit, row_idx, 4)
        row_widgets[KEY_RATE] = rate_edit
        rate_edit.textChanged.connect(self._on_value_changed)

        rate_data_source_edit = QLineEdit()
        rate_data_source_edit.setObjectName("MaterialGridInput")
        rate_data_source_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(rate_data_source_edit, row_idx, 5)
        row_widgets[KEY_RATE_DATA_SOURCE] = rate_data_source_edit
        rate_data_source_edit.textChanged.connect(self._on_value_changed)

        remove_button = QPushButton("x")
        remove_button.setFixedSize(24, 24)
        remove_button.setStyleSheet("""
            QPushButton {
                background-color: #FFCCCC;
                border: 1px solid #FF9999;
                border-radius: 12px;
                font-weight: bold;
                line-height:12px;
                padding: 0px;
                color: #CC0000;
            }
            QPushButton:hover {
                background-color: #FF9999;
                color: white;
            }
            QPushButton:pressed {
                background-color: #FF6666;
            }
        """)
        remove_button.clicked.connect(lambda: self.remove_material_row_by_widgets(row_widgets))
        self.material_grid_layout.addWidget(remove_button, row_idx, 6)
        row_widgets['remove_button'] = remove_button

        type_material_combo.currentTextChanged.connect(
            lambda text, grade_widget=grade_combo, unit_widget=unit_combo_m3: self._on_type_material_changed(text, grade_widget, unit_widget)
        )

        self.material_rows.append(row_widgets)
        self.current_material_row_idx += 1

        selected_component = self.component_combobox.currentText()
        materials = list(self.data.get(selected_component, {}).keys())
        type_material_combo.addItems(materials)
        
        if materials:
            first_material = materials[0]
            self.update_comp_grades(first_material, grade_combo)
            self.update_comp_units(first_material, unit_combo_m3)

        self.updateGeometry()
        self.adjustSize()
        self._on_value_changed()


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
        self._on_value_changed()

class Foundation(QWidget):
    closed = Signal()
    next = Signal(str)
    back = Signal(str)
    def __init__(self, database, parent=None):
        super().__init__()
        self.database_manager = database
        self.data_id = []
        self.setObjectName("central_panel_widget")
        self.component_widgets = []
        self._initializing = True
        self.state_changed = True
        self.is_first_visit = True
        self.is_locked = False
        
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
            
            QPushButton#lock_button {
                background: transparent;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                color: #3F3E5E;
                padding: 2px 2px;
                text-align: center;
                font-weight: bold;
            }
            QPushButton#lock_button:hover {
                background: transparent;
                border-color: #C0C0C0;
            }
            QPushButton#lock_button[locked="true"] {
                background: transparent;
                border-color: #FF9999;
                color: #CC0000;
            }
            QPushButton#lock_button[locked="false"] {
                background: transparent;
                border-color: #45913E;
                color: #00AA00;
            }
            QLineEdit {
                text-align: center;
            }
            QComboBox {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
                text-align: center;
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
            #MaterialGridInput:disabled {
                background-color: #F0F0F0;
                color: #888888;
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
            QPushButton#add_material_button:disabled, QPushButton#add_component_button:disabled {
                background-color: #F0F0F0;
                color: #AAAAAA;
                border-color: #D0D0D0;
            }
        """)
        
        left_panel_vlayout = QVBoxLayout(self)
        left_panel_vlayout.setContentsMargins(0,0,0,0)
        left_panel_vlayout.setSpacing(0)

        lock_hlayout = QHBoxLayout()
        lock_hlayout.setContentsMargins(0,2,2,0)
        lock_hlayout.setSpacing(0)
        lock_hlayout.addStretch()

        self.lock_button = QPushButton("🔓")
        self.lock_button.setObjectName("lock_button")
        self.lock_button.setFixedSize(24, 24)
        self.lock_button.setProperty("locked", "false")
        self.lock_button.clicked.connect(self.toggle_lock)
        lock_hlayout.addWidget(self.lock_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        scroll_content_widget = QWidget()
        scroll_content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        scroll_content_widget.setObjectName("scroll_content_widget")
        self.scroll_area.setWidget(scroll_content_widget)

        self.scroll_content_layout = QVBoxLayout(scroll_content_widget)
        self.scroll_content_layout.setContentsMargins(0,0,0,0)
        self.scroll_content_layout.setSpacing(0)

        self.scroll_content_layout.addLayout(lock_hlayout)

        self.add_component_button = QPushButton("+ Add Component")
        self.add_component_button.setObjectName("add_component_button")
        self.add_component_button.clicked.connect(self.add_component_layout)

        self.button_h_layout = QHBoxLayout()
        self.button_h_layout.setSpacing(10)
        self.button_h_layout.setContentsMargins(10,10,10,10)

        self.button_h_layout.addStretch(6)

        next_button = QPushButton("Next")
        next_button.setObjectName("nav_button")
        next_button.clicked.connect(self.on_next_clicked)
        self.button_h_layout.addWidget(next_button)

        self.add_component_layout()

        self.scroll_content_layout.addLayout(self.button_h_layout)
        left_panel_vlayout.addWidget(self.scroll_area)
        self._initializing = False

    def showEvent(self, event):
        super().showEvent(event)
        if not self.is_first_visit:
            self.set_form_locked(True)
        else:
            self.is_first_visit = False

    def toggle_lock(self):
        self.set_form_locked(not self.is_locked)
    
    def set_form_locked(self, locked):
        self.is_locked = locked
        
        if locked:
            self.lock_button.setText("🔒")
            self.lock_button.setProperty("locked", "true")
        else:
            self.lock_button.setText("🔓")
            self.lock_button.setProperty("locked", "false")
        
        self.lock_button.style().unpolish(self.lock_button)
        self.lock_button.style().polish(self.lock_button)
        
        for component_widget in self.component_widgets:
            component_widget.set_locked(locked)
        
        self.add_component_button.setEnabled(not locked)

    def collect_data(self):
        all_data = []
        for component_widget in self.component_widgets:
            component_data = component_widget.collect_data()
            all_data.append(component_data)
        return all_data
    
    def mark_state_changed(self):
        if self._initializing:
            return
        self.state_changed = True
    
    def save_data(self):
        from pprint import pprint
        data = self.collect_data()
        print("\nCollected Data from Foundation UI:")
        pprint(data)
            
        if self.data_id:
            self.data_id = self.database_manager.replace_structure_work_rows(KEY_FOUNDATION, data, self.data_id)
        else:
            self.data_id = self.database_manager.input_data_row(KEY_FOUNDATION, data)
        self.state_changed = False

    def on_next_clicked(self):
        if not self.state_changed:
            self.next.emit(KEY_FOUNDATION)
            return
        if self.data_id:
            message = "Do you want to replace previous data?"
        else:
            message = "Do you want to save data?"
        reply = QMessageBox.question(self, "Confirm", message, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.save_data()
        self.next.emit(KEY_FOUNDATION)

    def add_component_layout(self):
        new_component = ComponentWidget(self)
        self.component_widgets.append(new_component)
        new_component.remove_component_button.clicked.connect(lambda: self.remove_component_layout(new_component))

        if self.scroll_content_layout.indexOf(self.add_component_button) != -1:
            self.scroll_content_layout.removeWidget(self.add_component_button)
        if self.scroll_content_layout.indexOf(self.button_h_layout) != -1:
            self.scroll_content_layout.removeItem(self.button_h_layout)

        self.scroll_content_layout.addWidget(new_component)
        self.scroll_content_layout.addWidget(self.add_component_button, alignment=Qt.AlignCenter)
        self.scroll_content_layout.addLayout(self.button_h_layout)

        if self.is_locked:
            new_component.set_locked(True)

        self.scroll_area.widget().updateGeometry()
        self.scroll_area.widget().adjustSize()
        self.mark_state_changed()

    def remove_component_layout(self, component_to_remove):
        if component_to_remove in self.component_widgets:
            self.scroll_content_layout.removeWidget(component_to_remove)
            self.component_widgets.remove(component_to_remove)
            component_to_remove.deleteLater()
            self.scroll_area.widget().updateGeometry()
            self.scroll_area.widget().adjustSize()
            self.mark_state_changed()

    def expand_scroll_area(self):
        self.central_widget.layout().invalidate()

    def close_widget(self):
        self.closed.emit()
        self.setParent(None)