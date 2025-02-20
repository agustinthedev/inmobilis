import sqlite3
from Util import Util

class DB:
    def __init__(self):
        pass

    def __start_connection(self):
        connection = sqlite3.connect(Util().get_db_name())
        return connection.cursor()