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

        # UI Variable
        self.searchbar_visible = False
        self.addnote_visible = False
        self.cluster_visible = True
        self.timeline_visible = False
        self.theme_visible = False
        
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
        self.toggle_cluster()


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.graph_widget.setGeometry(0, 0, self.width(), self.height())
        self.visualization_container.setGeometry(0, 0, self.width(), self.height())
        for widget in self.visualization_widgets.values():
            if widget:
                widget.setGeometry(0, 0, self.width(), self.height())

        self.leftbar.move(16, 16)
        self.addnote.move(54, 54)

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
        for widget in self.visualization_widgets.values(): # Cacher tous les widgets
            if widget:
                widget.hide()

        widget = self.visualization_widgets[mode] # Afficher uniquement le mode demandé
        widget.show()

        self.current_mode = mode
        print(f"🔁 Mode actif : {mode}")


    def toggle_search_input(self):
        self.searchbar_visible = not self.searchbar_visible

        if self.searchbar_visible:
            self.search_input.show()
            self.search_input.setEnabled(True)
            self.search_input.setFocus()
            self.search_button.setObjectName("Button_Default_Selected")
        else:
            self.search_input.hide()
            self.search_input.setEnabled(False)
            self.search_button.setObjectName("Button_Default")

        # Rafraîchir le style pour que le changement soit visible
        self.search_button.style().unpolish(self.search_button)
        self.search_button.style().polish(self.search_button)
        self.search_button.update()


    def toggle_addnote_input(self):
        self.addnote_visible = not self.addnote_visible

        if self.addnote_visible:
            self.addnote.show()
            self.addnote.setEnabled(True)
            self.addnote.setFocus()
            self.plus_button.setObjectName("Button_Default_Selected")
        else:
            self.addnote.hide()
            self.addnote.setEnabled(False)
            self.plus_button.setObjectName("Button_Default")

        # Rafraîchir le style pour que le changement soit visible
        self.plus_button.style().unpolish(self.plus_button)
        self.plus_button.style().polish(self.plus_button)
        self.plus_button.update()

    def toggle_cluster(self):
        self.cluster_visible = True
        self.timeline_visible = False
        self.theme_visible = False

        self.switch_note_mode("cluster")

        self.cluster_button.setObjectName("Button_Default_Selected")
        self.timeline_button.setObjectName("Button_Default")
        self.theme_button.setObjectName("Button_Default")
        self.refresh_note_mode_button()

    def toggle_timeline(self):
        self.cluster_visible = False
        self.timeline_visible = True
        self.theme_visible = False

        self.switch_note_mode("timeline")

        self.cluster_button.setObjectName("Button_Default")
        self.timeline_button.setObjectName("Button_Default_Selected")
        self.theme_button.setObjectName("Button_Default")
        self.refresh_note_mode_button()

    def toggle_theme(self):
        self.cluster_visible = False
        self.timeline_visible = False
        self.theme_visible = True

        self.switch_note_mode("theme")

        self.cluster_button.setObjectName("Button_Default")
        self.timeline_button.setObjectName("Button_Default")
        self.theme_button.setObjectName("Button_Default_Selected")
        self.refresh_note_mode_button()

    def refresh_note_mode_button(self):
        # Rafraîchir tous les boutons
        for btn in [self.cluster_button, self.timeline_button, self.theme_button]:
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()
