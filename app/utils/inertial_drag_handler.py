from PySide6.QtCore import QObject, QPointF, QTimer

class InertialDragHandler(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.last_mouse_pos = None
        self.velocity = QPointF(0, 0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)

    def mousePressEvent(self, event):
        if event.button() == 2:  # Clique droit
            self.last_mouse_pos = event.pos()
            self.velocity = QPointF(0, 0)
            self.timer.stop()

    def mouseMoveEvent(self, event):
        if event.buttons() & 2 and self.last_mouse_pos is not None:
            current_pos = event.pos()
            delta = current_pos - self.last_mouse_pos

            # 📍Déplacement du graphe directement
            self.view.translate(delta.x(), delta.y())

            # 📍Mettre à jour la vélocité pour l'inertie plus tard
            self.velocity = QPointF(delta.x(), delta.y())

            self.last_mouse_pos = current_pos

    def mouseReleaseEvent(self, event):
        if event.button() == 2:  # Clique droit relâché
            if not self.timer.isActive() and (self.velocity.manhattanLength() > 0.1):
                self.timer.start(16)  # 60 FPS

    def update_position(self):
        # Appliquer la vélocité
        self.view.translate(self.velocity.x(), self.velocity.y())

        # 📉 Diminuer progressivement la vitesse
        self.velocity *= 0.90  # 10% de perte de vitesse par frame

        # 🛑 Stopper si vitesse trop faible
        if self.velocity.manhattanLength() < 0.5:
            self.timer.stop()
