from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Sql_database = 'postgresql://<username>:<password>@<hostname>/<database_name>'

Sql_database = "postgresql://postgres:quhduzski@localhost/Fastapi"

engine = create_engine(Sql_database)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
