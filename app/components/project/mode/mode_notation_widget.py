from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from pathlib import Path
import json

from app.components.buttons.button_icon import ButtonIcon
from app.components.labels.label_default import LabelDefault

class Mode_Notation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
