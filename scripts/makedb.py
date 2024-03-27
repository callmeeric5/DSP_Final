import psycopg2
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, DB_PORT

class database():
    # create a function to connect to the database using psycopg2
    def __init__(self):
        self.db = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

