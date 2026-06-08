from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt
from models.database import DatabaseManager

class OrderDetailsWindow(QWidget):
    def __init__(self, order_id, main_window=None):
        super().__init__()
        self.order_id = order_id
        self.main_window = main_window
        self.setWindowTitle(f"Деталі замовлення №{order_id}")
        self.resize(800, 400)

        db = DatabaseManager()
        self.conn = db.connect()
        self.cursor = self.conn.cursor()

        layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        self.label_title = QLabel(f"<b>Замовлення №{self.order_id}</b>")
        self.btn_back = QPushButton(" ⬅  Назад")

        self.btn_back.clicked.connect(self.go_back)
        header_layout.addWidget(self.label_title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_back)
        layout.addLayout(header_layout)

        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_details()

    def go_back(self):
        self.close()
        if self.main_window:
            current_geometry = self.geometry()
            self.main_window.setGeometry(current_geometry)
            self.main_window.show()

    def load_details(self):
        try:
            self.cursor.execute("SELECT s.name, oi.quantity, oi.unit_price, oi.subtotal FROM OrderItems oi LEFT JOIN Services s ON oi.service_id = s.id WHERE oi.order_id = ?", (self.order_id,))
            rows = self.cursor.fetchall()

            headers = ["Послуга/Товар", "Кількість", "Ціна ($)", "Сума ($)"]
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            self.table.setRowCount(len(rows))
            self.table.setAlternatingRowColors(True)

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value) if value is not None else "")
                    if col_idx in [1, 2, 3]:
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.table.setItem(row_idx, col_idx, item)

            if not rows:
                QMessageBox.information(self, "Інформація", "Це замовлення не містить позицій.")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зчитати деталі:\n{e}")