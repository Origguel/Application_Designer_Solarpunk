from PySide6.QtWidgets import QWidget, QLabel, QGridLayout
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Qt
from app.components.buttons.button_icon import ButtonIcon

import os
import json
from pathlib import Path


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

        # 🧩 Obtenir l’ID du projet sélectionné
        selected_project_id = self.get_selected_project_id()
        if not selected_project_id:
            print("❌ Aucun projet sélectionné.")
            return

        # 📂 Construire le chemin vers le dossier des photos
        folder = Path(f"data/projets/Photos/{selected_project_id}")
        if not folder.exists():
            print(f"📁 Dossier photos introuvable pour {selected_project_id}, création automatique.")
            try:
                folder.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"❌ Impossible de créer le dossier : {e}")
                return


        # 📸 Lister les fichiers image valides
        image_paths = sorted([
            str(p) for p in folder.glob("*.png")
        ])

        # 🧱 Afficher les photos
        for i, path in enumerate(image_paths):
            label = QLabel()
            label.setFixedSize(443, 266)
            label.setStyleSheet("border-radius: 6px; background-color: #F4B67C;")
            label.setAlignment(Qt.AlignCenter)

            if os.path.exists(path):
                original = QPixmap(path)
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

            row = i // 2
            col = i % 2
            self.layout.addWidget(label, row, col)

        # ➕ Ajouter le bouton en dernier
        total_photos = len(image_paths)
        row = total_photos // 2
        col = total_photos % 2

        add_button = ButtonIcon(icon_name="image", icon_color="black", style="Button_Medium", x=443, y=266)
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