import sqlite3

class DB:

    def __init__(self,db_file):
        """Init connect Database"""
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """Create tables"""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS base
                          (id INTEGER, title TEXT NOT NULL, url TEXT, 
                          price INTEGER, list TEXT, description TEXT, 
                          img TEXT, dt datetime default current_timestamp)""")

    def record_exist(self,id):
        """Проверка существует ли забись в базе"""
        result = self.cursor.execute("SELECT `id` FROM `base` WHERE `id` = ?", (id,))
        return bool(len(result.fetchall()))

    def record_add(self,data):
        """Добавляем азпись в базу"""
        for id in data:
            self.cursor.execute("INSERT INTO base (id, title, url, price, list, description, img) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (id, data[id]['title'], data[id]['url'], data[id]['price'], data[id]['list'],
                        data[id]['description'], data[id]['img']))

    def clearOld_record(self, n=5):
        """Чиста базы от старых записей старше n дней"""
        days = f"-{n} days"
        self.cursor.execute("DELETE FROM base WHERE date(dt) < date('now', '-5 days')")

    def close(self):
        """Close coonnect DB"""
        self.connection.close()