from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QTimer
from pathlib import Path
import json

from app.components.inputs.input_multiline import Input_Multiline

class Mode_Prisedenote(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.project_id = None
        self.save_timer = QTimer(self)
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.save_data)

        self.prisedenote_input = Input_Multiline(
            object_name="Input_Multiline_Prisedenote",
            placeholder="Prise de note",
            x=384,
            y=True
        )

        try:
            self.prisedenote_input.textChanged.connect(self.on_text_changed)
            print("✅ Connexion à textChanged réussie")
        except Exception as e:
            print(f"❌ Signal textChanged non supporté : {e}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.prisedenote_input)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def on_text_changed(self):
        print("✏️ Texte modifié → sauvegarde dans 500ms")
        self.save_timer.start(500)  # attend 500 ms avant de sauvegarder

    def load_data(self):
        print("🧪 load_data() appelé")
        selected_path = Path("assets/project/project_selected.json")
        if not selected_path.exists():
            print("❌ Fichier project_selected.json manquant.")
            return

        try:
            with open(selected_path, "r", encoding="utf-8") as f:
                selected_data = json.load(f)
                self.project_id = selected_data.get("project_id_selected", None)
                print(f"🔍 ID du projet sélectionné : {self.project_id}")
        except Exception as e:
            print(f"❌ Erreur lecture project_selected.json : {e}")
            return

        if not self.project_id:
            print("❌ Aucun ID de projet sélectionné.")
            return

        project_path = Path(f"data/projets/{self.project_id}.json")
        print(f"📄 Chargement du fichier : {project_path}")
        print(f"📄 Existe ? {project_path.exists()}")

        if not project_path.exists():
            print(f"❌ Projet introuvable : {project_path}")
            return

        try:
            with open(project_path, "r", encoding="utf-8") as f:
                project_data = json.load(f)
                text = project_data.get("prise_de_note", "")
                print(f"📥 Texte récupéré : {text}")
                self.prisedenote_input.setText(text)

        except Exception as e:
            print(f"❌ Erreur lecture projet : {e}")


    def save_data(self):
        if not self.project_id:
            return

        project_path = Path(f"data/projets/{self.project_id}.json")
        if not project_path.exists():
            return

        try:
            with open(project_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            data["prise_de_note"] = self.prisedenote_input.toPlainText()

            with open(project_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print("✅ Donnée enregistrée.")

        except Exception as e:
            print(f"❌ Erreur sauvegarde projet : {e}")
