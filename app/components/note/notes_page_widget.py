from PySide6.QtWidgets import QWidget
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
from app.components.note.notes_camera_animation import animate_camera_to_center


class NotesPageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.is_camera_animating = False
        setup_ui(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.graph_widget.setGeometry(0, 0, self.width(), self.height())
        self.toolbar.move(16, 16)
        self.note_mode.move(500, 500)
        self.search_input.move(58, 16)
        if self.overlay.isVisible():
            self.overlay.setGeometry(0, 0, self.width(), self.height())
        if self.add_note_widget:
            self.add_note_widget.move(
                (self.width() - self.add_note_widget.width()) // 2,
                (self.height() - self.add_note_widget.height()) // 2
            )
        if hasattr(self, "note_mode"):
            widget_width = self.note_mode.width()
            widget_height = self.note_mode.height()
            x = (self.width() - widget_width) // 2
            y = self.height() - widget_height - 16
            self.note_mode.move(x, y)

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

        current_center = self.graph_widget.mapToScene(self.graph_widget.viewport().rect().center())
        current_scale = self.graph_widget.transform().m11()
        center_threshold = 5.0
        scale_threshold = 0.01
        target_center = QPointF(0, 0)
        target_scale = 0.1

        if (current_center - target_center).manhattanLength() < center_threshold and abs(current_scale - target_scale) < scale_threshold:
            print("✅ Vue déjà centrée et zoomée, animation ignorée.")
            return

        animate_camera_to_center(self)

