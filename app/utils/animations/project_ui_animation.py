from PySide6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, QPauseAnimation, QSequentialAnimationGroup


def get_leave_animation(widget, screen_width, duration=250, delay=0, overshoot=0.6):
    original_pos = widget.pos()
    offscreen_right = QPoint(screen_width + 100, original_pos.y())

    anim = QPropertyAnimation(widget, b"pos")
    anim.setDuration(duration)
    anim.setStartValue(original_pos)
    anim.setEndValue(offscreen_right)

    easing = QEasingCurve(QEasingCurve.InBack)
    easing.setOvershoot(overshoot)
    anim.setEasingCurve(easing)

    if delay > 0:
        sequence = QSequentialAnimationGroup()
        sequence.addAnimation(QPauseAnimation(delay))
        sequence.addAnimation(anim)
        return sequence
    else:
        return anim



def get_enter_animation(widget, screen_width, duration=750, delay=0, overshoot=0.6):
    original_pos = widget.pos()
    offscreen_right = QPoint(screen_width + 100, original_pos.y())

    anim = QPropertyAnimation(widget, b"pos")
    anim.setDuration(duration)
    anim.setStartValue(offscreen_right)
    anim.setEndValue(original_pos)

    easing = QEasingCurve(QEasingCurve.OutBack)
    easing.setOvershoot(overshoot)
    anim.setEasingCurve(easing)

    if delay > 0:
        sequence = QSequentialAnimationGroup()
        sequence.addAnimation(QPauseAnimation(delay))
        sequence.addAnimation(anim)
        return sequence
    else:
        return anim




def play_enter_exit_sequence(widget, screen_width, on_mid_callback=None, duration=1000):
    leave = get_leave_animation(widget, screen_width, duration=250, delay=0, overshoot=0.6)
    enter = get_enter_animation(widget, screen_width, duration=750, delay=500, overshoot=0.6)

    sequence = QSequentialAnimationGroup(widget)  # 👈 optionnel mais bon pour attacher
    sequence.addAnimation(leave)

    if on_mid_callback:
        leave.finished.connect(on_mid_callback)

    sequence.addAnimation(enter)
    sequence.start()

    return sequence  # 👈 indispensable
