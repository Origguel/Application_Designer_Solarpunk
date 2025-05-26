from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel
from PySide6.QtCore import Qt, QPointF, Signal, QObject, QTimer
import json
from pathlib import Path



# Components
from .project_ui import Project_UI
from .project_title import Project_Title
from .prise_de_note import Prise_de_Note

from app.components.buttons.button_text import ButtonText
from app.utils.animations.project_ui_animation import (play_enter_exit_sequence, get_leave_animation, get_enter_animation)



class ProjectsPageWidget(QWidget):
    def __init__(self):
        super().__init__()

        

        self.prisedenote_visible = True
        self.photo_visible = False
        self.notation_visible = False
        self.finalisation_visible = False
        self.project_list_visible = False
        self.add_project_visible = False

        Project_UI(self)
        
        self.title_widget = Project_Title(self)
        self.prisedenote_widget = Prise_de_Note(self)
        self.title_widget.show()
        self.prisedenote_widget.show()

        # 🧱 Conteneur indépendant pour le bloc "project"
        self.project_container = QWidget(self)
        self.project_container.setObjectName("ProjectContainer")
        self.project_layout = QVBoxLayout(self.project_container)
        self.project_layout.setContentsMargins(0, 0, 0, 0)
        self.project_layout.setSpacing(12)
        self.project_layout.addWidget(self.title_widget)
        self.project_layout.addWidget(self.prisedenote_widget)
        self.project_layout.addStretch()

        self.toggle_prisedenote()

    # ──────────────────────────────────────────────
    # ▶ Événements Qt
    # ──────────────────────────────────────────────

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.leftbar.move(16, 16)
        self.project_list.move(54, 16)
        self.project_list.setFixedWidth(370)

        # Positionnement du container du bloc projet
        self.project_container.move(64, 72)
        self.project_container.resize(427, self.height() - 72 - 16)

    # ──────────────────────────────────────────────
    # ▶ Contrôle des modes de visualisation
    # ──────────────────────────────────────────────

    def toggle_prisedenote(self):
        self.prisedenote_visible = True
        self.photo_visible = False
        self.notation_visible = False
        self.finalisation_visible = False
        self.prisedenote_widget.show()
        self.prisedenote_button.setObjectName("Button_Default_Selected")
        self.photo_button.setObjectName("Button_Default")
        self.notation_button.setObjectName("Button_Default")
        self.finalisation_button.setObjectName("Button_Default")
        self.refresh_note_mode_button()
    
    def toggle_photo(self):
        self.prisedenote_visible = False
        self.photo_visible = True
        self.notation_visible = False
        self.finalisation_visible = False
        self.prisedenote_widget.hide()
        self.prisedenote_button.setObjectName("Button_Default")
        self.photo_button.setObjectName("Button_Default_Selected")
        self.notation_button.setObjectName("Button_Default")
        self.finalisation_button.setObjectName("Button_Default")
        self.refresh_note_mode_button()

    def toggle_notation(self):
        self.prisedenote_visible = False
        self.photo_visible = False
        self.notation_visible = True
        self.finalisation_visible = False
        self.prisedenote_widget.hide()
        self.prisedenote_button.setObjectName("Button_Default")
        self.photo_button.setObjectName("Button_Default")
        self.notation_button.setObjectName("Button_Default_Selected")
        self.finalisation_button.setObjectName("Button_Default")
        self.refresh_note_mode_button()

    def toggle_finalisation(self):
        self.prisedenote_visible = False
        self.photo_visible = False
        self.notation_visible = False
        self.finalisation_visible = True
        self.prisedenote_widget.hide()
        self.prisedenote_button.setObjectName("Button_Default")
        self.photo_button.setObjectName("Button_Default")
        self.notation_button.setObjectName("Button_Default")
        self.finalisation_button.setObjectName("Button_Default_Selected")
        self.refresh_note_mode_button()

    def refresh_note_mode_button(self):
        for btn in [self.prisedenote_button, self.photo_button, self.notation_button, self.finalisation_button]:
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    def toggle_project_list(self):
        self.project_list_visible = not self.project_list_visible
        self.project_list.setVisible(self.project_list_visible)
        self.project_list.setEnabled(self.project_list_visible)

        if self.project_list_visible:
            self.load_project_buttons()  # ✅ charger les projets ici
            self.project_list.raise_()
        else:
            self.title_widget.raise_()

        self.list_button.setObjectName("Button_Default_Selected" if self.project_list_visible else "Button_Default")
        self.list_button.style().unpolish(self.list_button)
        self.list_button.style().polish(self.list_button)
        self.list_button.update()



    def toggle_add_project(self):
        self.add_project_visible = True


    # ──────────────────────────────────────────────
    # ▶ Gestion de projet
    # ──────────────────────────────────────────────

    def add_project(self):
        print("add projet")

    def delete_project(self):
        print("delete projet")


    # ──────────────────────────────────────────────
    # ▶ Project List Utils
    # ──────────────────────────────────────────────

    def load_project_buttons(self):
        projets_dir = Path("data/projets/")
        selection_path = Path("assets/project/project_selected.json")
        layout = self.project_list_layout

        # 🧼 Nettoyer le layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                del item

        # 📥 Lire l'ID sélectionné actuel
        selected_id = None
        if selection_path.exists():
            try:
                with open(selection_path, "r", encoding="utf-8") as f:
                    selected_data = json.load(f)
                    selected_id = selected_data.get("project_id_selected", None)
            except Exception as e:
                print(f"❌ Erreur lecture project_selected.json : {e}")

        # 📂 Charger les projets
        json_files = sorted(projets_dir.glob("projet_*.json"))
        total_height = 0
        button_height = 32
        spacing = 0

        for index, file_path in enumerate(json_files):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    nom = data.get("nom", file_path.stem)
                    projet_id = data.get("id", file_path.stem)

                    style = "Button_Default_Left_Selected" if projet_id == selected_id else "Button_Default_Left"
                    button = ButtonText(text=nom, style=style, x=370, parent=self)
                    button.clicked.connect(lambda _, pid=projet_id: self.set_selected_project_id(pid))

                    layout.addWidget(button)
                    total_height += button_height

                    if index < len(json_files) - 1:
                        layout.addSpacing(spacing)
                        total_height += spacing

            except Exception as e:
                print(f"❌ Erreur lecture {file_path.name} : {e}")

        self.project_list.setFixedHeight(total_height)


    def set_selected_project_id(self, project_id):
        json_path = Path("assets/project/project_selected.json")

        try:
            data = {}
            if json_path.exists():
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

            data["project_id_selected"] = project_id

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"✅ Projet sélectionné : {project_id}")

            self.load_project_buttons()  # Met à jour les styles visuels
            self.toggle_project_list() # Ferme la list de note

            # ✅ Recharge dynamiquement le contenu de la prise de note
            if hasattr(self, 'prisedenote_widget'):
                self.animation = play_enter_exit_sequence(
                    self.title_widget,
                    self.width(),
                    self.title_widget.load_selected_project
                )



        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour du fichier : {e}")


