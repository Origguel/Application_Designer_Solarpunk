from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
import json
from pathlib import Path

from app.components.labels.label_default import LabelDefault
from app.components.buttons.button_text import ButtonText
from app.components.inputs.input_multiline import Input_Multiline

class PriseDeNote(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)  # ✅ 1 seul layout principal
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # -------- TOP LAYOUT --------
        self.title_label = LabelDefault(text="Pulp'Cycle", style="H1_WB")
        self.client_label = LabelDefault(text="Google", style="H2_WB", x=None)
        self.client_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.date_label = LabelDefault(text="Du 6 janvier 2025 au 23 mai 2025", style="Sous_Text_WB", x=256)
        self.date_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.see_note_button = ButtonText(text="Voir les notes de Pulp’Cycle", x=173)

        client_date_widget = QWidget()
        client_date_total_width = (self.client_label.sizeHint().width() + 12 + self.date_label.sizeHint().width())
        client_date_widget.setFixedWidth(client_date_total_width)
        client_date_widget_layout = QHBoxLayout(client_date_widget)
        client_date_widget_layout.setContentsMargins(0, 0, 0, 0)
        client_date_widget_layout.addWidget(self.client_label)
        client_date_widget_layout.addSpacing(12)
        client_date_widget_layout.addWidget(self.date_label)

        top_widget_left = QWidget()
        top_widget_left_layout = QVBoxLayout(top_widget_left)
        top_widget_left_layout.setContentsMargins(0, 0, 0, 0)
        top_widget_left_layout.setSpacing(6)
        top_widget_left_layout.addWidget(self.title_label)
        top_widget_left_layout.addWidget(client_date_widget)

        top_widget = QWidget()
        top_widget.setFixedHeight(50)
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(6)
        top_layout.addWidget(top_widget_left, alignment=Qt.AlignBottom)
        top_layout.addWidget(self.see_note_button , alignment=Qt.AlignBottom)

        # -------- BOTTOM LAYOUT --------
        self.prisedenote_input = Input_Multiline(object_name="Input_Multiline_Prisedenote", placeholder="Prise de note", x=True, y=True)
        bottom_widget = QWidget()
        bottom_widget.setObjectName("PriseDeNote")
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(self.prisedenote_input)

        # -------- ASSEMBLAGE --------
        layout.addWidget(top_widget)
        layout.addWidget(bottom_widget)
        
        self.load_selected_project()


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
            self.prisedenote_input.setText(data.get("prise_de_note", ""))

        except Exception as e:
            print(f"❌ Erreur lors du chargement du projet sélectionné : {e}")
