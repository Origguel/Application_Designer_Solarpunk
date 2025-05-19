from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QWidget
from PySide6.QtCore import Qt
from datetime import datetime

# Components
from app.components.buttons.button_icon import ButtonIcon
from app.components.buttons.button_text import ButtonText
from app.components.inputs.input_default import Input_Default
from app.components.inputs.input_multiline import Input_Multiline
from app.components.dropdowns.dropdown_default import Dropdown_Default



def Project_UI(self):
    # Toolbar
    self.toolbar = QWidget(self)
    toolbar_layout = QVBoxLayout(self.toolbar)
    toolbar_layout.setContentsMargins(0, 0, 0, 0)
    toolbar_layout.setSpacing(6)
    # Toolbar Buttons
    self.list_button = ButtonIcon("list", parent=self.toolbar)
    self.plus_button = ButtonIcon("add", parent=self.toolbar)
    self.delete_button = ButtonIcon("trash", parent=self.toolbar)
    # Toolbar Buttons Order
    toolbar_layout.addWidget(self.list_button)
    toolbar_layout.addWidget(self.plus_button)
    toolbar_layout.addWidget(self.delete_button)
    # Toolbar Buttons Click
    self.list_button.clicked.connect(self.toggle_project_list)
    self.plus_button.clicked.connect(self.toggle_add_project)
    self.delete_button.clicked.connect(self.delete_project)

    # Project_mode
    self.project_mode = QWidget(self)
    project_mode_layout = QVBoxLayout(self.project_mode)
    project_mode_layout.setContentsMargins(0, 0, 0, 0)
    project_mode_layout.setSpacing(6)
    # Project_mode Buttons
    self.prisedenote_button = ButtonIcon("prise_de_note", parent=self.project_mode)
    self.notation_button = ButtonIcon("notation", parent=self.project_mode)
    self.finalisation_button = ButtonIcon("finalisation", parent=self.project_mode)
    # Project_mode Buttons Order
    project_mode_layout.addWidget(self.prisedenote_button)
    project_mode_layout.addWidget(self.notation_button)
    project_mode_layout.addWidget(self.finalisation_button)
    # Project_mode Buttons Click
    self.prisedenote_button.clicked.connect(self.toggle_prisedenote)
    self.notation_button.clicked.connect(self.toggle_notation)
    self.finalisation_button.clicked.connect(self.toggle_finalisation)

    # Lines
    line1 = QFrame()
    line1.setFixedSize(6, 1)
    line1.setStyleSheet("background-color: #2B2B2B; border: none;")
    line2 = QFrame()
    line2.setFixedSize(6, 1)
    line2.setStyleSheet("background-color: #2B2B2B; border: none;")

    # Left Bar
    self.leftbar = QWidget(self)
    leftbar_layout = QVBoxLayout(self.leftbar)
    leftbar_layout.setContentsMargins(0, 0, 0, 0)
    leftbar_layout.setSpacing(6)
    # Left Bar contenu
    leftbar_layout.addWidget(self.toolbar)
    leftbar_layout.addWidget(line1, alignment=Qt.AlignHCenter)
    leftbar_layout.addWidget(self.project_mode)





    # Project List
    self.project_list_item1 = ButtonText("Projet 1", style="Button_Default_Left", x=370, parent=self)
    self.project_list_item2 = ButtonText("Projet 2", style="Button_Default_Left", x=370, parent=self)
    self.project_list_item3 = ButtonText("Projet 3", style="Button_Default_Left", x=370, parent=self)
    self.project_list_item4 = ButtonText("Projet 4", style="Button_Default_Left", x=370, parent=self)
    
    self.project_list = QWidget(self)
    project_list_layout = QVBoxLayout(self.project_list)
    project_list_layout.setContentsMargins(0, 0, 0, 0)
    project_list_layout.setSpacing(6)

    project_list_layout.addWidget(self.project_list_item1)
    project_list_layout.addWidget(self.project_list_item2)
    project_list_layout.addWidget(self.project_list_item3)
    project_list_layout.addWidget(self.project_list_item4)

    self.project_list.hide()
    self.project_list.setEnabled(False)