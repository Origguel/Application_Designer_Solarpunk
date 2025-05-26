from PySide6.QtWidgets import QWidget, QFrame, QLabel
from PySide6.QtCore import Qt, QPointF, Signal, QObject, QTimer, QPoint, QSize
import json
from pathlib import Path

from app.components.note.notes_ui import setup_ui
from app.components.note.notes_search_handler import (
    on_search_note,
    clear_search_highlights
)
from app.components.note.modes.cluster.cluster_camera_animation import animate_camera_to_center
from app.components.note.modes.cluster_mode_widget import ClusterModeWidget
from app.components.note.modes.timeline_mode_widget import TimelineModeWidget
from app.components.note.modes.theme_mode_widget import ThemeModeWidget
from app.utils.categorie_manager.category_manager import CategoryManager
from app.components.note.delete_note_handler import confirm_and_delete_note
from app.utils.categorie_manager.category_tree_updater import CategoryTreeUpdater
from app.components.note.note_detail_widget import NoteDetailWidget
from app.components.note.note_creator import NoteCreator
from app.utils.note_selection_manager import set_selected_note_id, get_selected_note_id
from app.utils.animations.note_ui_animation import play_toolbar_animation


class NotesPageWidget(QWidget):
    # ──────────────────────────────────────────────
    # ▶ Signaux Qt
    # ──────────────────────────────────────────────
    note_created = Signal(str, list)
    cancelled = Signal()

    # ──────────────────────────────────────────────
    # ▶ Initialisation
    # ──────────────────────────────────────────────
    def __init__(self):
        super().__init__()

        self.searchbar_visible = False
        self.addnote_visible = False
        self.cluster_visible = True
        self.timeline_visible = False
        self.theme_visible = False
        self.is_camera_animating = False

        self.reset_view_timer = QTimer()
        self.reset_view_timer.setSingleShot(True)
        self.reset_view_timer.timeout.connect(self.reset_reset_button_style)

        self.visualization_container = QFrame(self)
        self.visualization_container.setGeometry(0, 0, self.width(), self.height())
        self.visualization_container.lower()

        self.note_created.connect(self.add_note_visually)

        self.graph_widget = ClusterModeWidget(self, self.visualization_container)

        setup_ui(self, note_id="note_0001")

        self.visualization_widgets = {
            "cluster": self.graph_widget,
            "timeline": TimelineModeWidget(self.visualization_container),
            "theme": ThemeModeWidget(self.visualization_container)
        }

        self.current_mode = "cluster"
        self.switch_note_mode("cluster")
        self.toggle_cluster()

    # ──────────────────────────────────────────────
    # ▶ Événements Qt
    # ──────────────────────────────────────────────
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.graph_widget.setGeometry(0, 0, self.width(), self.height())
        self.visualization_container.setGeometry(0, 0, self.width(), self.height())
        for widget in self.visualization_widgets.values():
            if widget:
                widget.setGeometry(0, 0, self.width(), self.height())

        self.searchbar_widget.move(54, 16)
        self.leftbar.move(16, 16)
        self.addnote.move(54, 54)

        self.leftbar.raise_()
        self.searchbar_widget.raise_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            clear_search_highlights(self)
            self.on_reset_view_button_clicked()
            print("🧹 Vue réinitialisée via Escape.")
        elif event.key() == Qt.Key_R:
            self.on_reset_view_button_clicked()
            print("🔄 Vue recentrée via touche R.")
            

    # ──────────────────────────────────────────────
    # ▶ Liaison des handlers globaux
    # ──────────────────────────────────────────────
    on_search_note = on_search_note
    clear_search_highlights = clear_search_highlights
    animate_camera_to_center = animate_camera_to_center

    # ──────────────────────────────────────────────
    # ▶ Contrôle des modes de visualisation
    # ──────────────────────────────────────────────
    def switch_note_mode(self, mode):
        if mode not in self.visualization_widgets:
            print(f"❌ Mode inconnu : {mode}")
            return
        for widget in self.visualization_widgets.values():
            if widget:
                widget.hide()
        self.visualization_widgets[mode].show()
        self.current_mode = mode
        print(f"🔁 Mode actif : {mode}")

    def toggle_cluster(self):
        self.cluster_visible = True
        self.timeline_visible = False
        self.theme_visible = False
        self.switch_note_mode("cluster")
        self.cluster_button.setObjectName("Button_Default_Selected")
        self.timeline_button.setObjectName("Button_Default")
        self.theme_button.setObjectName("Button_Default")
        self.cluster_button.update_icon()
        self.timeline_button.update_icon()
        self.theme_button.update_icon()
        self.refresh_note_mode_button()

    def toggle_timeline(self):
        self.cluster_visible = False
        self.timeline_visible = True
        self.theme_visible = False
        self.switch_note_mode("timeline")
        self.cluster_button.setObjectName("Button_Default")
        self.timeline_button.setObjectName("Button_Default_Selected")
        self.theme_button.setObjectName("Button_Default")
        self.cluster_button.update_icon()
        self.timeline_button.update_icon()
        self.theme_button.update_icon()
        self.refresh_note_mode_button()

    def toggle_theme(self):
        self.cluster_visible = False
        self.timeline_visible = False
        self.theme_visible = True
        self.switch_note_mode("theme")
        self.cluster_button.setObjectName("Button_Default")
        self.timeline_button.setObjectName("Button_Default")
        self.theme_button.setObjectName("Button_Default_Selected")
        self.cluster_button.update_icon()
        self.timeline_button.update_icon()
        self.theme_button.update_icon()
        self.refresh_note_mode_button()

    def refresh_note_mode_button(self):
        for btn in [self.cluster_button, self.timeline_button, self.theme_button]:
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    def on_reset_view_button_clicked(self):
        if self.is_camera_animating:
            print("⏳ Animation déjà en cours.")
            return

        current_widget = self.visualization_widgets.get(self.current_mode)
        if hasattr(current_widget, "reset_view"):
            current_widget.reset_view()
            print(f"🔄 Vue recentrée pour le mode {self.current_mode}.")
        else:
            print(f"❌ Le mode {self.current_mode} ne supporte pas encore la réinitialisation.")

        # ✅ Changer le style du bouton temporairement
        self.resetview_button.setObjectName("Button_Default_Selected")
        self.resetview_button.style().unpolish(self.resetview_button)
        self.resetview_button.style().polish(self.resetview_button)
        self.resetview_button.update_icon()
        self.resetview_button.update()

        # ✅ Lancer le timer pour revenir au style normal après 2 secondes
        self.reset_view_timer.start(2500)

    def reset_reset_button_style(self):
        self.resetview_button.setObjectName("Button_Default")
        self.resetview_button.style().unpolish(self.resetview_button)
        self.resetview_button.style().polish(self.resetview_button)
        self.resetview_button.update_icon()
        self.resetview_button.update()



    # ──────────────────────────────────────────────
    # ▶ Recherche & Ajout de notes
    # ──────────────────────────────────────────────
    def toggle_search_input(self):
        self.searchbar_visible = not self.searchbar_visible
        self.animation = play_toolbar_animation(self.searchbar_widget, self.searchbar_visible)
        self.search_button.setObjectName("Button_Default_Selected" if self.searchbar_visible else "Button_Default")
        self.search_button.style().unpolish(self.search_button)
        self.search_button.style().polish(self.search_button)
        self.search_button.update_icon()
        self.search_button.update()

    def toggle_addnote_input(self):
        self.addnote_visible = not self.addnote_visible

        self.animation = play_toolbar_animation(
            widget=self.addnote,
            visible=self.addnote_visible,
            target_pos=QPoint(54, 54),
            target_size=QSize(370, 350)  # taille finale de ton addnote widget
        )

        self.plus_button.setObjectName("Button_Default_Selected" if self.addnote_visible else "Button_Default")
        self.plus_button.style().unpolish(self.plus_button)
        self.plus_button.style().polish(self.plus_button)
        self.plus_button.update_icon()
        self.plus_button.update()


    def validate_and_save_note(self):
        title = self.title_input.text().strip()
        date = self.date_input.text().strip()
        project = self.project_selector.currentText().strip()
        description = self.description_input.toPlainText().strip()
        contenu = self.contenu_input.toPlainText().strip()
        type_note = self.selected_note_type

        if not title or not date or not project or not description or not type_note or not contenu:
            print("❗ Tous les champs obligatoires ne sont pas remplis.")
            return

        note_data = NoteCreator.create_note(
            title=title,
            date_str=date,
            note_type=type_note,
            project=project,
            description=description,
            contenu=contenu
        )

        self.clear_fields()
        self.note_created.emit(note_data["id"], note_data["keywords"])
        self.cancelled.emit()
        print("Note created")

    def add_note_visually(self, note_id, keywords):
        updater = CategoryTreeUpdater()
        updater.add_note(note_id, keywords)
        self.graph_widget.add_note_live(note_id, keywords)
        print(f"✨ Note ajoutée visuellement dans le graphe : {note_id}")

    def clear_fields(self):
        self.title_input.clear()
        self.description_input.clear()
        self.contenu_input.clear()

    # ──────────────────────────────────────────────
    # ▶ Détails & suppression
    # ──────────────────────────────────────────────
    def open_note_detail(self, note_id=None):
        if note_id is None:
            note_id = get_selected_note_id()
        if not note_id:
            print("❌ Aucune note sélectionnée (ni paramètre, ni JSON).")
            return
        note_path = Path(f"data/notes/{note_id}.json")
        if not note_path.exists():
            print(f"❌ Fichier de note introuvable : {note_path}")
            return
        with open(note_path, "r", encoding="utf-8") as f:
            note_data = json.load(f)
        self.close_note_detail()
        note_detail_x = 408
        note_detail_y = self.height() - 54 - 16
        self.note_detail_widget = NoteDetailWidget(note_data, x=note_detail_x, y=note_detail_y, parent=self)
        self.note_detail_widget.move(self.width() - note_detail_x - 16, 54)
        self.note_detail_widget.raise_()
        self.note_detail_widget.show()

    def close_note_detail(self):
        if hasattr(self, 'note_detail_widget') and self.note_detail_widget:
            self.note_detail_widget.setParent(None)
            self.note_detail_widget.deleteLater()
            self.note_detail_widget = None

    def on_delete_button_clicked(self):
        selected_note_id = self.graph_widget.get_selected_note_id()
        if selected_note_id:
            confirm_and_delete_note(self, selected_note_id)
            CategoryManager().update()
            self.graph_widget.delete_note_live(selected_note_id)
        else:
            print("❌ Aucune note sélectionnée pour suppression.")

    def set_note_type(self, note_type):
        self.selected_note_type = note_type
        print(f"📜 Type de note sélectionné : {note_type}")
        
        all_buttons = [
            self.notetype_text, self.notetype_image, self.notetype_video,
            self.notetype_doc, self.notetype_lien, self.notetype_code
        ]

        # Réinitialiser tous les boutons
        for btn in all_buttons:
            btn.setObjectName("Button_Default")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update_icon()  # 🔁 Mise à jour de l'icône après le style

        # Appliquer le style "selected" au bon bouton
        selected_button = getattr(self, f"notetype_{note_type}", None)
        if selected_button:
            selected_button.setObjectName("Button_Default_Selected")
            selected_button.style().unpolish(selected_button)
            selected_button.style().polish(selected_button)
            selected_button.update_icon()  # 🔁 Mise à jour icône sélectionnée

