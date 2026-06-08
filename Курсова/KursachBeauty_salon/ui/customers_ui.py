from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt
from .customer_form import CustomerForm
from models.database import DatabaseManager

class CustomersWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Клієнти Салону краси")
        self.setMinimumSize(600, 400)

        db = DatabaseManager()
        self.conn = db.connect()
        self.cursor = self.conn.cursor()

        main_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        self.btn_menu = QPushButton(" ⬅  Меню")
        self.btn_add = QPushButton(" ➕  Додати")
        self.btn_edit = QPushButton(" ✏️  Редагувати")
        self.btn_delete = QPushButton(" 🗑️  Видалити")
        for btn in [self.btn_menu, self.btn_add, self.btn_edit, self.btn_delete]:
            btn_layout.addWidget(btn)
        main_layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

        self.btn_menu.clicked.connect(self.go_back)
        self.btn_add.clicked.connect(self.add_customer)
        self.btn_edit.clicked.connect(self.edit_customer)
        self.btn_delete.clicked.connect(self.delete_customer)
        self.load_data()

    def go_back(self):
        current_geometry = self.geometry()
        self.main_window.setGeometry(current_geometry)
        self.hide()
        self.main_window.show()

    def load_data(self):
        try:
            self.cursor.execute("SELECT id, name, email, phone, address FROM Customers")
            rows = self.cursor.fetchall()
            headers = ["ID", "Прізвище та ім’я", "Email", "Телефон", "Адреса"]
            self.table.setColumnCount(len(headers))
            self.table.setRowCount(len(rows))
            self.table.setHorizontalHeaderLabels(headers)
            self.table.setAlternatingRowColors(True)
            for r, row in enumerate(rows):
                for c, val in enumerate(row):
                    item = QTableWidgetItem(str(val))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.table.setItem(r, c, item)
            self.table.hideColumn(0)
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зчитати дані:\n{e}")

    def add_customer(self):
        dialog = CustomerForm(mode="add")
        if dialog.exec_():
            self.load_data()

    def edit_customer(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Увага", "Виберіть клієнта для редагування.")
            return
        customer_data = [self.table.item(selected, c).text() for c in range(self.table.columnCount())]
        dialog = CustomerForm(mode="edit", customer_data=customer_data)
        if dialog.exec_():
            self.load_data()

    def delete_customer(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Увага", "Виберіть клієнта для видалення.")
            return
        customer_id = self.table.item(selected, 0).text()
        confirm = QMessageBox.question(self, "Підтвердження", f"Видалити клієнта ID {customer_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM Customers WHERE id=?", (customer_id,))
                self.conn.commit()
                self.load_data()
            except Exception as e:
                self.conn.rollback()
                QMessageBox.critical(self, "Помилка", f"Не вдалося видалити: {e}.\nМожливо, існують пов'язані замовлення.")