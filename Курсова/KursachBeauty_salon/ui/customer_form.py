from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)
from models.database import DatabaseManager


class CustomerForm(QDialog):
    def __init__(self, mode="add", customer_data=None):
        super().__init__()
        self.mode = mode
        self.customer_data = customer_data
        self.setWindowTitle("Редагування клієнта" if mode == "edit" else "Додавання клієнта")
        self.resize(400, 250)

        db = DatabaseManager()
        self.conn = db.connect()
        self.cursor = self.conn.cursor()

        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()
        form_layout.addRow("Прізвище та ім’я:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Телефон:", self.phone_input)
        form_layout.addRow("Адреса:", self.address_input)

        button_layout = QHBoxLayout()
        self.btn_save = QPushButton(" 💾 Зберегти")
        self.btn_cancel = QPushButton(" ❌ Скасувати")
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.save_customer)

        if self.mode == "edit" and self.customer_data:
            self.load_customer_data()

    def load_customer_data(self):
        if self.customer_data and len(self.customer_data) >= 5:
            self.name_input.setText(self.customer_data[1])
            self.email_input.setText(self.customer_data[2])
            self.phone_input.setText(self.customer_data[3])
            self.address_input.setText(self.customer_data[4])

    def save_customer(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Помилка", "Поле 'Прізвище та ім’я' є обов’язковим!")
            return

        try:
            if self.mode == "add":
                self.cursor.execute(
                    "INSERT INTO Customers (name, email, phone, address) VALUES (?, ?, ?, ?)",
                    (name, email, phone, address)
                )
            else:
                customer_id = self.customer_data[0]
                self.cursor.execute(
                    "UPDATE Customers SET name=?, email=?, phone=?, address=? WHERE id=?",
                    (name, email, phone, address, customer_id)
                )

            self.conn.commit()
            self.accept()
        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Помилка", f"Помилка при збереженні:\n{e}")
