from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel
from PySide6.QtCore import Qt, QPointF, Signal, QObject, QTimer
import json
from pathlib import Path



# Components
from .project_ui import Project_UI
from .project_title import Project_Title

from .mode_prisedenote_widget import Mode_Prisedenote
from .mode_photo_widget import Mode_Photo
from .mode_finalisation_widget import Mode_Finalisation

from app.components.buttons.button_text import ButtonText
from app.utils.animations.project_ui_animation import (play_enter_exit_sequence, get_leave_animation, get_enter_animation)
from app.utils.animations.project_mode_animation import (animate_mode_leave, animate_mode_enter, animate_container_resize)




class ProjectsPageWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.prisedenote_visible = False
        self.photo_visible = False
        self.notation_visible = False
        self.finalisation_visible = False
        self.project_list_visible = False
        self.add_project_visible = False

        Project_UI(self)
        
        self.title_widget = Project_Title(self)
        self.title_widget.show()

        self.mode_prisedenote_widget = Mode_Prisedenote(self)
        self.mode_photo_widget = Mode_Photo(self)
        self.mode_finalisation_widget = Mode_Finalisation(self)

        self.mode_prisedenote_widget.hide()
        self.mode_photo_widget.hide()
        self.mode_finalisation_widget.hide()
        

        # 🧱 Conteneur indépendant pour le bloc "project"
        self.project_container = QWidget(self)
        self.project_container.setObjectName("ProjectContainer")
        self.project_layout = QVBoxLayout(self.project_container)
        self.project_layout.setContentsMargins(0, 0, 0, 0)
        self.project_layout.setSpacing(12)
        self.project_layout.addWidget(self.title_widget)
        self.project_layout.addWidget(self.mode_prisedenote_widget)
        self.project_layout.addWidget(self.mode_photo_widget)
        self.project_layout.addWidget(self.mode_finalisation_widget)
        self.project_layout.addStretch()

        self.mode_prisedenote_widget.load_data()
        self.mode_finalisation_widget.load_data()
        self.toggle_mode("prisedenote")

    # ──────────────────────────────────────────────
    # ▶ Événements Qt
    # ──────────────────────────────────────────────

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.leftbar.move(16, 16)
        self.project_list.move(54, 16)
        self.project_list.setFixedWidth(370)
        self.update_project_container_size()



    # ──────────────────────────────────────────────
    # ▶ Contrôle des modes de visualisation
    # ──────────────────────────────────────────────

    def toggle_mode(self, mode_name: str):
        mode_widgets = {
            "prisedenote": self.mode_prisedenote_widget,
            "photo": self.mode_photo_widget,
            "finalisation": self.mode_finalisation_widget
        }

        incoming = mode_widgets.get(mode_name)
        if not incoming:
            print(f"❌ Mode inconnu : {mode_name}")
            return

        outgoing = next((w for w in mode_widgets.values() if w and w.isVisible()), None)

        self.update_mode_flags(mode_name)

        if mode_name == "photo":
            self.mode_photo_widget.load_photos()

        mode_target_sizes = {
            "prisedenote": 384,
            "photo": 1184,
            "finalisation": 1184
        }
        target_width = mode_target_sizes.get(mode_name, 427)
        target_height = self.height() - 72 - 16

        if not outgoing:
            print("⚠️ Aucun widget visible actuellement")
            incoming.show()
            self.update_project_container_size()  # ✅ uniquement ici
            return

        def after_leave():
            outgoing.hide()
            self.animation = animate_container_resize(
                container=self.project_container,
                target_width=target_width,
                target_height=target_height,
                callback=lambda: self.start_enter_animation(incoming)
            )

        self.animation = animate_mode_leave(
            widget_out=outgoing,
            container_width=self.project_container.width(),
            callback=after_leave
        )


    def update_mode_flags(self, mode_name: str):
        self.prisedenote_visible = (mode_name == "prisedenote")
        self.photo_visible       = (mode_name == "photo")
        self.notation_visible    = (mode_name == "notation")
        self.finalisation_visible= (mode_name == "finalisation")

        # Mise à jour visuelle des boutons
        button_map = {
            "prisedenote": self.prisedenote_button,
            "photo": self.photo_button,
            "notation": self.notation_button,
            "finalisation": self.finalisation_button,
        }

        for name, button in button_map.items():
            style = "Button_Default_Selected" if name == mode_name else "Button_Default"
            button.setObjectName(style)
            button.update_icon()

        self.refresh_note_mode_button()





    def start_enter_animation(self, widget_in):
        for w in [self.mode_prisedenote_widget, self.mode_photo_widget, self.mode_finalisation_widget]:
            if w != widget_in:
                w.hide()


        widget_in.move(self.project_container.width(), widget_in.y())
        widget_in.raise_()
        widget_in.show()

        self.animation = animate_mode_enter(
            widget_in,
            self.project_container
        )



    def refresh_note_mode_button(self):
        buttons = [
            self.prisedenote_button,
            self.photo_button,
            self.notation_button,
            self.finalisation_button
        ]

        for btn in buttons:
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    def update_project_container_size(self):
        container_size_y = self.height() - 72 - 16

        if self.prisedenote_visible:
            container_size_x = 427
        elif self.photo_visible:
            container_size_x = 1184
        elif self.finalisation_visible:
            container_size_x = 1184
        else:
            container_size_x = 1184

        move_x = self.width() - container_size_x - 16
        move_y = 72

        self.project_container.move(move_x, move_y)
        self.project_container.resize(container_size_x, container_size_y)





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
        self.list_button.update_icon()
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

            self.load_project_buttons()
            self.toggle_project_list()

            # MAJ des différents composants
            self.title_widget.load_selected_project()

            if hasattr(self, 'mode_prisedenote_widget'):
                self.mode_prisedenote_widget.load_data()

            if hasattr(self, 'mode_photo_widget'):
                self.mode_photo_widget.load_photos()

            if hasattr(self, 'mode_finalisation_widget'):
                self.mode_finalisation_widget.load_data()  # À faire si besoin

        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour du fichier : {e}")
