from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QWidget
from PySide6.QtCore import Qt
from datetime import datetime

# Components
from app.components.note.modes.cluster_mode_widget import ClusterModeWidget
from app.components.buttons.button_icon import ButtonIcon
from app.components.buttons.button_text import ButtonText
from app.components.inputs.input_default import Input_Default
from app.components.inputs.input_multiline import Input_Multiline
from app.components.dropdowns.dropdown_default import Dropdown_Default



def setup_ui(self, note_id):
    # Toolbar
    self.toolbar = QWidget(self)
    toolbar_layout = QVBoxLayout(self.toolbar)
    toolbar_layout.setContentsMargins(0, 0, 0, 0)
    toolbar_layout.setSpacing(6)
    # Toolbar Buttons
    self.search_button = ButtonIcon("search", parent=self.toolbar)
    self.plus_button = ButtonIcon("toolbar_add", parent=self.toolbar)
    self.resetview_button = ButtonIcon("toolbar_resize", parent=self.toolbar)
    self.delete_button = ButtonIcon("trash", parent=self.toolbar)
    # Toolbar Buttons Order
    toolbar_layout.addWidget(self.search_button)
    toolbar_layout.addWidget(self.plus_button)
    toolbar_layout.addWidget(self.resetview_button)
    toolbar_layout.addWidget(self.delete_button)
    # Toolbar Buttons Click
    self.search_button.clicked.connect(self.toggle_search_input)
    self.plus_button.clicked.connect(self.toggle_addnote_input)
    self.resetview_button.clicked.connect(self.on_reset_view_button_clicked)
    self.delete_button.clicked.connect(self.on_delete_button_clicked)

    # Note_mode
    self.note_mode = QWidget(self)
    note_mode_layout = QVBoxLayout(self.note_mode)
    note_mode_layout.setContentsMargins(0, 0, 0, 0)
    note_mode_layout.setSpacing(6)
    # Note_mode Buttons
    self.cluster_button = ButtonIcon("toolbar_cluster", parent=self.note_mode)
    self.timeline_button = ButtonIcon("toolbar_timeline", parent=self.note_mode)
    self.theme_button = ButtonIcon("toolbar_theme", parent=self.note_mode)
    # Note_mode Buttons Order
    note_mode_layout.addWidget(self.cluster_button)
    note_mode_layout.addWidget(self.timeline_button)
    note_mode_layout.addWidget(self.theme_button)
    # Note_mode Buttons Click
    self.cluster_button.clicked.connect(self.toggle_cluster)
    self.timeline_button.clicked.connect(self.toggle_timeline)
    self.theme_button.clicked.connect(self.toggle_theme)

    # Calender
    self.calender_button = ButtonIcon("toolbar_calendrier", parent=self)

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
    leftbar_layout.addWidget(self.note_mode)
    leftbar_layout.addWidget(line2, alignment=Qt.AlignHCenter)
    leftbar_layout.addWidget(self.calender_button)





    self.search_input = Input_Default(placeholder="Rechercher une note", x=None, y=32, parent=self)
    self.search_input.textChanged.connect(self.on_search_note)

    self.searchbar_widget = QWidget(self)
    self.searchbar_widget_layout = QVBoxLayout(self.searchbar_widget)
    self.searchbar_widget_layout.setContentsMargins(0, 0, 0, 0)
    self.searchbar_widget_layout.addWidget(self.search_input)
    self.searchbar_widget.resize(32, 32)
    self.searchbar_widget.move(54, 16)
    self.searchbar_widget.hide()
    self.searchbar_widget.setEnabled(False)


    






    # Contenu du add note widget
    self.title_input = Input_Default(placeholder="Nom de la note", x=370, parent=self)
    self.description_input = Input_Multiline(placeholder="Description rapide de la note", x=370, y=64, parent=self)

    self.date_input = Input_Default(placeholder="Date de création de la note", x=218)
    today = datetime.now().strftime("%d/%m/%Y")
    self.date_input.setText(today)
    self.project_selector = Dropdown_Default(x=218, style="Dropdown_Default", items=["Projet 1", "Projet 2", "Projet 3", "Projet 4"], parent=self)

    self.notetype_text = ButtonIcon("note_text", parent=self)
    self.notetype_image = ButtonIcon("note_image", parent=self)
    self.notetype_video = ButtonIcon("note_video", parent=self)
    self.notetype_doc = ButtonIcon("note_doc", parent=self)
    self.notetype_lien = ButtonIcon("note_lien", parent=self)
    self.notetype_code = ButtonIcon("note_code", parent=self)

    self.contenu_input = Input_Multiline(placeholder="Contenu principal de la note", x=370, y=128, parent=self)
    self.createnote_button = ButtonText("Créer la note", x=94, parent=self)
    
    # Add note Widget part1_1 name description
    self.addnote_part1_1 = QWidget(self)
    addnote_part1_1_layout = QVBoxLayout(self.addnote_part1_1)
    addnote_part1_1_layout.setSpacing(6)
    addnote_part1_1_layout.setContentsMargins(0, 0, 0, 0)
    addnote_part1_1_layout.addWidget(self.title_input)
    addnote_part1_1_layout.addWidget(self.description_input)

    # Add note Widget part1_2 date projet
    self.addnote_part1_2_dp = QWidget(self)
    addnote_part1_2_dp_layout = QVBoxLayout(self.addnote_part1_2_dp)
    addnote_part1_2_dp_layout.setSpacing(6)
    addnote_part1_2_dp_layout.setContentsMargins(0, 0, 0, 0)
    addnote_part1_2_dp_layout.addWidget(self.date_input)
    addnote_part1_2_dp_layout.addWidget(self.project_selector)

    # Add note Widget part1_2 note type
    self.addnote_part1_2_nt = QWidget(self)
    addnote_part1_2_nt_layout = QGridLayout(self.addnote_part1_2_nt)
    addnote_part1_2_nt_layout.setHorizontalSpacing(6)
    addnote_part1_2_nt_layout.setVerticalSpacing(6)
    addnote_part1_2_nt_layout.setContentsMargins(0, 0, 0, 0)
    note_types = [
        self.notetype_text,
        self.notetype_image,
        self.notetype_video,
        self.notetype_doc,
        self.notetype_lien,
        self.notetype_code
    ]
    for index, widget in enumerate(note_types):
        row = index // 3
        col = index % 3
        addnote_part1_2_nt_layout.addWidget(widget, row, col)
    self.selected_note_type = None
    self.notetype_text.clicked.connect(lambda: self.set_note_type("text"))
    self.notetype_image.clicked.connect(lambda: self.set_note_type("image"))
    self.notetype_video.clicked.connect(lambda: self.set_note_type("video"))
    self.notetype_doc.clicked.connect(lambda: self.set_note_type("doc"))
    self.notetype_lien.clicked.connect(lambda: self.set_note_type("lien"))
    self.notetype_code.clicked.connect(lambda: self.set_note_type("code"))


    # Add note Widget part1_2 date projet type
    self.addnote_part1_2 = QWidget(self)
    addnote_part1_2_layout = QHBoxLayout(self.addnote_part1_2)
    addnote_part1_2_layout.setSpacing(6)
    addnote_part1_2_layout.setContentsMargins(0, 0, 0, 0)
    addnote_part1_2_layout.addWidget(self.addnote_part1_2_dp)
    addnote_part1_2_layout.addWidget(self.addnote_part1_2_nt)

    # Add note Widget part 1
    self.addnote_part1 = QWidget(self)
    addnote_part1_layout = QVBoxLayout(self.addnote_part1)
    addnote_part1_layout.setSpacing(6)
    addnote_part1_layout.setContentsMargins(0, 0, 0, 0)
    addnote_part1_layout.addWidget(self.addnote_part1_1)
    addnote_part1_layout.addWidget(self.addnote_part1_2)

    # Add note Widget part 2
    self.addnote_part2 = QWidget(self)
    addnote_part2_layout = QVBoxLayout(self.addnote_part2)
    addnote_part2_layout.setSpacing(6)
    addnote_part2_layout.setContentsMargins(0, 0, 0, 0)
    addnote_part2_layout.addWidget(self.contenu_input)
    addnote_part2_layout.addWidget(self.createnote_button, alignment=Qt.AlignRight)
    self.createnote_button.clicked.connect(self.validate_and_save_note)

    
    # Add note Widget
    self.addnote = QWidget(self)
    addnote_layout = QVBoxLayout(self.addnote)
    addnote_layout.setSpacing(6)
    addnote_layout.setContentsMargins(0, 0, 0, 0)
    addnote_layout.addWidget(self.addnote_part1)
    addnote_layout.addWidget(self.addnote_part2)
    self.addnote.resize(32, 500)
    self.addnote.move(54, 54)
    self.addnote.hide()
    self.addnote.setEnabled(False)