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

    def record_exist(self, id):
        """Проверка существует ли забись в базе"""
        result = self.cursor.execute("SELECT COUNT(*) FROM `base` WHERE `id` = ?", (id,))
        return bool(result.fetchone()[0])

    def record_add(self, id, data):
        """Добавляем азпись в базу"""
        try:
            result = self.cursor.execute("INSERT INTO base (id, title, url, price, list, description, img) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                        (id, data['title'], data['url'], data['price'], data['list'],data['description'], data['img']))

        except sqlite3.Error as e:
            print(e)

    def clearOld_record(self):
        """Чиста базы от старых записей старше n дней"""
        self.cursor.execute("DELETE FROM base WHERE date(dt) < date('now', '-5 days')")

    def close(self):
        """Close coonnect DB"""
        self.connection.commit()
        self.connection.close()