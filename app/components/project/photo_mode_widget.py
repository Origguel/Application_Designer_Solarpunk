from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QFrame, QFileDialog
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Qt
from app.components.buttons.button_icon import ButtonIcon

import os
import json
from pathlib import Path
import shutil


class PhotoModeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("PhotoModeWidget")

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setHorizontalSpacing(16)
        self.layout.setVerticalSpacing(16)

        self.setLayout(self.layout)
        self.setVisible(False)

        self.load_photos()  # initial load

    def clear_photos(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    def load_photos(self):
        self.clear_photos()

        selected_project_id = self.get_selected_project_id()
        if not selected_project_id:
            print("❌ Aucun projet sélectionné.")
            return

        folder = Path(f"data/projets/Photos/{selected_project_id}")
        folder.mkdir(parents=True, exist_ok=True)
        image_paths = sorted(folder.glob("*.png"))

        for i, path in enumerate(image_paths):
            frame = PhotoFrame()
            frame.setFixedSize(443, 266)

            label = QLabel(frame)
            label.setFixedSize(443, 266)
            label.setAlignment(Qt.AlignCenter)

            if path.exists():
                original = QPixmap(str(path))
                scaled = original.scaled(label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

                rounded = QPixmap(label.size())
                rounded.fill(Qt.transparent)

                painter = QPainter(rounded)
                painter.setRenderHint(QPainter.Antialiasing)
                clip_path = QPainterPath()
                clip_path.addRoundedRect(0, 0, label.width(), label.height(), 6, 6)
                painter.setClipPath(clip_path)
                painter.drawPixmap(0, 0, scaled)
                painter.end()

                label.setPixmap(rounded)
            else:
                label.setText("📸")

            delete_button = ButtonIcon(icon_name="trash", icon_color="white", style="Button_EveryBackground", parent=frame)
            delete_button.move(443 - 32 - 6, 6)
            delete_button.clicked.connect(lambda _, p=path: self.delete_photo(p))

            frame.set_delete_button(delete_button)

            row = i // 2
            col = i % 2
            self.layout.addWidget(frame, row, col)

        # ➕ Ajouter bouton "ajouter"
        total_photos = len(image_paths)
        row = total_photos // 2
        col = total_photos % 2

        add_button = ButtonIcon(icon_name="image", icon_color="black", style="Button_Medium", x=443, y=266)
        add_button.clicked.connect(self.handle_add_photo)
        self.layout.addWidget(add_button, row, col, alignment=Qt.AlignLeft)

    def get_selected_project_id(self):
        selection_path = Path("assets/project/project_selected.json")
        if not selection_path.exists():
            return None

        try:
            with open(selection_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("project_id_selected")
        except Exception as e:
            print(f"❌ Erreur lecture projet sélectionné : {e}")
            return None

    def handle_add_photo(self):
        selected_project_id = self.get_selected_project_id()
        if not selected_project_id:
            print("❌ Aucun projet sélectionné pour l'ajout d'image.")
            return

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Ajouter des images au projet",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if not files:
            return

        folder = Path(f"data/projets/Photos/{selected_project_id}")
        folder.mkdir(parents=True, exist_ok=True)

        existing = sorted(folder.glob("*.*"))
        start_index = len(existing) + 1

        for i, file_path in enumerate(files, start=start_index):
            extension = Path(file_path).suffix.lower()
            target = folder / f"{i:04}{extension}"
            shutil.copy(file_path, target)

        self.load_photos()

    def delete_photo(self, path: Path):
        try:
            os.remove(path)
            print(f"🗑️ Supprimé : {path}")
            self.load_photos()
        except Exception as e:
            print(f"❌ Erreur suppression {path}: {e}")


class PhotoFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.delete_button = None

    def set_delete_button(self, button):
        self.delete_button = button
        if self.delete_button:
            self.delete_button.hide()

    def enterEvent(self, event):
        if self.delete_button:
            self.delete_button.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.delete_button:
            self.delete_button.hide()
        super().leaveEvent(event)
