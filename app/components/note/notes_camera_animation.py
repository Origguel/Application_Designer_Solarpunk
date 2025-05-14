from PySide6.QtCore import QTimer, QPointF

def animate_camera_to_center(self, duration_ms=1000, target_scale=0.1):
    def ease_in_out_expo(t):
        if t == 0: return 0
        if t == 1: return 1
        return 0.5 * pow(2, 20 * t - 10) if t < 0.5 else 1 - 0.5 * pow(2, -20 * t + 10)

    if self.is_camera_animating:
        return

    self.is_camera_animating = True
    self.setInteractive(False)

    steps = 60
    interval = duration_ms // steps
    initial_scale = self.transform().m11()
    scale_diff = target_scale - initial_scale
    current_center = self.mapToScene(self.viewport().rect().center())
    delta_center = QPointF(0, 0) - current_center
    step = 0

    def animate_step():
        nonlocal step
        if step >= steps:
            timer.stop()
            self.setInteractive(True)
            self.is_camera_animating = False
            print("✅ Animation terminée")
            return

        t = ease_in_out_expo((step + 1) / steps)
        scale = initial_scale + scale_diff * t
        center = current_center + delta_center * t

        self.resetTransform()
        self.scale(scale, scale)
        self.centerOn(center)

        # Facultatif : rafraîchir les éléments graphiques si méthode dispo
        if hasattr(self, "update_category_display"):
            self.update_category_display()

        step += 1

    timer = QTimer(self)
    timer.timeout.connect(animate_step)
    timer.start(interval)
