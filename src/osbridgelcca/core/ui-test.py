
import sys
import copy
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QLineEdit, QLabel, QMessageBox, QScrollArea, QFrame
)
from osbridgelcca.core.material_types_consts import (
    MATERIAL_COSTS_TEMPLATE,
    get_materials, get_submaterials, get_units, set_material_cost
)
# Add import for saving user data
from osbridgelcca.backend.api.routes.user_data import save_user_input

print("Material Cost Editor UI Test")

class MaterialRow(QWidget):

    def __init__(self, material_costs):
        super().__init__()
        self.material_costs = material_costs

        layout = QHBoxLayout()

        # Material dropdown
        self.material_cb = QComboBox()
        self.material_cb.addItems(get_materials(self.material_costs))
        self.material_cb.currentTextChanged.connect(self.update_submaterials)
        layout.addWidget(QLabel("Material:"))
        layout.addWidget(self.material_cb)

        # Submaterial dropdown
        self.submaterial_cb = QComboBox()
        layout.addWidget(QLabel("Submaterial:"))
        layout.addWidget(self.submaterial_cb)

        # Unit dropdown
        self.unit_cb = QComboBox()
        layout.addWidget(QLabel("Unit:"))
        layout.addWidget(self.unit_cb)

        # Cost input
        self.cost_input = QLineEdit()
        self.cost_input.setPlaceholderText("Enter cost")
        layout.addWidget(QLabel("Cost:"))
        layout.addWidget(self.cost_input)

        self.setLayout(layout)

        # Connect submaterial change signal only once
        self.submaterial_cb.currentTextChanged.connect(self.update_units)

        # Initialize submaterials and units for the first material
        initial_material = self.material_cb.currentText()
        self.update_submaterials(initial_material)

    def update_submaterials(self, material):
        self.submaterial_cb.clear()
        submaterials = get_submaterials(self.material_costs, material)
        self.submaterial_cb.addItems(submaterials)
        self.update_units()

    def update_units(self):
        material = self.material_cb.currentText()
        self.unit_cb.clear()
        units = get_units(self.material_costs, material)
        self.unit_cb.addItems(units)


class MaterialCostApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Material Cost Editor")

        self.material_costs = copy.deepcopy(MATERIAL_COSTS_TEMPLATE)

        self.layout = QVBoxLayout()

        # Container for rows with scrollbar
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.rows_container = QFrame()
        self.rows_layout = QVBoxLayout()
        self.rows_container.setLayout(self.rows_layout)
        self.scroll_area.setWidget(self.rows_container)

        self.layout.addWidget(self.scroll_area)

        # Add buttons
        btn_layout = QHBoxLayout()
        self.add_material_btn = QPushButton("Add Material")
        self.add_material_btn.clicked.connect(self.add_material_row)
        btn_layout.addWidget(self.add_material_btn)

        self.save_btn = QPushButton("Save All")
        self.save_btn.clicked.connect(self.save_all)
        btn_layout.addWidget(self.save_btn)

        self.layout.addLayout(btn_layout)

        self.setLayout(self.layout)

        # Add initial row
        self.add_material_row()

    def add_material_row(self):
        row = MaterialRow(self.material_costs)
        self.rows_layout.addWidget(row)

    def save_all(self):
        # Iterate over each row and save costs
        for i in range(self.rows_layout.count()):
            row = self.rows_layout.itemAt(i).widget()
            material = row.material_cb.currentText()
            submaterial = row.submaterial_cb.currentText()
            unit = row.unit_cb.currentText()
            cost_text = row.cost_input.text()

            try:
                cost = float(cost_text)
            except ValueError:
                QMessageBox.warning(self, "Invalid input",
                                    f"Invalid cost value in row {i+1}: '{cost_text}'")
                return

            set_material_cost(self.material_costs, material, submaterial, unit, cost)

        # Save to file
        save_user_input(self.material_costs)

        QMessageBox.information(self, "Success", "All costs saved successfully!")

        # For demo, print the updated costs
        print(self.material_costs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MaterialCostApp()
    window.resize(900, 400)
    window.show()
    sys.exit(app.exec_())
