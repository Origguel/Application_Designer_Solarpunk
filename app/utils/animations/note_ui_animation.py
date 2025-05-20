from PySide6.QtCore import QEasingCurve, QPoint, QSize, QPropertyAnimation, QParallelAnimationGroup
from PySide6.QtWidgets import QWidget

def get_toolbar_enter_animation(widget: QWidget, offset_x=38, target_width=370, duration=1000):
    animations = QParallelAnimationGroup()

    start_pos = QPoint(widget.pos().x() - offset_x, widget.pos().y())
    end_pos = widget.pos()
    widget.move(start_pos)

    move_anim = QPropertyAnimation(widget, b"pos")
    move_anim.setDuration(duration)
    move_anim.setStartValue(start_pos)
    move_anim.setEndValue(end_pos)
    easing_pos = QEasingCurve(QEasingCurve.OutBack)
    easing_pos.setOvershoot(0.6)
    move_anim.setEasingCurve(easing_pos)

    resize_anim = QPropertyAnimation(widget, b"size")
    resize_anim.setDuration(duration)
    resize_anim.setStartValue(QSize(32, widget.height()))
    resize_anim.setEndValue(QSize(target_width, widget.height()))
    resize_anim.setEasingCurve(QEasingCurve.InOutCubic)

    animations.addAnimation(move_anim)
    animations.addAnimation(resize_anim)
    return animations

def get_toolbar_leave_animation(widget: QWidget, offset_x=-38, target_width=32, duration=1000):
    animations = QParallelAnimationGroup()

    start_pos = widget.pos()
    end_pos = QPoint(start_pos.x() + offset_x, start_pos.y())

    move_anim = QPropertyAnimation(widget, b"pos")
    move_anim.setDuration(duration)
    move_anim.setStartValue(start_pos)
    move_anim.setEndValue(end_pos)
    easing_pos = QEasingCurve(QEasingCurve.InBack)
    easing_pos.setOvershoot(0.6)
    move_anim.setEasingCurve(easing_pos)

    resize_anim = QPropertyAnimation(widget, b"size")
    resize_anim.setDuration(duration)
    resize_anim.setStartValue(widget.size())
    resize_anim.setEndValue(QSize(target_width, widget.height()))
    resize_anim.setEasingCurve(QEasingCurve.InOutCubic)

    animations.addAnimation(move_anim)
    animations.addAnimation(resize_anim)
    return animations

def play_toolbar_animation(widget: QWidget, visible: bool):
    final_pos = QPoint(54, 16)

    if visible:
        widget.move(final_pos)
        widget.setVisible(True)
        widget.raise_()
        widget.setEnabled(True)
        anim = get_toolbar_enter_animation(widget)
    else:
        anim = get_toolbar_leave_animation(widget)

        def hide_after():
            widget.setEnabled(False)
            widget.setVisible(False)
            widget.move(final_pos)

        anim.finished.connect(hide_after)

    anim.start()
    return anim