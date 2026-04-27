import sqlite3

class Database:
    def __init__(self, db_name='grab_helper.db'):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS restaurants (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                location TEXT NOT NULL);''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS menus (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                restaurant_id INTEGER,
                                name TEXT NOT NULL,
                                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id));''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS dishes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                menu_id INTEGER,
                                name TEXT NOT NULL,
                                price REAL NOT NULL,
                                FOREIGN KEY (menu_id) REFERENCES menus(id));''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_query TEXT NOT NULL,
                                bot_response TEXT NOT NULL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);''')
        self.connection.commit()

    def add_restaurant(self, name, location):
        try:
            self.cursor.execute('INSERT INTO restaurants (name, location) VALUES (?, ?)', (name, location))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding restaurant: {e}")
            return False

    def add_menu(self, restaurant_id, menu_name):
        try:
            self.cursor.execute('INSERT INTO menus (restaurant_id, name) VALUES (?, ?)', (restaurant_id, menu_name))
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error adding menu: {e}")
            return None

    def add_dish(self, menu_id, dish_name, price):
        try:
            self.cursor.execute('INSERT INTO dishes (menu_id, name, price) VALUES (?, ?, ?)', (menu_id, dish_name, price))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding dish: {e}")
            return False

    def add_chat_history(self, user_query, bot_response):
        try:
            self.cursor.execute('INSERT INTO chat_history (user_query, bot_response) VALUES (?, ?)', (user_query, bot_response))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding chat history: {e}")
            return False

    def get_restaurants(self):
        self.cursor.execute('SELECT * FROM restaurants')
        return self.cursor.fetchall()

    def get_menus(self, restaurant_id):
        self.cursor.execute('SELECT * FROM menus WHERE restaurant_id = ?', (restaurant_id,))
        return self.cursor.fetchall()

    def get_dishes(self, menu_id):
        self.cursor.execute('SELECT * FROM dishes WHERE menu_id = ?', (menu_id,))
        return self.cursor.fetchall()

    def get_chat_history(self):
        self.cursor.execute('SELECT user_query, bot_response FROM chat_history ORDER BY id DESC')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()