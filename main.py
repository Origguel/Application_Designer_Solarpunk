"""
Point d'entrée principal de ton application.
"""
import sys
import os
import time
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from app.views.home_view import HomeView
from custom_splash import CustomSplash

# === Ajouter le dossier "app" au chemin Python ===
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

# === Fonction pour charger automatiquement tous les fichiers .qss ===
def load_all_qss_from_dir(directory: Path, splash=None, app=None) -> str:
    style = ""
    qss_files = sorted(directory.glob("*.qss"))
    total = len(qss_files)

    for i, file in enumerate(qss_files):
        if splash and app:
            splash.set_progress(70 + int((i + 1) / total * 20), f"Chargement du style : {file.name}")
            app.processEvents()

        try:
            with open(file, "r", encoding="utf-8") as f:
                style += f"/* {file.name} */\n{f.read()}\n\n"
        except Exception as e:
            print(f"❌ Erreur lecture de {file.name} : {e}")
    return style

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = CustomSplash()
    splash.show()
    app.processEvents()

    # === Étape 1 : Chargement NLP (ex : spaCy)
    print(">>> Début du chargement de spaCy")
    splash.set_progress(10, "Chargement de spaCy (import)...")
    app.processEvents()

    import importlib
    spacy = importlib.import_module("spacy")
    print(">>> Import spaCy terminé")

    splash.set_progress(30, "Chargement du modèle NLP...")
    app.processEvents()
    nlp = spacy.load("fr_core_news_md")
    print(">>> Modèle spaCy chargé")

    splash.set_progress(50, "Modèle NLP chargé.")
    app.processEvents()

    # === Étape 2 : Charger les styles QSS ===
    style_dir = Path(__file__).parent / "styles"
    style = load_all_qss_from_dir(style_dir, splash=splash, app=app)
    if style:
        app.setStyleSheet(style)
        splash.set_progress(90, "Style appliqué.")
    else:
        splash.set_progress(90, "Aucun style trouvé.")
    app.processEvents()

    # === Étape 3 : Lancer la fenêtre principale ===
    splash.set_progress(100, "Initialisation de l'interface...")
    app.processEvents()
    QTimer.singleShot(300, splash.close)  # léger délai pour fluidité visuelle

    window = HomeView()
    window.show()

    sys.exit(app.exec())
