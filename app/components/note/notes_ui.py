from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
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
    self.toolbar.setObjectName("Note_ToolsBar")
    self.toolbar.setFixedWidth(36)
    self.toolbar.setFixedHeight(104)

    toolbar_layout = QVBoxLayout(self.toolbar)
    toolbar_layout.setContentsMargins(3, 3, 3, 3)
    toolbar_layout.setSpacing(4)
    # Toolbar Buttons
    self.plus_button = ButtonIcon("add", style="Button_Secondary_Icon", parent=self.toolbar)
    self.resetview_button = ButtonIcon("resize", style="Button_Secondary_Icon", parent=self.toolbar)
    self.delete_button = ButtonIcon("trash", style="Button_Delete_Icon", parent=self.toolbar)

    toolbar_layout.addWidget(self.plus_button)
    toolbar_layout.addWidget(self.resetview_button)
    toolbar_layout.addWidget(self.delete_button)

    self.plus_button.clicked.connect(self.open_add_note_widget)
    self.resetview_button.clicked.connect(self.on_reset_view_button_clicked)
    self.delete_button.clicked.connect(self.on_delete_button_clicked)

    self.search_input = Input_Default(
        placeholder="Rechercher une note...",
        x=400, y=36,
        text_position="center-left",
        parent=self
    )
    self.search_input.raise_()
    self.search_input.textChanged.connect(self.on_search_note)

    self.add_note_widget = None

    # Positionner dynamiquement le détail de note sur la gauche (dans open_note_detail)
    self.note_detail_left_margin = 16  # à droite de la toolbar et search input
    self.note_detail_top_margin = 16 + self.toolbar.height() + 6
    self.note_detail_widget = None



    self.note_mode = QWidget(self)
    self.note_mode.setObjectName("Note_Mode_Bar")
    self.note_mode.setFixedWidth(104)
    self.note_mode.setFixedHeight(36)

    note_mode_layout = QHBoxLayout(self.note_mode)
    note_mode_layout.setContentsMargins(3, 3, 3, 3)
    note_mode_layout.setSpacing(4)

    self.note_mode_cluster = ButtonIcon("cluster", style="Button_Secondary_Icon", parent=self.note_mode)
    self.note_mode_timeline = ButtonIcon("timeline", style="Button_Secondary_Icon", parent=self.note_mode)
    self.note_mode_theme = ButtonIcon("theme", style="Button_Secondary_Icon", parent=self.note_mode)

    note_mode_layout.addWidget(self.note_mode_cluster)
    note_mode_layout.addWidget(self.note_mode_timeline)
    note_mode_layout.addWidget(self.note_mode_theme)

    self.note_mode_cluster.clicked.connect(lambda: self.switch_note_mode("cluster"))
    self.note_mode_timeline.clicked.connect(lambda: self.switch_note_mode("timeline"))
    self.note_mode_theme.clicked.connect(lambda: self.switch_note_mode("theme"))
