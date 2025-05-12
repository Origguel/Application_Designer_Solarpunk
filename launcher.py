import sys
import subprocess
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QFont, QPainter, QColor, QGuiApplication
from PySide6.QtCore import Qt, QRect

class CustomSplash(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SplashScreen)
        self.resize(400, 200)
        self.setStyleSheet("background-color: white;")

        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        splash_geometry = self.geometry()
        x = (screen_geometry.width() - splash_geometry.width()) // 2
        y = (screen_geometry.height() - splash_geometry.height()) // 2
        self.move(x, y)

    def drawContents(self, painter):
        painter.setPen(QColor("#2B2B2B"))
        painter.setFont(QFont("Arial", 32, QFont.Bold))
        rect = QRect(0, 0, self.width(), self.height())
        painter.drawText(rect, Qt.AlignCenter, "Mycelium")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = CustomSplash()
    splash.show()
    app.processEvents()

    # Lancer le vrai programme et ATTENDRE qu’il se termine
    try:
        process = subprocess.Popen([sys.executable, "main.py"])
        process.wait()  # <-- Bloque ici jusqu'à fermeture de main.py
    except Exception as e:
        splash.showMessage(f"Erreur : {e}", Qt.AlignBottom | Qt.AlignCenter, Qt.red)
    finally:
        splash.close()

    sys.exit()
