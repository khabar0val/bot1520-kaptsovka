import sqlite3

class SQLighterLottery:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect('lottery.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_request(self, user_id, phio):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `requests` (`user_id`, `phio`) VALUES(?,?)", (user_id, phio))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()