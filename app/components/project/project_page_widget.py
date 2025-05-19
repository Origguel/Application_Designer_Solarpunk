from PySide6.QtWidgets import QWidget, QFrame, QLabel
from PySide6.QtCore import Qt, QPointF, Signal, QObject, QTimer
import json
from pathlib import Path



# Components
from .project_ui import Project_UI
from .prise_de_note import PriseDeNote



class ProjectsPageWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.prisedenote_visible = True
        self.photo_visible = False
        self.notation_visible = False
        self.finalisation_visible = False
        self.project_list_visible = False
        self.add_project_visible = False

        Project_UI(self)               # initialise les boutons, etc.
        self.init_prisedenote()       # crée prisedenote_widget proprement

        

        self.toggle_prisedenote()

    # ──────────────────────────────────────────────
    # ▶ Événements Qt
    # ──────────────────────────────────────────────

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.leftbar.move(16, 16)
        self.project_list.move(54, 16)

        if hasattr(self, 'prisedenote_widget') and self.prisedenote_widget:
            x = int(self.width() * 0.865)
            y = int(self.height() - 105 - 16)

            # Calcul du décalage si la project_list est visible
            move_x = int(self.width() - x - 16)

            self.prisedenote_widget.move(move_x, 105)
            self.prisedenote_widget.resize(x, y)

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
            self.project_list.raise_()
        else:
            self.prisedenote_widget.raise_()
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

    def init_prisedenote(self):
        self.prisedenote_widget = PriseDeNote(self)
        self.prisedenote_widget.raise_()
        self.prisedenote_widget.show()
