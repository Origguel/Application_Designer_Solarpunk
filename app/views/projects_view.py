import os
import json
from datetime import datetime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
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

        # Dropdowns
        self.dropdown_projet = Dropdown_Legende(x=400, style="Dropdown_Default", items=[], legende=[], parent=self)
        self.dropdown_projet.move(34, 26)
        self.dropdown_projet.raise_()
        self.dropdown_projet.currentIndexChanged.connect(self.afficher_infos_projet)

        self.dropdown_filtre = Dropdown_Default(x=250, style="Dropdown_Default",
                                                items=["Pas de filtre", "Date de création croissant", "Date de création décroissant", "Type de design"],
                                                parent=self)
        self.dropdown_filtre.move(440, 26)
        self.dropdown_filtre.raise_()
        self.dropdown_filtre.currentIndexChanged.connect(self.mettre_a_jour_dropdown_projet)

        # Labels pour les infos du projet
        self.nom_projet = QLabel()
        self.nom_projet.setObjectName("Nom_Projet")

        self.date_debut_projet = QLabel()
        self.date_debut_projet.setObjectName("Date_Debut_Projet")

        self.date_fin_projet = QLabel()
        self.date_fin_projet.setObjectName("Date_Fin_Projet")

        self.commanditaire_projet = QLabel()
        self.commanditaire_projet.setObjectName("Commanditaire_Projet")

        self.type_projet = QLabel()
        self.type_projet.setObjectName("Type_Projet")

        self.prise_de_note_projet = QLabel()
        self.prise_de_note_projet.setObjectName("Prise_De_Note_Projet")


        # Groupe contenant les labels
        self.labels_group = QWidget(self)
        self.labels_group.move(34, 124)
        self.labels_group.setFixedSize(800, 150)

        self.labels_layout = QVBoxLayout(self.labels_group)
        self.labels_layout.setContentsMargins(0, 0, 0, 0)
        self.labels_layout.setSpacing(6)

        self.labels_layout.addWidget(self.nom_projet)
        self.labels_layout.addWidget(self.date_debut_projet)
        self.labels_layout.addWidget(self.date_fin_projet)
        self.labels_layout.addWidget(self.commanditaire_projet)
        self.labels_layout.addWidget(self.type_projet)
        self.labels_layout.addWidget(self.prise_de_note_projet)

        

        # Initialisation dropdown projet
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

        else:
            items = [p["nom"] for p in projets]
            legendes = [""] * len(items)

        # Met à jour les données
        self.projets_data = projets

        # Sauvegarder le nom du projet sélectionné
        selected_data = self.dropdown_projet.get_current_data()
        selected_nom = selected_data["left"] if selected_data else None

        # Recharge la dropdown
        self.dropdown_projet.blockSignals(True)
        self.dropdown_projet.clear()
        for nom, legende in zip(items, legendes):
            self.dropdown_projet.addItem("", {"left": nom, "right": legende})
        self.dropdown_projet.blockSignals(False)

        # Rétablir la sélection si possible
        index_to_select = 0
        for i in range(self.dropdown_projet.count()):
            data = self.dropdown_projet.itemData(i)
            if data and data.get("left") == selected_nom:
                index_to_select = i
                break

        self.dropdown_projet.setCurrentIndex(index_to_select)
        self.afficher_infos_projet()


    def afficher_infos_projet(self):
        index = self.dropdown_projet.currentIndex()
        if index < 0 or index >= len(self.projets_data):
            return

        projet = self.projets_data[index]

        self.nom_projet.setText(f"{projet.get('nom', 'N/A')}")
        self.date_debut_projet.setText(f"{projet.get('date_debut', 'N/A')}")
        self.date_fin_projet.setText(f"{projet.get('date_fin', 'N/A')}")
        self.commanditaire_projet.setText(f"{projet.get('commanditaire', 'N/A')}")
        self.type_projet.setText(f"{projet.get('type_design', 'N/A')}")
        self.prise_de_note_projet.setText(f"{projet.get('prise_de_note', '')}")
