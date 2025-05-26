from PySide6.QtCore import QEasingCurve, QPoint, QSize, QPropertyAnimation, QParallelAnimationGroup
from PySide6.QtWidgets import QWidget

def get_enter_animation(widget: QWidget, target_pos: QPoint, target_size: QSize, offset_x=38, duration=300):
    animations = QParallelAnimationGroup()

    # Position de départ à gauche
    start_pos = QPoint(target_pos.x() - offset_x, target_pos.y())
    widget.move(start_pos)

    # Animation de position
    move_anim = QPropertyAnimation(widget, b"pos")
    move_anim.setDuration(duration)
    move_anim.setStartValue(start_pos)
    move_anim.setEndValue(target_pos)
    easing_pos = QEasingCurve(QEasingCurve.OutBack)
    easing_pos.setOvershoot(0.6)
    move_anim.setEasingCurve(easing_pos)

    # Animation de taille
    start_size = QSize(32, target_size.height())
    resize_anim = QPropertyAnimation(widget, b"size")
    resize_anim.setDuration(duration)
    resize_anim.setStartValue(start_size)
    resize_anim.setEndValue(target_size)
    resize_anim.setEasingCurve(QEasingCurve.InOutCubic)

    animations.addAnimation(move_anim)
    animations.addAnimation(resize_anim)
    return animations

def get_leave_animation(widget: QWidget, target_pos: QPoint, target_size: QSize, offset_x=38, duration=300):
    animations = QParallelAnimationGroup()

    # Position de départ = actuelle
    start_pos = widget.pos()
    end_pos = QPoint(target_pos.x() - offset_x, target_pos.y())

    # Animation de position
    move_anim = QPropertyAnimation(widget, b"pos")
    move_anim.setDuration(duration)
    move_anim.setStartValue(start_pos)
    move_anim.setEndValue(end_pos)
    easing_pos = QEasingCurve(QEasingCurve.InBack)
    easing_pos.setOvershoot(0.6)
    move_anim.setEasingCurve(easing_pos)

    # Animation de taille
    resize_anim = QPropertyAnimation(widget, b"size")
    resize_anim.setDuration(duration)
    resize_anim.setStartValue(widget.size())
    resize_anim.setEndValue(target_size)
    resize_anim.setEasingCurve(QEasingCurve.InOutCubic)

    animations.addAnimation(move_anim)
    animations.addAnimation(resize_anim)
    return animations

def play_toolbar_animation(widget: QWidget, visible: bool, target_pos=QPoint(54, 16), 
                            target_size=QSize(370, 32), offset_x=38, duration=300):
    if visible:
        widget.setVisible(True)
        widget.raise_()
        widget.setEnabled(True)
        anim = get_enter_animation(widget, target_pos, target_size, offset_x, duration)
    else:
        anim = get_leave_animation(widget, target_pos, QSize(32, target_size.height()), offset_x, duration)

        def hide_after():
            widget.setEnabled(False)
            widget.setVisible(False)
            widget.move(target_pos)

        anim.finished.connect(hide_after)

    anim.start()
    return anim
