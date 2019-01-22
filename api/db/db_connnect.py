import psycopg2
from os import environ
from psycopg2.extras import RealDictCursor

class Database:

    def __init__(self):
        try:
            # self.conn = psycopg2.connect(environ.get("DATABASE_URL"))
            self.conn = psycopg2.connect("dbname='ireporter' user='postgres' host='localhost' password='.Adgjmp1' ")
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            self.conn.autocommit = True
            print("connected")
        except (Exception, psycopg2.Error) as e:
            print(e)

Database()