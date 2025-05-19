from PySide6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, QSequentialAnimationGroup


def get_leave_animation(widget, screen_width, duration=500):
    """Animation : le widget sort à droite de l'écran"""
    original_pos = widget.pos()
    offscreen_right = QPoint(screen_width + 100, original_pos.y())

    anim = QPropertyAnimation(widget, b"pos")
    anim.setDuration(duration)
    anim.setStartValue(original_pos)
    anim.setEndValue(offscreen_right)
    anim.setEasingCurve(QEasingCurve.InOutQuad)
    return anim


def get_enter_animation(widget, screen_width, duration=500):
    """Animation : le widget entre depuis la droite de l'écran"""
    original_pos = widget.pos()
    offscreen_right = QPoint(screen_width + 100, original_pos.y())

    anim = QPropertyAnimation(widget, b"pos")
    anim.setDuration(duration)
    anim.setStartValue(offscreen_right)
    anim.setEndValue(original_pos)
    anim.setEasingCurve(QEasingCurve.InOutQuad)
    return anim


def play_enter_exit_sequence(widget, screen_width, on_mid_callback=None, duration=1000):
    leave = get_leave_animation(widget, screen_width, duration)
    enter = get_enter_animation(widget, screen_width, duration)

    sequence = QSequentialAnimationGroup(widget)  # 👈 optionnel mais bon pour attacher
    sequence.addAnimation(leave)

    if on_mid_callback:
        leave.finished.connect(on_mid_callback)

    sequence.addAnimation(enter)
    sequence.start()

    return sequence  # 👈 indispensable
