import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from models.database import DatabaseManager

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Помилка: файл 'style.qss' не знайдено.")

    db_manager = DatabaseManager()
    db_manager.connect()

    app.aboutToQuit.connect(db_manager.close)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())