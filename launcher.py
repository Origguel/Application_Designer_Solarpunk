import sys
import subprocess
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QFont, QPainter, QColor, QGuiApplication
from PySide6.QtCore import Qt, QRect, QTimer

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

        self.percent = 0

    def drawContents(self, painter):
        # Texte principal "Mycelium"
        painter.setPen(QColor("#2B2B2B"))
        painter.setFont(QFont("Arial", 32, QFont.Bold))
        painter.drawText(QRect(0, 30, self.width(), 50), Qt.AlignCenter, "Mycelium")

        # Texte secondaire : pourcentage
        painter.setFont(QFont("Arial", 14))
        painter.drawText(QRect(0, self.height() - 50, self.width(), 30), Qt.AlignCenter, f"Chargement... {self.percent}%")

def update_progress(splash: CustomSplash, app: QApplication, callback_on_complete):
    def step():
        splash.percent += 1
        splash.update()
        app.processEvents()
        if splash.percent < 100:
            QTimer.singleShot(50, step)  # temps total ~5s
        else:
            callback_on_complete()

    step()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = CustomSplash()
    splash.show()
    app.processEvents()

    # Quand le chargement est terminé (100%), fermer splash et lancer l'app principale
    def on_complete():
        splash.close()
        try:
            subprocess.Popen([sys.executable, "main.py"])  # ← Lancer sans attendre
        except Exception as e:
            print(f"Erreur de lancement : {e}")
        sys.exit()  # Ferme le launcher

    update_progress(splash, app, on_complete)
    sys.exit(app.exec())
