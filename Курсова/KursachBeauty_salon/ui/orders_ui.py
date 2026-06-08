from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt
from .order_details_ui import OrderDetailsWindow
from .order_form_ui import OrderForm
from models.database import DatabaseManager

class OrdersWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Записи та Замовлення")
        self.setMinimumSize(600, 400)

        db = DatabaseManager()
        self.conn = db.connect()
        self.cursor = self.conn.cursor()

        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        self.btn_menu = QPushButton(" ⬅  Меню")
        self.btn_details = QPushButton(" 📝  Деталі запису")
        self.btn_add = QPushButton(" ➕  Додати запис")
        self.btn_edit = QPushButton(" ✏️  Редагувати")
        self.btn_delete = QPushButton(" 🗑️  Видалити")
        for btn in [self.btn_menu, self.btn_details, self.btn_add, self.btn_edit, self.btn_delete]:
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.btn_menu.clicked.connect(self.go_back)
        self.btn_add.clicked.connect(self.add_order)
        self.btn_edit.clicked.connect(self.edit_order)
        self.btn_delete.clicked.connect(self.delete_order)
        self.btn_details.clicked.connect(self.show_details)
        self.load_data()

    def go_back(self):
        current_geometry = self.geometry()
        self.main_window.setGeometry(current_geometry)
        self.hide()
        self.main_window.show()

    def load_data(self):
        try:
            self.cursor.execute("SELECT o.id, c.name, o.order_date, o.status, o.total_price FROM Orders o LEFT JOIN Customers c ON o.customer_id = c.id ORDER BY o.id DESC")
            rows = self.cursor.fetchall()
            headers = ["ID", "Клієнт", "Дата запису", "Статус", "Сума ($)"]
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            self.table.hideColumn(0)
            self.table.setAlternatingRowColors(True)
            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    item = QTableWidgetItem(str(val if val is not None else ""))
                    if j == 4: item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.table.setItem(i, j, item)
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зчитати дані:\n{e}")

    def add_order(self):
        self.order_form = OrderForm(self)
        self.order_form.setGeometry(self.geometry())
        self.order_form.show()
        self.hide()

    def edit_order(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Увага", "Оберіть запис для редагування.")
            return
        order_id = int(self.table.item(selected, 0).text())
        self.order_form = OrderForm(self, order_id=order_id)
        self.order_form.setGeometry(self.geometry())
        self.order_form.show()
        self.hide()

    def delete_order(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Увага", "Оберіть запис для видалення.")
            return
        order_id = int(self.table.item(selected, 0).text())
        reply = QMessageBox.question(self, "Підтвердження", f"Видалити запис №{order_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM Orders WHERE id=?", (order_id,))
                self.conn.commit()
                self.load_data()
            except Exception as e:
                self.conn.rollback()
                QMessageBox.critical(self, "Помилка", f"Не вдалося видалити запис: {e}")

    def show_details(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Увага", "Оберіть запис для перегляду.")
            return
        order_id = int(self.table.item(selected, 0).text())
        self.details_win = OrderDetailsWindow(order_id, self)
        self.details_win.setGeometry(self.geometry())
        self.details_win.show()
        self.hide()