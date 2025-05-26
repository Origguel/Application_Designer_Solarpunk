from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
import json
from pathlib import Path

from app.components.labels.label_default import LabelDefault
from app.components.buttons.button_text_small import ButtonTextSmall

class Project_Title(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # -------- TITLE COMPONENTS --------
        self.title_label = LabelDefault(text="Pulp'Cycle", style="H1_WB", x=427)
        self.title_label.setStyleSheet("color: #EC831E;")
        self.client_label = LabelDefault(text="Google", style="H2_WB", x=427)
        self.date_label = LabelDefault(text="Du 6 janvier 2025 au 23 mai 2025", style="Sous_Text_WB", x=427)
        self.see_note_button = ButtonTextSmall(text="Voir les notes de Pulp’Cycle", x=173)

        self.load_selected_project()


        # CLIENT DATE
        client_date_widget = QWidget()
        client_date_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        client_date_widget_layout = QVBoxLayout(client_date_widget)
        client_date_widget_layout.setContentsMargins(0, 0, 0, 0)
        client_date_widget_layout.setSpacing(2)
        client_date_widget_layout.addWidget(self.client_label)
        client_date_widget_layout.addWidget(self.date_label)

        # -------- ASSEMBLAGE --------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.addWidget(self.title_label)
        layout.addWidget(client_date_widget)
        layout.addWidget(self.see_note_button)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)


    def load_selected_project(self):
        try:
            selection_path = Path("assets/project/project_selected.json")
            if not selection_path.exists():
                print("❌ Aucun projet sélectionné.")
                return

            with open(selection_path, "r", encoding="utf-8") as f:
                selected = json.load(f)
                project_id = selected.get("project_id_selected")

            if not project_id:
                print("❌ Clé 'project_id_selected' absente.")
                return

            project_path = Path(f"data/projets/{project_id}.json")
            if not project_path.exists():
                print(f"❌ Projet introuvable : {project_path}")
                return

            with open(project_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # ⬇️ Mise à jour des champs du widget
            self.title_label.setText(data.get("nom", "Projet inconnu"))
            self.client_label.setText(data.get("commanditaire", "Commanditaire inconnu"))
            self.date_label.setText(f"Du {data.get('date_debut', '')} au {data.get('date_fin', '')}")

        except Exception as e:
            print(f"❌ Erreur lors du chargement du projet sélectionné : {e}")
