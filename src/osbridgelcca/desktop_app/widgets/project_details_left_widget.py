from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, Qt, QSize, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QTextEdit, QWidget, QLabel, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy)
from PySide6.QtGui import QIcon, QTextDocument
import sys
import os
from widgets.structure_works_data.foundation_widget import Foundation
from widgets.structure_works_data.super_structure_widget import SuperStructure
from widgets.structure_works_data.sub_structure_widget import SubStructure
from widgets.structure_works_data.auxiliary_works_widget import AuxiliaryWorks
from PySide6.QtWidgets import QStackedWidget
from .utils.data import *

class ProjectDetailsLeft(QWidget):
    closed = Signal()
    """
    The main application window that uses a custom title bar.
    """
    def __init__(self, widget_map, parent):
        super().__init__()
        self.widget_map = widget_map
        self.parent = parent

        self.current_selected_button = None
        self.all_param_buttons = {}

        self.setObjectName("left_panel_widget")
        self.setStyleSheet("""
           #left_panel_widget {
                background-color: #F8F8F8;
                border-radius: 8px;
            }
            #left_panel_widget QLabel {
                color: #333333;
                font-size: 12px;
            }
            #left_panel_widget QLabel#page_number_label {
                font-size: 14px;
                font-weight: bold;
                color: #555555;
            }                         
            QScrollArea {
                border: 1px solid #000000;
                background-color: transparent;
                outline: none;            
            }
            QScrollArea > QWidget {
                background-color: transparent;
            }
            QScrollBar:vertical {
                width: 12px;
                margin: 0px;
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
                background-color: #F0E6E6;
                border: 1px solid #000000;
                border-bottom: none;
                text-align: left;
                padding: 4px 10px;
                color: #000000;        
            }
            QPushButton#top_button_left_panel:hover {
                background-color: #FDEFEF;
            }
            QPushButton#top_button_left_panel:pressed {
                background-color: #FFF3F3;
            }                         
            #input_output_header {
                background-color: #F0E6E6;
                margin-top: 0px;
                margin-bottom: 0px;
                padding: 0px;
            }
            #input_output_header QLabel {
                font-size: 15px; 
                font-weight: bold; 
                color: #333; 
                letter-spacing: 1px; 
                padding: 8px 0 8px 0;
                background: transparent;
            }
            #input_output_separator {
                background-color: #F0E6E6;
                height: 10px;
                border-bottom: 1px solid black;
            }
            QPushButton.category_button { 
                background-color: transparent;
                border: none;
                text-align: left;
                padding: 6px 0px 6px 15px;
                color: #000;
                font-size: 13px;
            }
            QPushButton.category_button:hover {
                background-color: #2A3F54;
                color: #FFFFFF;
            }
            QPushButton.subcategory_button {
                background-color: transparent;
                border: none;
                text-align: left;
                padding: 4px 0px 4px 30px;
                color: #000;
                font-size: 12px;
            }
            QPushButton.subcategory_button:hover {
                background-color: #2A3F54;
                color: #FFFFFF;
            }
            QPushButton.category_button[selected="true"],
            QPushButton.subcategory_button[selected="true"] {
                background-color: #2A3F54;
                color: #FFFFFF;
            }
            QLabel.output_label {
                background-color: transparent;
                color: #808080;
                font-size: 12px;
            }
        """)
        left_panel_vlayout = QVBoxLayout(self)
        left_panel_vlayout.setContentsMargins(0, 0, 0, 0)
        left_panel_vlayout.setSpacing(0)

        top_h_layout_left_panel = QHBoxLayout()
        top_button_left_panel = QPushButton("Project Details Window")
        top_button_left_panel.setIcon(QIcon("resources/close.png"))
        top_button_left_panel.setIconSize(QSize(13, 13))
        top_button_left_panel.setObjectName("top_button_left_panel")
        top_button_left_panel.setLayoutDirection(Qt.RightToLeft)
        top_button_left_panel.clicked.connect(self.close_widget)
        top_h_layout_left_panel.addWidget(top_button_left_panel, 2)
        top_h_layout_left_panel.addStretch(1)
        left_panel_vlayout.addLayout(top_h_layout_left_panel)

        bordered_spacer_widget = QWidget()
        bordered_spacer_widget.setObjectName("bordered_spacer_widget")
        bordered_spacer_widget.setFixedHeight(50)
        bordered_spacer_widget.setStyleSheet("""
            #bordered_spacer_widget {
                background-color: #F0E6E6;
                border: 1px solid black;
                border-bottom: none;                            
            }
        """)
        left_panel_vlayout.addWidget(bordered_spacer_widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content_widget = QWidget()
        scroll_area.setWidget(scroll_content_widget)
        scroll_content_layout = QVBoxLayout(scroll_content_widget)
        scroll_content_layout.setContentsMargins(0, 0, 0, 0)
        scroll_content_layout.setSpacing(0)

        input_param_header = QWidget()
        input_param_header.setObjectName("input_param_header")
        input_param_header.setStyleSheet("""
            #input_param_header {
                background-color: #F0E6E6;
            }
        """)
        input_param_header_layout = QVBoxLayout(input_param_header)
        input_param_header_layout.setContentsMargins(0, 0, 0, 0)
        input_param_header_layout.setSpacing(0)
        input_param_label = QLabel("Input Parameters")
        input_param_label.setAlignment(Qt.AlignCenter)
        input_param_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #333; padding: 8px 0 8px 0; background: transparent;border:none;")
        input_param_header_layout.addWidget(input_param_label)
        scroll_content_layout.addWidget(input_param_header)

        header_separator = QWidget()
        header_separator.setObjectName("input_output_separator")
        header_separator.setFixedHeight(2)
        scroll_content_layout.addWidget(header_separator)

        # Define icons for the four states of category buttons
        unselected_unexpanded_icon = QIcon("resources/play-button-arrowhead.png")
        unselected_sub_icon = QIcon("resources/play-button-arrowhead.png")

        self.current_selected_button = None
        self.all_param_buttons = {}
        button_data = {
            KEY_STRUCTURE_WORKS_DATA: [KEY_FOUNDATION, KEY_SUPERSTRUCTURE, KEY_SUBSTRUCTURE, KEY_AUXILIARY],
            KEY_FINANCIAL: [],
            KEY_CARBON_EMISSION: [KEY_CARBON_EMISSION_COST],
            KEY_BRIDGE_TRAFFIC: [],
            KEY_MAINTAINANCE_REPAIR: [],
            KEY_DEMOLITION_RECYCLE: []
        }
        for label, sublabels in button_data.items():
            btn = QPushButton(label)
            btn.setProperty("class", "category_button")
            btn.setProperty("selected", False)
            btn.setProperty("expanded", False)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setLayoutDirection(Qt.LeftToRight)
            btn.setFocusPolicy(Qt.StrongFocus)
            btn.setIcon(unselected_unexpanded_icon)
            btn.setIconSize(QSize(10, 10))
            btn.clicked.connect(lambda checked ,b=btn ,name=label: self.show_structure_widget(name, b))
            scroll_content_layout.addWidget(btn)
            self.all_param_buttons[label] = btn
            if sublabels:
                sub_widgets = []
                for sublabel in sublabels:
                    sub_btn = QPushButton(sublabel)
                    sub_btn.setProperty("class", "subcategory_button")
                    sub_btn.setProperty("selected", False)
                    sub_btn.setIcon(unselected_sub_icon)
                    sub_btn.setIconSize(QSize(10, 10))
                    sub_btn.setFocusPolicy(Qt.StrongFocus)
                    sub_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    sub_btn.setLayoutDirection(Qt.LeftToRight)
                    sub_btn.setVisible(False)
                    sub_btn.clicked.connect(lambda checked ,b=sub_btn, name=sublabel: self.show_structure_widget(name,b))
                    scroll_content_layout.addWidget(sub_btn)
                    sub_widgets.append(sub_btn)
                    self.all_param_buttons[sublabel] = sub_btn                
                
                def make_toggle(button, sub_widgets):
                    def toggle():
                        is_expanded = button.property("expanded")
                        for widget in sub_widgets:
                            widget.setVisible(not widget.isVisible())
                        button.setProperty("expanded", not is_expanded)
                        self.update_button_icon(button)
                        self.handle_button_selection(button)
                    return toggle
                btn.clicked.connect(lambda checked, b=btn, sw=sub_widgets: make_toggle(b, sw)())
        
        input_output_middle_separator = QWidget()
        input_output_middle_separator.setObjectName("input_output_separator")
        input_output_middle_separator.setFixedHeight(2)
        scroll_content_layout.addWidget(input_output_middle_separator)

        output_header = QWidget()
        output_header.setObjectName("input_param_header")
        output_header.setStyleSheet("""
            #input_param_header {
                background-color: #F0E6E6;
            }
        """)
        output_header_layout = QVBoxLayout(output_header)
        output_header_layout.setContentsMargins(0, 0, 0, 0)
        output_header_layout.setSpacing(0)
        output_label = QLabel("Output")
        output_label.setAlignment(Qt.AlignCenter)
        output_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #333; letter-spacing: 1px; padding: 8px 0 8px 0; background: transparent;")
        output_header_layout.addWidget(output_label)
        scroll_content_layout.addWidget(output_header)

        output_header_separator = QWidget()
        output_header_separator.setObjectName("input_output_separator")
        output_header_separator.setFixedHeight(2)
        scroll_content_layout.addWidget(output_header_separator)

        output_labels_data = [
            "Initial Construction Cost", "Initial Carbon Emission Cost", "Time Cost", 
            "Road User Cost", "Carbon Emission due to Re-Routing", "Periodic Maintenance Costs",
            "Maintenance Emission Costs", "Routine Inspection Costs", "Repair & Rehabilitation Costs",
            "Reconstruction Costs", "Demolition & Disposal Cost", "Recycling Cost", "Total Life-Cycle Cost"
        ]
        output_layout = QVBoxLayout()
        output_layout.setContentsMargins(10, 10, 10, 10)
        for text in output_labels_data:
            output_item = QLabel(text)
            output_item.setProperty("class", "output_label")
            output_layout.addWidget(output_item)
        scroll_content_layout.addLayout(output_layout)
        scroll_content_layout.addStretch(1)

        scroll_content_widget.setStyleSheet("""
        QPushButton[selected="true"] {
            background-color: #2A3F54;
            color: #FFFFFF;
        }
        QPushButton[selected="false"], QPushButton {
            background-color: transparent;
            color: #000000;
        }
        """)
        left_panel_vlayout.addWidget(scroll_area)
    
    def handle_button_selection(self, button_clicked=None, button_name=None):
        """
        Handles the visual selection state of buttons in the side panel.
        """
        for b in self.all_param_buttons.values():
            b.setProperty("selected", False)
            b.style().unpolish(b)
            b.style().polish(b)
            if b.property("class") == "subcategory_button":
                b.setIcon(QIcon("resources/play-button-arrowhead.png"))
            else:
                self.update_button_icon(b)
            
            if button_name:
                if b.text() == button_name:
                    button_clicked = b
                    button_clicked.click()

        button_clicked.setProperty("selected", True)
        button_clicked.style().unpolish(button_clicked)
        button_clicked.style().polish(button_clicked)
        if button_clicked.property("class") == "subcategory_button":
            button_clicked.setIcon(QIcon("resources/play-button-selected.png"))
        else:
            self.update_button_icon(button_clicked)
        self.current_selected_button = button_clicked
    
    def update_button_icon(self, button):
        """
        Updates the icon of a category button based on its selected and expanded state.
        """
        if button.property("class") != "category_button":
            return
        is_selected = button.property("selected")
        is_expanded = button.property("expanded")
        if is_selected and is_expanded:
            button.setIcon(QIcon("resources/arrow_down_selected.png"))
        elif is_selected:
            button.setIcon(QIcon("resources/play-button-selected.png"))
        elif is_expanded:
            button.setIcon(QIcon("resources/arrow_down.png"))
        else:
            button.setIcon(QIcon("resources/play-button-arrowhead.png"))
        button.setIconSize(QSize(10, 10))

    def show_structure_widget(self, name, btn):
        self.parent.show_project_detail_widgets(name)
        self.handle_button_selection(btn)

    def close_widget(self):
        self.closed.emit()
        self.setParent(None)