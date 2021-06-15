import sqlite3

class SQLighterOtzivy:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect('otzivy.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_otziv(self, user_id, otziv):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `otzivy` (`user_id`, `otziv`) VALUES(?,?)", (user_id, otziv))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()