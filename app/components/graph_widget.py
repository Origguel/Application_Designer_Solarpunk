from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QWidget
from PySide6.QtGui import QPainter, QWheelEvent, QMouseEvent
from PySide6.QtCore import Qt

from app.utils.graph_logic import GraphLogic
from app.components.note_detail_widget import NoteDetailWidget
from app.components.interactive_ellipse_item import InteractiveEllipseItem

class GraphWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setSceneRect(-5000, -5000, 10000, 10000)
        self.setRenderHints(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scale(1.2, 1.2)

        self.text_items = []
        self.detail_panel = None

        # Overlay pour les détails
        self.overlay_container = QWidget(self)
        self.overlay_container.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.overlay_container.setAttribute(Qt.WA_NoSystemBackground, True)
        self.overlay_container.setStyleSheet("background: transparent;")
        self.overlay_container.setGeometry(0, 0, self.width(), self.height())
        self.overlay_container.raise_()

        self.graph_logic = GraphLogic(self)
        self.graph_logic.draw_graph()

        # Variables pour drag classique
        self._drag_active = False
        self._drag_start_position = None

        # 🆕 Ajouté proprement ici
        self.selected_note_id = None

    def wheelEvent(self, event: QWheelEvent):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        zoom_factor = zoom_in_factor if event.angleDelta().y() > 0 else zoom_out_factor

        old_anchor = self.transformationAnchor()
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.scale(zoom_factor, zoom_factor)
        self.setTransformationAnchor(old_anchor)
        self.graph_logic.update_text_visibility()
        event.accept()

    from app.components.interactive_ellipse_item import InteractiveEllipseItem

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if item and isinstance(item, InteractiveEllipseItem):
                # 🔥 Enlever les highlights de tous
                for other_item in self.scene.items():
                    if isinstance(other_item, InteractiveEllipseItem):
                        other_item.remove_highlight()

                note_id = item.data(0)
                self.select_note(note_id)
                print(f"✅ Note sélectionnée : {note_id}")

        elif event.button() == Qt.RightButton:
            self._drag_active = True
            self._drag_start_position = event.pos()
            self.setCursor(Qt.ClosedHandCursor)

        super().mousePressEvent(event)




    def mouseMoveEvent(self, event: QMouseEvent):
        if self._drag_active and self._drag_start_position is not None:
            delta = event.pos() - self._drag_start_position
            self._drag_start_position = event.pos()

            slow_factor = 0.5
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x() * slow_factor)
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y() * slow_factor)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            self._drag_active = False
            self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)

    def show_note_detail(self, note_data):
        if self.detail_panel:
            self.detail_panel.setParent(None)

        self.detail_panel = NoteDetailWidget(note_data, parent=self.overlay_container)
        self.detail_panel.resize(500, self.height() - 68 - 26)
        self.detail_panel.move(self.width() - 500 - 34, 68)
        self.detail_panel.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'overlay_container'):
            self.overlay_container.setGeometry(0, 0, self.width(), self.height())

    # 🆕 Correctement placé ici
    def select_note(self, note_id):
        """Simule la sélection d'une note par son ID."""
        self.selected_note_id = note_id

    def get_selected_note_id(self):
        """Retourne l'ID de la note sélectionnée."""
        return self.selected_note_id
