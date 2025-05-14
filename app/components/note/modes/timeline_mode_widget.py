from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from datetime import datetime
from app.components.note.modes.timeline.timeline_canvas import TimelineCanvas


class TimelineModeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TimelineModeWidget")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.canvas = TimelineCanvas(self)
        layout.addWidget(self.canvas)
