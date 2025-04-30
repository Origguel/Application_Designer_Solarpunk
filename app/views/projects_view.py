import os
import json
from datetime import datetime
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QStackedLayout


# Components
from app.components.dropdowns.dropdown_default import Dropdown_Default
from app.components.dropdowns.dropdown_legende import Dropdown_Legende


class ProjectsView(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        list_projets = self.list_projets()
        self.dropdown_projet = Dropdown_Legende(x=400, style="Dropdown_Default", items=list_projets, legende=["légende du 1", "légende du 2"], parent=self)
        self.dropdown_projet.move(34, 26)
        self.dropdown_projet.raise_()

        list_projets = self.list_projets()
        self.dropdown_projet = Dropdown_Default(x=400, style="Dropdown_Default", items=["Pas de filtre", "Date de création croissant", "Date de création décroissant", "Type de design"], parent=self)
        self.dropdown_projet.move(440, 26)
        self.dropdown_projet.raise_()

    def list_projets(self):
        projets_dir = os.path.join("data", "projets")
        projets = []

        if os.path.exists(projets_dir):
            for filename in os.listdir(projets_dir):
                if filename.endswith(".json"):
                    try:
                        with open(os.path.join(projets_dir, filename), "r", encoding="utf-8") as f:
                            data = json.load(f)
                            nom = data.get("nom", filename)
                            date_str = data.get("date_création", "01/01/1970")
                            # Convertir la date en objet datetime
                            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                            projets.append((date_obj, nom))
                    except Exception as e:
                        print(f"Erreur lecture projet {filename}: {e}")

            # Trier du plus récent au plus ancien
            projets.sort(reverse=True, key=lambda x: x[0])
            # Ne garder que le nom
            projets = [nom for _, nom in projets]

        return projets if projets else ["Aucun projet trouvé"]
