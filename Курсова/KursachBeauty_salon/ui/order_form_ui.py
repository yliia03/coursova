from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem,
    QPushButton, QSpinBox, QMessageBox
)
from PyQt5.QtCore import Qt
from datetime import datetime
from models.database import DatabaseManager


class OrderForm(QWidget):
    def __init__(self, parent_window, order_id=None):
        super().__init__()
        self.parent_window = parent_window
        self.order_id = order_id
        self.setWindowTitle("Редагування запису" if order_id else "Новий запис")
        self.resize(850, 550)

        db = DatabaseManager()
        self.conn = db.connect()
        self.cursor = self.conn.cursor()

        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Клієнт:"))
        self.cmb_customer = QComboBox()
        top_layout.addWidget(self.cmb_customer)
        top_layout.addWidget(QLabel("Статус:"))
        self.cmb_status = QComboBox()
        top_layout.addWidget(self.cmb_status)
        layout.addLayout(top_layout)

        if not self.order_id:
            self.cmb_status.addItem("нове")
            self.cmb_status.setEnabled(False)
        else:
            self.cmb_status.addItems(["нове", "підтверджене", "виконане", "скасоване"])

        layout.addWidget(QLabel("Виберіть послуги та товари:"))
        self.table = QTableWidget()
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton(" 💾  Зберегти")
        self.btn_cancel = QPushButton(" ❌  Скасувати")
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.btn_save.clicked.connect(self.save_order)
        self.btn_cancel.clicked.connect(self.cancel)

        self.load_customers()
        self.load_services()

        if self.order_id:
            self.load_order_data()

        self.old_status = self.cmb_status.currentText() if self.order_id else "нове"

    def load_customers(self):
        self.cursor.execute("SELECT id, name FROM Customers")
        for cid, name in self.cursor.fetchall():
            self.cmb_customer.addItem(name, cid)

    def load_services(self):
        self.cursor.execute("SELECT id, name, price_usd, stock_quantity FROM Services")
        rows = self.cursor.fetchall()
        headers = ["ID", "Назва", "Ціна ($)", "Залишок", "Кількість"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(rows))

        for i, (pid, name, price, stock) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(pid)))
            self.table.setItem(i, 1, QTableWidgetItem(name))
            self.table.setItem(i, 2, QTableWidgetItem(f"{price:.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(str(stock)))
            spin = QSpinBox()
            spin.setRange(0, stock if stock is not None else 0)
            self.table.setCellWidget(i, 4, spin)

        self.table.hideColumn(0)
        self.table.resizeColumnsToContents()

    def load_order_data(self):
        self.cursor.execute("SELECT customer_id, status FROM Orders WHERE id=?", (self.order_id,))
        order = self.cursor.fetchone()
        if order:
            customer_id, status = order
            idx = self.cmb_customer.findData(customer_id)
            if idx >= 0: self.cmb_customer.setCurrentIndex(idx)
            if status: self.cmb_status.setCurrentText(status)

        self.cursor.execute("SELECT service_id, quantity FROM OrderItems WHERE order_id=?", (self.order_id,))
        items = dict(self.cursor.fetchall())
        for i in range(self.table.rowCount()):
            pid = int(self.table.item(i, 0).text())
            if pid in items:
                self.table.cellWidget(i, 4).setValue(items[pid])

    def save_order(self):
        customer_id = self.cmb_customer.currentData()
        if customer_id is None:
            QMessageBox.warning(self, "Помилка", "Оберіть клієнта!")
            return

        new_status = self.cmb_status.currentText()
        order_items, total = [], 0.0
        for i in range(self.table.rowCount()):
            if self.table.cellWidget(i, 4).value() > 0:
                pid = int(self.table.item(i, 0).text())
                price = float(self.table.item(i, 2).text())
                qty = self.table.cellWidget(i, 4).value()
                total += price * qty
                order_items.append((pid, qty, price, price * qty))

        if not order_items:
            QMessageBox.warning(self, "Помилка", "Оберіть хоча б одну послугу/товар!")
            return

        try:
            if self.order_id:
                self.cursor.execute("UPDATE Orders SET customer_id=?, total_price=?, status=? WHERE id=?",
                                    (customer_id, total, new_status, self.order_id))
                self.cursor.execute("DELETE FROM OrderItems WHERE order_id=?", (self.order_id,))
                order_id = self.order_id
            else:
                self.cursor.execute("INSERT INTO Orders (customer_id, order_date, status, total_price) VALUES (?, ?, ?, ?)", (customer_id, datetime.now().strftime("%Y-%m-%d"), new_status, total))
                order_id = self.cursor.lastrowid

            for pid, qty, price, subtotal in order_items:
                self.cursor.execute("INSERT INTO OrderItems (order_id, service_id, quantity, unit_price, subtotal) VALUES (?, ?, ?, ?, ?)", (order_id, pid, qty, price, subtotal))

            if self.old_status != "виконане" and new_status == "виконане":
                for pid, qty, _, _ in order_items:
                    self.cursor.execute("UPDATE Services SET stock_quantity = stock_quantity - ? WHERE id = ? AND duration_min = 0", (qty, pid))

            self.conn.commit()
            QMessageBox.information(self, "Успіх", "Замовлення збережено!")
            self.close()
            self.parent_window.load_data()
            self.parent_window.show()
        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти замовлення:\n{e}")

    def cancel(self):
        self.close()
        self.parent_window.show()
