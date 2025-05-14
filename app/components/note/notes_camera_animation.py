from PySide6.QtCore import QTimer, QPointF

def animate_camera_to_center(self, duration_ms=1000, target_scale=0.1):
    def ease_in_out_expo(t):
        if t == 0: return 0
        if t == 1: return 1
        return 0.5 * pow(2, 20 * t - 10) if t < 0.5 else 1 - 0.5 * pow(2, -20 * t + 10)

    if self.is_camera_animating:
        return

    view = self.graph_widget
    self.is_camera_animating = True
    view.setInteractive(False)

    steps = 60
    interval = duration_ms // steps
    initial_scale = view.transform().m11()
    scale_diff = target_scale - initial_scale
    current_center = view.mapToScene(view.viewport().rect().center())
    delta_center = QPointF(0, 0) - current_center
    step = 0

    def animate_step():
        nonlocal step
        if step >= steps:
            timer.stop()
            view.setInteractive(True)
            self.is_camera_animating = False
            print("✅ Animation terminée")
            return

        t = ease_in_out_expo((step + 1) / steps)
        scale = initial_scale + scale_diff * t
        center = current_center + delta_center * t

        view.resetTransform()
        view.scale(scale, scale)
        view.centerOn(center)
        self.graph_widget.update_category_display()
        step += 1

    timer = QTimer(self)
    timer.timeout.connect(animate_step)
    timer.start(interval)
