from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QWheelEvent, QMouseEvent
from PySide6.QtCore import Qt


class TreeGraphInteraction:
    def __init__(self, view: QGraphicsView):
        self.view = view
        self._drag_active = False
        self._drag_start_position = None

    def wheel_event(self, event: QWheelEvent):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        zoom_factor = zoom_in_factor if event.angleDelta().y() > 0 else zoom_out_factor

        old_anchor = self.view.transformationAnchor()
        self.view.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.view.scale(zoom_factor, zoom_factor)
        self.view.setTransformationAnchor(old_anchor)
        event.accept()

    def mouse_press_event(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            self._drag_active = True
            self._drag_start_position = event.pos()
            self.view.setCursor(Qt.ClosedHandCursor)

    def mouse_move_event(self, event: QMouseEvent):
        if self._drag_active and self._drag_start_position is not None:
            delta = event.pos() - self._drag_start_position
            self._drag_start_position = event.pos()

            slow_factor = 0.5
            self.view.horizontalScrollBar().setValue(self.view.horizontalScrollBar().value() - delta.x() * slow_factor)
            self.view.verticalScrollBar().setValue(self.view.verticalScrollBar().value() - delta.y() * slow_factor)

    def mouse_release_event(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            self._drag_active = False
            self.view.setCursor(Qt.ArrowCursor)
