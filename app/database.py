from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import time
import psycopg2
from .config import Settings


# Sql_database = 'postgresql://<username>:<password>@<hostname>/<database_name>'

Sql_database = f"postgresql://{Settings.DATABASE_USERNAME}:{Settings.DATABASE_PASSWORD}@{Settings.DATABASE_HOST}:{Settings.DATABASE_PORT}/{Settings.DATABASE_NAME}"

engine = create_engine(Sql_database)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:  # This is to keep the code running until it connects
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Fastapi",
            user="postgres",
            password="quhduzski",
            cursor_factory=RealDictCursor,
        )
        cur = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)
        time.sleep(5)  # The time it will wait before trying to reconnect
