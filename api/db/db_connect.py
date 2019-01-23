import psycopg2
from os import environ
from psycopg2.extras import RealDictCursor, Json

class Database:

    def __init__(self):
        try:
            # self.conn = psycopg2.connect(environ.get("DATABASE"))
            self.conn = psycopg2.connect("dbname='ireporter' user='postgres' host='localhost' password='.Adgjmp1' ")
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            self.conn.autocommit = True
            self.create_tables()
            print("connected to database")
        except (Exception, psycopg2.Error) as e:
            print(e)

    def create_tables(self):
        tables=("""
        DROP TABLE IF EXISTS users;
        CREATE TABLE IF NOT EXISTS users
        (id serial PRIMARY KEY, 
        firstname varchar(100), 
        lastname varchar(100), 
        othernames varchar(100),
        username varchar(100) NOT NULL,
        phoneNumber varchar(20), 
        registered TIMESTAMP DEFAULT NOW(),
        password varchar(255) NOT NULL, 
        email varchar(50) NOT NULL, 
        isAdmin BOOLEAN NOT NULL 

        """,
        """
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
        comment varchar(100) NOT NULL
        """,

        """
        DROP TABLE IF EXISTS interventions;
        CREATE TABLE IF NOT EXISTS interventions(
        id serial PRIMARY KEY, 
        created_on TIMESTAMP DEFAULT NOW(), 
        created_by varchar(50), 
        incident_type varchar(50), 
        location varchar(50), 
        status varchar(20), 
        image varchar(255), 
        comment varchar(100))    
        """)
        for table in tables:
            self.cursor.execute(table)



