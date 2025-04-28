"""
Point d'entrée principal de ton application.
"""
import sys

import os
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

import app.resources_rc
print("resources_rc imported successfully")

from pathlib import Path
from PySide6.QtWidgets import QApplication
from app.views.home_view import HomeView

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # === Charger un fichier de style avec variables ===
    style_path = Path(__file__).parent / "styles" / "default.qss"
    if style_path.exists():
        with open(style_path, "r", encoding="utf-8") as f:
            style = f.read()
        app.setStyleSheet(style)

    else:
        print("⚠️ Fichier de style 'default.qss' non trouvé, l'application s'affichera sans thème.")

    # === Lancer la fenêtre principale ===
    window = HomeView()
    window.show()

    # === Démarrer l'application ===
    sys.exit(app.exec())
