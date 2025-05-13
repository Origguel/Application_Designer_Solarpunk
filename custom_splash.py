# custom_splash.py
from PySide6.QtWidgets import QSplashScreen
from PySide6.QtGui import QFont, QPainter, QColor, QGuiApplication
from PySide6.QtCore import Qt, QRect

class CustomSplash(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.resize(400, 200)
        self.setStyleSheet("background-color: white;")

        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

        self.percent = 0
        self.message = ""

    def set_progress(self, percent: int, message: str = ""):
        self.percent = percent
        if message:
            self.message = message
        self.update()

    def drawContents(self, painter: QPainter):
        painter.setPen(QColor("#2B2B2B"))
        painter.setFont(QFont("Arial", 32, QFont.Bold))
        painter.drawText(QRect(0, 30, self.width(), 50), Qt.AlignCenter, "Mycelium")

        painter.setFont(QFont("Arial", 14))
        painter.drawText(QRect(0, self.height() - 70, self.width(), 30), Qt.AlignCenter, self.message)
        painter.drawText(QRect(0, self.height() - 40, self.width(), 30), Qt.AlignCenter, f"{self.percent}%")
