"""
Point d'entrée principal de ton application.
"""
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from app.views.home_view import HomeView

# === Ajouter le dossier "app" au chemin Python ===
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

# === Charger les ressources (images, icons, etc.) ===
import app.resources_rc
print("resources_rc imported successfully")

# === Fonction pour charger automatiquement tous les fichiers .qss ===
def load_all_qss_from_dir(directory: Path) -> str:
    style = ""
    if not directory.exists():
        print(f"❌ Le dossier de styles '{directory}' n'existe pas.")
        return style

    qss_files = sorted(directory.glob("*.qss"))  # Trie les fichiers par nom
    if not qss_files:
        print("⚠️ Aucun fichier QSS trouvé dans le dossier.")
        return style

    for file in qss_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                style += f"/* {file.name} */\n{content}\n\n"
        except Exception as e:
            print(f"❌ Erreur lors de la lecture de {file.name} : {e}")
    return style

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # === Charger les styles QSS depuis le dossier "styles" ===
    style_dir = Path(__file__).parent / "styles"
    style = load_all_qss_from_dir(style_dir)
    if style:
        app.setStyleSheet(style)
    else:
        print("⚠️ Aucun style appliqué, l'application s'affichera sans thème.")

    # === Lancer la fenêtre principale ===
    window = HomeView()
    window.show()

    # === Démarrer l'application ===
    sys.exit(app.exec())
