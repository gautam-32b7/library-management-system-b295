import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .evn file
load_dotenv()

def create_connection():
    try:
        conn = psycopg2.connect(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except:
        print("Error connecting to PostgreSQL")
        return None
