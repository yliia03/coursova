import sqlite3

class DatabaseManager:
    _instance = None
    _connection = None

    def __new__(cls, db_name="data/beauty_salon.db"):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.db_name = db_name
        return cls._instance

    def connect(self):
        if self._connection is None:
            try:
                self._connection = sqlite3.connect(self.db_name)
            except sqlite3.Error as e:
                print(f"Помилка з'єднання з БД: {e}")
                return None
        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            print("З'єднання з базою даних закрито.")