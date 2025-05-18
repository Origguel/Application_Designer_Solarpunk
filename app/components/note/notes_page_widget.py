from PySide6.QtWidgets import QWidget, QFrame, QLabel
from PySide6.QtCore import Qt, QPointF

from app.components.note.notes_ui import setup_ui
from app.components.note.notes_interactions import (
    open_note_detail,
    open_add_note_widget,
    close_add_note_widget,
    add_note_visually,
    on_delete_button_clicked,
    close_note_detail
)
from app.components.note.notes_search_handler import (
    on_search_note,
    clear_search_highlights
)
from app.components.note.modes.cluster.cluster_camera_animation import animate_camera_to_center

from app.components.note.modes.cluster_mode_widget import ClusterModeWidget
from app.components.note.modes.timeline_mode_widget import TimelineModeWidget
from app.components.note.modes.theme_mode_widget import ThemeModeWidget


class NotesPageWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.is_camera_animating = False
        self.visualization_container = QFrame(self)
        self.visualization_container.setGeometry(0, 0, self.width(), self.height())
        self.visualization_container.lower()  # reste derrière les autres UI
        setup_ui(self)

        self.visualization_widgets = {
            "cluster": self.graph_widget,  # déjà instancié par setup_ui
            "timeline": None,              # à instancier plus tard
            "theme": None                  # à instancier plus tard
        }
        self.current_mode = "cluster"

        self.visualization_widgets["cluster"] = ClusterModeWidget(self, self.visualization_container)
        self.visualization_widgets["timeline"] = TimelineModeWidget(self.visualization_container)
        self.visualization_widgets["theme"] = ThemeModeWidget(self.visualization_container)

        self.switch_note_mode("cluster")


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.graph_widget.setGeometry(0, 0, self.width(), self.height())
        self.visualization_container.setGeometry(0, 0, self.width(), self.height())
        for widget in self.visualization_widgets.values():
            if widget:
                widget.setGeometry(0, 0, self.width(), self.height())

        self.leftbar.move(16, 16)

        self.search_input.move(54, 16)
        if self.overlay.isVisible():
            self.overlay.setGeometry(0, 0, self.width(), self.height())

        if self.add_note_widget:
            self.add_note_widget.move(
                (self.width() - self.add_note_widget.width()) // 2,
                (self.height() - self.add_note_widget.height()) // 2
            )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            clear_search_highlights(self)
            self.on_reset_view_button_clicked()
            print("🧹 Vue réinitialisée via Escape.")
        elif event.key() == Qt.Key_R:
            self.on_reset_view_button_clicked()
            print("🔄 Vue recentrée via touche R.")

    # Liaison directe aux handlers
    open_note_detail = open_note_detail
    close_note_detail = close_note_detail
    open_add_note_widget = open_add_note_widget
    close_add_note_widget = close_add_note_widget
    add_note_visually = add_note_visually
    on_delete_button_clicked = on_delete_button_clicked
    on_search_note = on_search_note
    clear_search_highlights = clear_search_highlights
    animate_camera_to_center = animate_camera_to_center

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



    def switch_note_mode(self, mode):
        if mode not in self.visualization_widgets:
            print(f"❌ Mode inconnu : {mode}")
            return

        # Cacher tous les widgets de visualisation
        for widget in self.visualization_widgets.values():
            if widget:
                widget.hide()

        # Si le widget du mode n’est pas encore créé, afficher un placeholder
        if self.visualization_widgets[mode] is None:
            placeholder = QLabel(f"Mode '{mode}' en cours de développement", self.visualization_container)
            placeholder.setAlignment(Qt.AlignCenter)
            placeholder.setStyleSheet("font-size: 24px; color: grey;")
            placeholder.setGeometry(0, 0, self.width(), self.height())
            placeholder.show()
            self.visualization_widgets[mode] = placeholder
        else:
            self.visualization_widgets[mode].show()

        self.current_mode = mode
        print(f"🔁 Mode actif : {mode}")
