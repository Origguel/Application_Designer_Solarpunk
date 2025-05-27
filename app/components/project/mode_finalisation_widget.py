from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from pathlib import Path
import json

from app.components.inputs.input_multiline import Input_Multiline
from app.components.labels.label_default import LabelDefault

class Mode_Finalisation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.project_id = None

        # Timers pour chaque champ
        self.save_timers = {
            "moyens_actions": QTimer(self),
            "resultantes": QTimer(self),
            "abstract": QTimer(self)
        }

        for timer in self.save_timers.values():
            timer.setSingleShot(True)

        # 🔹 Bloc 1
        self.moyendaction_label = LabelDefault(text="Moyens d’action", style="H2_WB", x=384)
        self.moyendaction_input = Input_Multiline(
            object_name="Input_Multiline_Prisedenote",
            placeholder="Quelles ont été les choix et décision importante pour ce projet ?",
            x=384, y=True
        )
        self.moyendaction_input.textChanged.connect(lambda: self.on_text_changed("moyens_actions"))
        self.moyendaction_widget = QWidget(self)
        self.moyendaction_layout = QVBoxLayout(self.moyendaction_widget)
        self.moyendaction_layout.setContentsMargins(0, 0, 0, 0)
        self.moyendaction_layout.setSpacing(6)
        self.moyendaction_layout.addWidget(self.moyendaction_label)
        self.moyendaction_layout.addWidget(self.moyendaction_input)
        self.moyendaction_layout.addStretch()

        # 🔹 Bloc 2
        self.resultante_label = LabelDefault(text="Résultantes", style="H2_WB", x=384)
        self.resultante_input = Input_Multiline(
            object_name="Input_Multiline_Prisedenote",
            placeholder="Quelles en ont été les répercussions ?",
            x=384, y=True
        )
        self.resultante_input.textChanged.connect(lambda: self.on_text_changed("resultantes"))
        self.resultante_widget = QWidget(self)
        self.resultante_layout = QVBoxLayout(self.resultante_widget)
        self.resultante_layout.setContentsMargins(0, 0, 0, 0)
        self.resultante_layout.setSpacing(6)
        self.resultante_layout.addWidget(self.resultante_label)
        self.resultante_layout.addWidget(self.resultante_input)
        self.resultante_layout.addStretch()

        # 🔹 Bloc 3
        self.abstract_label = LabelDefault(text="Abstract", style="H2_WB", x=384)
        self.abstract_input = Input_Multiline(
            object_name="Input_Multiline_Prisedenote",
            placeholder="Raconte ton expérience dans ce projet, n’hésite pas à te conseiller pour de futurs projets",
            x=384, y=True
        )
        self.abstract_input.textChanged.connect(lambda: self.on_text_changed("abstract"))
        self.abstract_widget = QWidget(self)
        self.abstract_layout = QVBoxLayout(self.abstract_widget)
        self.abstract_layout.setContentsMargins(0, 0, 0, 0)
        self.abstract_layout.setSpacing(6)
        self.abstract_layout.addWidget(self.abstract_label)
        self.abstract_layout.addWidget(self.abstract_input)
        self.abstract_layout.addStretch()

        # 🔹 Layout principal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        layout.addWidget(self.moyendaction_widget)
        layout.addWidget(self.resultante_widget)
        layout.addWidget(self.abstract_widget)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def on_text_changed(self, field_name):
        print(f"✏️ Modification détectée pour {field_name}")
        self.save_timers[field_name].start(500)
        self.save_timers[field_name].timeout.connect(lambda: self.save_data(field_name))

    def load_data(self):
        selected_path = Path("assets/project/project_selected.json")
        if not selected_path.exists():
            print("❌ Fichier project_selected.json introuvable")
            return

        try:
            with open(selected_path, "r", encoding="utf-8") as f:
                selected = json.load(f)
                self.project_id = selected.get("project_id_selected")
        except Exception as e:
            print(f"❌ Erreur lecture project_selected.json : {e}")
            return

        if not self.project_id:
            print("❌ Aucun projet sélectionné.")
            return

        project_path = Path(f"data/projets/{self.project_id}.json")
        if not project_path.exists():
            print("❌ Projet introuvable :", project_path)
            return

        try:
            with open(project_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            def clean_and_update(field, input_widget):
                raw = data.get(field, "")
                cleaned = raw.rstrip()
                if cleaned.strip() == "":
                    cleaned = ""
                    print(f"🔧 Champ {field} vidé")
                else:
                    if cleaned != raw:
                        print(f"🔧 Champ {field} nettoyé")
                    cleaned += "\n"
                    print(f"➕ Nouvelle ligne ajoutée au champ {field}")

                input_widget.setText(cleaned)
                data[field] = cleaned

            clean_and_update("moyens_actions", self.moyendaction_input)
            clean_and_update("resultantes", self.resultante_input)
            clean_and_update("abstract", self.abstract_input)

            with open(project_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                print("🧼 Champs finalisation nettoyés et sauvegardés une seule fois.")

        except Exception as e:
            print(f"❌ Erreur chargement projet : {e}")

    def save_data(self, field_name):
        if not self.project_id:
            return

        project_path = Path(f"data/projets/{self.project_id}.json")
        if not project_path.exists():
            return

        try:
            with open(project_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            value = {
                "moyens_actions": self.moyendaction_input.toPlainText(),
                "resultantes": self.resultante_input.toPlainText(),
                "abstract": self.abstract_input.toPlainText()
            }.get(field_name, "")

            data[field_name] = value

            with open(project_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"✅ Sauvegarde automatique de {field_name}")

        except Exception as e:
            print(f"❌ Erreur sauvegarde {field_name} : {e}")
