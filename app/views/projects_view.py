import os
import json
from datetime import datetime
from PySide6.QtWidgets import QWidget, QVBoxLayout
from app.components.dropdowns.dropdown_default import Dropdown_Default
from app.components.dropdowns.dropdown_legende import Dropdown_Legende


class ProjectsView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Stocke les projets complets
        self.projets_data = self.load_projets()

        # Création des dropdowns
        self.dropdown_projet = Dropdown_Legende(x=400, style="Dropdown_Default", items=[], legende=[], parent=self)
        self.dropdown_projet.move(34, 26)
        self.dropdown_projet.raise_()

        self.dropdown_filtre = Dropdown_Default(x=400, style="Dropdown_Default",
                                                items=["Pas de filtre", "Date de création croissant", "Date de création décroissant", "Type de design"],
                                                parent=self)
        self.dropdown_filtre.move(440, 26)
        self.dropdown_filtre.raise_()
        self.dropdown_filtre.currentIndexChanged.connect(self.mettre_a_jour_dropdown_projet)

        # Initialisation
        self.mettre_a_jour_dropdown_projet()

    def load_projets(self):
        projets_dir = os.path.join("data", "projets")
        projets = []

        if os.path.exists(projets_dir):
            for filename in os.listdir(projets_dir):
                if filename.endswith(".json"):
                    try:
                        with open(os.path.join(projets_dir, filename), "r", encoding="utf-8") as f:
                            data = json.load(f)
                            projets.append(data)
                    except Exception as e:
                        print(f"Erreur lecture projet {filename}: {e}")
        return projets

    def mettre_a_jour_dropdown_projet(self):
        filtre = self.dropdown_filtre.currentText()
        projets = self.projets_data

        if filtre == "Date de création croissant":
            projets = sorted(projets, key=lambda p: datetime.strptime(p.get("date_création", "01/01/1970"), "%d/%m/%Y"))
            items = [p["nom"] for p in projets]
            legendes = [p.get("date_création", "") for p in projets]

        elif filtre == "Date de création décroissant":
            projets = sorted(projets, key=lambda p: datetime.strptime(p.get("date_création", "01/01/1970"), "%d/%m/%Y"), reverse=True)
            items = [p["nom"] for p in projets]
            legendes = [p.get("date_création", "") for p in projets]

        elif filtre == "Type de design":
            projets = sorted(projets, key=lambda p: (p.get("type_design", ""), p.get("nom", "")))
            items = [p["nom"] for p in projets]
            legendes = [p.get("type_design", "") for p in projets]

        else:  # Pas de filtre
            items = [p["nom"] for p in projets]
            legendes = [""] * len(items)

        # Mise à jour de la dropdown
        self.dropdown_projet.clear()
        for nom, legende in zip(items, legendes):
            label = f"{nom:<30} | {legende}"
            self.dropdown_projet.addItem(label, userData={"left": nom, "right": legende})
