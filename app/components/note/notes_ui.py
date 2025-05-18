from PySide6.QtWidgets import QVBoxLayout, QFrame, QWidget
from PySide6.QtCore import Qt


from app.components.note.modes.cluster_mode_widget import ClusterModeWidget
from app.components.buttons.button_icon import ButtonIcon
from app.components.inputs.input_default import Input_Default

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
    leftbar_layout.addWidget(self.toolbar)
    leftbar_layout.addWidget(line1, alignment=Qt.AlignHCenter)
    leftbar_layout.addWidget(self.note_mode)
    leftbar_layout.addWidget(line2, alignment=Qt.AlignHCenter)
    leftbar_layout.addWidget(self.calender_button)

    # Search bar
    self.search_input = Input_Default(placeholder="Rechercher une note", x=230, parent=self)
    self.search_input.raise_()
    self.search_input.textChanged.connect(self.on_search_note)

    # Add note widget
    self.add_note_widget = None

    # Note Detail
    self.note_detail_left_margin = 16  # à droite de la toolbar et search input
    self.note_detail_top_margin = 16 + self.toolbar.height() + 6
    self.note_detail_widget = None




    