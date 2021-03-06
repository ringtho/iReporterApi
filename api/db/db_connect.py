import psycopg2
import os
from os import environ
from psycopg2.extras import RealDictCursor


class Database:

    def __init__(self):
        try:
            if os.getenv("STATE")=="Testing":
                dbname = "ireportertest"
            else:
                dbname = "ireporter"
            # self.conn = psycopg2.connect(environ.get("DATABASE_URL"))
            self.conn = psycopg2.connect(dbname=dbname,user="postgres",host='localhost',password='.Adgjmp1')
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            self.cur = self.conn.cursor()
            self.conn.autocommit = True
            self.create_users_table()
            self.create_redflags_table()
            self.create_interventions_table()
          
            print("connected to database")
        except (Exception, psycopg2.OperationalError) as e:
            print(e)

    def create_users_table(self):
        query = """
        DROP TABLE IF EXISTS users;
        CREATE TABLE IF NOT EXISTS users
        (id serial PRIMARY KEY, 
        firstname varchar(100), 
        lastname varchar(100), 
        othernames varchar(100),
        username varchar(100) NOT NULL,
        phoneNumber varchar(20), 
        registered TIMESTAMP DEFAULT NOW(),
        password varchar NOT NULL, 
        email varchar(50) NOT NULL, 
        isAdmin BOOLEAN NOT NULL); """
        self.cursor.execute(query)

    def create_redflags_table(self):
        query = """ 
        DROP TABLE IF EXISTS redflags;
        CREATE TABLE IF NOT EXISTS redflags(
        id serial PRIMARY KEY, 
        created_on TIMESTAMP DEFAULT NOW(), 
        created_by INTEGER REFERENCES users(id), 
        incident_type varchar(50), 
        location varchar(255) NOT NULL, 
        status varchar(20) NOT NULL, 
        images varchar(255), 
        videos varchar(255),
        comment varchar(100) NOT NULL);"""
        self.cursor.execute(query)

    def create_interventions_table(self):
        query =  """
        DROP TABLE IF EXISTS interventions;
        CREATE TABLE IF NOT EXISTS interventions(
        id serial PRIMARY KEY, 
        created_on TIMESTAMP DEFAULT NOW(), 
        created_by INTEGER REFERENCES users(id), 
        incident_type varchar(50), 
        location varchar(255) NOT NULL, 
        status varchar(20) NOT NULL, 
        images varchar(255), 
        videos varchar(255),
        comment varchar(100) NOT NULL);
        """
        self.cursor.execute(query)
        

    def empty_tables(self):
        self.cursor.execute("TRUNCATE TABLE users CASCADE")
        self.cursor.execute("TRUNCATE TABLE redflags CASCADE")
        self.cursor.execute("TRUNCATE TABLE interventions CASCADE")

    def get_cursor(self):
        return self.cursor

if __name__ == '__main__':
    db = Database()



