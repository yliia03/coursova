from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

class ServiceDetailsWindow(QWidget):
    def __init__(self, details):
        super().__init__()
        self.setWindowTitle(f"Деталі: {details[1]}")

        self.resize(500, 350)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_details(details)

    def load_details(self, details):
        labels = ["ID", "Назва", "Майстер", "Категорія", "Тривалість (хв)", "Ціна ($)", "Залишок (шт)"]
        self.table.setRowCount(len(labels))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Характеристика", "Значення"])

        for i, label in enumerate(labels):
            self.table.setItem(i, 0, QTableWidgetItem(label))
            self.table.setItem(i, 1, QTableWidgetItem(str(details[i])))