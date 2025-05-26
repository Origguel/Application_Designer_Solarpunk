from PySide6.QtCore import QPropertyAnimation, QPoint, QRect, QEasingCurve

def animate_mode_leave(widget_out, container_width: int, callback=None):
    anim = QPropertyAnimation(widget_out, b"pos")
    anim.setDuration(300)
    anim.setEasingCurve(QEasingCurve.InBack)
    anim.setEndValue(QPoint(container_width, widget_out.y()))

    def on_finished():
        widget_out.hide()
        print("🔚 Sortie terminée")
        if callback:
            callback()

    anim.finished.connect(on_finished)
    anim.start()
    print("🟠 Animation de sortie déclenchée")
    return anim


def animate_mode_enter(widget_in, container):
    start_pos = QPoint(container.width(), widget_in.y())
    end_pos = QPoint(0, widget_in.y())

    widget_in.move(start_pos)
    widget_in.show()
    widget_in.raise_()

    anim = QPropertyAnimation(widget_in, b"pos")
    anim.setDuration(300)
    anim.setEasingCurve(QEasingCurve.OutBack)
    anim.setStartValue(start_pos)
    anim.setEndValue(end_pos)

    anim.start()
    print("🟢 Animation d'entrée déclenchée")
    return anim


def animate_container_resize(container, target_width: int, target_height: int, duration=300, callback=None):
    anim = QPropertyAnimation(container, b"geometry")
    anim.setDuration(duration)
    anim.setEasingCurve(QEasingCurve.OutBack)

    current_geom = container.geometry()
    target_geom = QRect(
        current_geom.x() + current_geom.width() - target_width,
        current_geom.y(),
        target_width,
        target_height
    )

    anim.setStartValue(current_geom)
    anim.setEndValue(target_geom)

    def on_finished():
        print("📏 Resize terminé")
        if callback:
            callback()

    anim.finished.connect(on_finished)
    anim.start()
    print("🟡 Resize lancé")
    return anim
