from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QWidget
from PySide6.QtCore import Qt
from datetime import datetime

# Components
from app.components.note.modes.cluster_mode_widget import ClusterModeWidget
from app.components.buttons.button_icon import ButtonIcon
from app.components.buttons.button_text import ButtonText
from app.components.inputs.input_default import Input_Default
from app.components.inputs.input_multiline import Input_Multiline
from app.components.dropdowns.dropdown_default import Dropdown_Default



def setup_ui(self):
    self.graph_widget = ClusterModeWidget(self.visualization_container)
    self.graph_widget.setGeometry(0, 0, self.width(), self.height())

    self.overlay = QWidget(self)
    self.overlay.setStyleSheet("background-color: rgba(255, 255, 255, 180);")
    self.overlay.hide()
    self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)

    # Toolbar
    self.toolbar = QWidget(self)
    toolbar_layout = QVBoxLayout(self.toolbar)
    toolbar_layout.setContentsMargins(0, 0, 0, 0)
    toolbar_layout.setSpacing(6)
    # Toolbar Buttons
    self.search_button = ButtonIcon("search", parent=self.toolbar)
    self.plus_button = ButtonIcon("add", parent=self.toolbar)
    self.resetview_button = ButtonIcon("resize", parent=self.toolbar)
    self.delete_button = ButtonIcon("trash", parent=self.toolbar)
    # Toolbar Buttons Order
    toolbar_layout.addWidget(self.search_button)
    toolbar_layout.addWidget(self.plus_button)
    toolbar_layout.addWidget(self.resetview_button)
    toolbar_layout.addWidget(self.delete_button)
    # Toolbar Buttons Click
    self.search_button.clicked.connect(self.toggle_search_input)
    self.plus_button.clicked.connect(self.open_add_note_widget)
    self.resetview_button.clicked.connect(self.on_reset_view_button_clicked)
    self.delete_button.clicked.connect(self.on_delete_button_clicked)

    # Note_mode
    self.note_mode = QWidget(self)
    note_mode_layout = QVBoxLayout(self.note_mode)
    note_mode_layout.setContentsMargins(0, 0, 0, 0)
    note_mode_layout.setSpacing(6)
    # Note_mode Buttons
    self.cluster_button = ButtonIcon("cluster", parent=self.note_mode)
    self.timeline_button = ButtonIcon("timeline", parent=self.note_mode)
    self.theme_button = ButtonIcon("theme", parent=self.note_mode)
    # Note_mode Buttons Order
    note_mode_layout.addWidget(self.cluster_button)
    note_mode_layout.addWidget(self.timeline_button)
    note_mode_layout.addWidget(self.theme_button)
    # Note_mode Buttons Click
    self.cluster_button.clicked.connect(lambda: self.switch_note_mode("cluster"))
    self.timeline_button.clicked.connect(lambda: self.switch_note_mode("timeline"))
    self.theme_button.clicked.connect(lambda: self.switch_note_mode("theme"))

    # Calender
    self.calender_button = ButtonIcon("calendar", parent=self)

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

    # Search bar
    self.search_input = Input_Default(placeholder="Rechercher une note", x=370, parent=self)
    self.search_input.raise_()
    self.search_input.textChanged.connect(self.on_search_note)
    self.search_input.hide()
    self.search_input.setEnabled(False)

    # Add note widget
    self.add_note_widget = None

    # Note Detail
    self.note_detail_left_margin = 16  # à droite de la toolbar et search input
    self.note_detail_top_margin = 16 + self.toolbar.height() + 6
    self.note_detail_widget = None

    






    # Contenu du add note widget
    self.name_input = Input_Default(placeholder="Nom de la note", x=370, parent=self)
    self.description_input = Input_Multiline(placeholder="Description rapide de la note", x=370, y=64, parent=self)

    self.date_input = Input_Default(placeholder="Date de création de la note", x=218)
    today = datetime.now().strftime("%d/%m/%Y")
    self.date_input.setText(today)
    self.project_selector = Dropdown_Default(x=218, style="Dropdown_Default", items=["Projet 1", "Projet 2", "Projet 3", "Projet 4"], parent=self)

    self.notetype_text = ButtonIcon("note_text", parent=self)
    self.notetype_image = ButtonIcon("note_image", parent=self)
    self.notetype_vidéo = ButtonIcon("note_video", parent=self)
    self.notetype_doc = ButtonIcon("note_doc", parent=self)
    self.notetype_lien = ButtonIcon("note_lien", parent=self)
    self.notetype_code = ButtonIcon("note_code", parent=self)
    self.notetype_dessin = ButtonIcon("note_dessin", parent=self)
    self.notetype_son = ButtonIcon("note_son", parent=self)

    self.contenu_input = Input_Multiline(placeholder="Contenu principal de la note", x=370, y=128, parent=self)
    self.createnote_button = ButtonText("Créer la note", x=94, parent=self)
    
    # Add note Widget part1_1 name description
    self.addnote_part1_1 = QWidget(self)
    addnote_part1_1_layout = QVBoxLayout(self.addnote_part1_1)
    addnote_part1_1_layout.setSpacing(6)
    addnote_part1_1_layout.setContentsMargins(0, 0, 0, 0)
    addnote_part1_1_layout.addWidget(self.name_input)
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
    addnote_part1_2_nt_layout = QHBoxLayout(self.addnote_part1_2_nt)
    addnote_part1_2_nt_layout.setSpacing(6)
    addnote_part1_2_nt_layout.setContentsMargins(0, 0, 0, 0)
    addnote_part1_2_nt_layout.addWidget(self.notetype_text)
    addnote_part1_2_nt_layout.addWidget(self.notetype_image)
    addnote_part1_2_nt_layout.addWidget(self.notetype_vidéo)
    addnote_part1_2_nt_layout.addWidget(self.notetype_doc)
    addnote_part1_2_nt_layout.addWidget(self.notetype_lien)
    addnote_part1_2_nt_layout.addWidget(self.notetype_code)
    addnote_part1_2_nt_layout.addWidget(self.notetype_dessin)
    addnote_part1_2_nt_layout.addWidget(self.notetype_son)

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
    
    # Add note Widget
    self.addnote = QWidget(self)
    addnote_layout = QVBoxLayout(self.addnote)
    addnote_layout.setSpacing(6)
    addnote_layout.setContentsMargins(0, 0, 0, 0)
    addnote_layout.addWidget(self.addnote_part1)
    addnote_layout.addWidget(self.addnote_part2)