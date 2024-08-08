import sqlite3
from datetime import datetime, timedelta

from .config import logger, DATABASE_NAME
from .list import spare_columns

class Database():
    def __init__(self, db_name):
        self.connection = sqlite3.Connection(db_name)
        self.cursor = self.connection
        self.create_db()
    
    def create_db(self):
        try:
            query = ("CREATE TABLE IF NOT EXISTS users ("
                    "id INTEGER PRIMARY KEY, "
                    "user_id BIGINT, "
                    "username TEXT, "
                    "fio TEXT, "
                    "spare1 TEXT, "
                    "spare2 TEXT);")
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            logger.error(f'Ошибка при создании таблицы users: {e}')
        
        try:
            query = ("CREATE TABLE IF NOT EXISTS stats ("
                    "id INTEGER PRIMARY KEY, "
                    "group_id TEXT, "
                    "date TEXT, "
                    "fio TEXT, "
                    "spare1 INTEGER, "
                    "spare2 INTEGER, "
                    "spare3 INTEGER, "
                    "spare4 INTEGER, "
                    "spare5 INTEGER, "
                    "spare6 BIGINT);")
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            logger.error(f'Ошибка при создании таблицы stats: {e}')

    
    def add_data(self, data_list):

        self.cursor.execute(f'INSERT INTO stats ('
                    'group_id, date, fio, '
                    'spare1, spare2, spare3, '
                    'spare4, spare5, spare6'
                    ') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                    (data_list['group_id'],
                    data_list['date'], data_list['fio'], 
                    data_list['spare1'], data_list['spare2'],
                    data_list['spare3'], data_list['spare4'], 
                    data_list['spare5'], data_list['spare6']))
        self.connection.commit()

    def add_user(self, user_id, username):
        try:
            query = "SELECT COUNT(*) FROM users WHERE user_id = ?"
            count = self.cursor.execute(query, (user_id,))
            count = count.fetchone()[0]
            if count > 0:
                return

            query = "INSERT INTO users (user_id, username) VALUES (?, ?)"
            self.cursor.execute(query, (user_id, username))
            self.connection.commit()
            logger.info(f'Пользователь {username} успешно добавлен.')
        except Exception as e:
            logger.error(f'Ошибка add_user: {e}')
        
    def get_spars(self, data, index, fio: list):
        try:
            sums = {}

            for column in spare_columns:
                match index:
                    case "day":
                        query =  f"SELECT SUM({column}) FROM stats WHERE date = ?"
                        result = self.cursor.execute(query, (data,))
                    case "week":
                        seven_days_ago = datetime.now() - timedelta(days=7)
                        seven_days_ago = seven_days_ago.strftime('%d.%m.%Y')

                        query = f"SELECT SUM({column}) FROM stats WHERE date >= ?"
                        result = self.cursor.execute(query, (seven_days_ago,))
                    case "mes":
                        data = f"%{data}%"

                        query =  f"SELECT SUM({column}) FROM stats WHERE date LIKE ?"
                        result = self.cursor.execute(query, (data,))
                    case "year":
                        data = f"%{data}%"

                        query = f"SELECT SUM({column}) FROM stats WHERE date LIKE ?"
                        result = self.cursor.execute(query, (data,))
                    case "usersday":
                        fio_placeholders = ', '.join('?' * len(fio))

                        query = f"SELECT SUM({column}) FROM stats WHERE date = ? AND fio IN ({fio_placeholders})"
                        params = [data] + fio
                        result = self.cursor.execute(query, params)
                    case "usersweek":
                        fio_placeholders = ', '.join('?' * len(fio))

                        seven_days_ago = datetime.now() - timedelta(days=7)
                        seven_days_ago = seven_days_ago.strftime('%d.%m.%Y')

                        query = f"SELECT SUM({column}) FROM stats WHERE date >= ? AND fio IN ({fio_placeholders})"
                        params = [seven_days_ago] + fio
                        result = self.cursor.execute(query, params)
                    case "usersmes":
                        fio_placeholders = ', '.join('?' * len(fio))

                        data = f"%{data}%"

                        query =  f"SELECT SUM({column}) FROM stats WHERE date LIKE ? AND fio IN ({fio_placeholders})"
                        params = [data] + fio
                        result = self.cursor.execute(query, params)
                    case "usersyear":
                        fio_placeholders = ', '.join('?' * len(fio))
                        
                        data = f"%{data}%"

                        query = f"SELECT SUM({column}) FROM stats WHERE date LIKE ? AND fio IN ({fio_placeholders})"
                        params = [data] + fio
                        result = self.cursor.execute(query, params)
                    case _:
                        query =  f"SELECT SUM({column}) FROM stats"
                        result = self.cursor.execute(query)
                
                result = result.fetchone()[0]
                if result is None:
                    result = ''
                sums[column] = result

            return sums

        except Exception as e:
            logger.error(f'Ошибка при get_spars: {e}')
            return {}
    

    def __del__(self):
        self.cursor.close()
        self.connection.close()

db = Database(DATABASE_NAME)