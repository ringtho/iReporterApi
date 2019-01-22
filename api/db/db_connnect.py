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
            print("connected to database")
        except (Exception, psycopg2.Error) as e:
            print(e)

    def create_table_users(self):
        users= """
        CREATE TABLE IF NOT EXISTS users
        (id serial PRIMARY KEY, 
        firstname varchar(100), 
        lastname varchar(100), 
        othernames varchar(100),
        username varchar(100),
        phoneNumber varchar(20), 
        password varchar(255), 
        email varchar(50), 
        role varchar(50))

        """
        self.cursor.execute(users)
    
    def create_table_redflags(self):

        redflags = """
        CREATE TABLE IF NOT EXISTS redflags(
        id serial PRIMARY KEY, 
        created_on TIMESTAMP DEFAULT NOW(), 
        created_by varchar(50), 
        incident_type varchar(50), 
        location varchar(50), 
        status varchar(20), 
        image varchar(255), 
        comment varchar(100))
        """
        self.cursor.execute(redflags)

    def create_table_interventions(self):
        interventions = """
        CREATE TABLE IF NOT EXIST interventions(
        id serial PRIMARY KEY, 
        created_on TIMESTAMP DEFAULT NOW(), 
        created_by varchar(50), 
        incident_type varchar(50), 
        location varchar(50), 
        status varchar(20), 
        image varchar(255), 
        comment varchar(100))    
        )
        """

        self.cursor.execute(interventions)

Database()