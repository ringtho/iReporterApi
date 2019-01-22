import psycopg2
from os import environ
from psycopg2.extras import RealDictCursor

class Database:

    def __init__(self):
        try:
            self.conn = psycopg2.connect(environ.get("DATABASE_URL"))
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            self.conn.autocommit = True
        except (Exception, psycopg2.Error) as e:
            print(e)