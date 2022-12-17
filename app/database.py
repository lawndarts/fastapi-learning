from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
#imports for raw sql method
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from .config import settings

SQL_ALCHEMY_DATABASE_URI = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQL_ALCHEMY_DATABASE_URI)#need to add another parameter for sqlight
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Dependency function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# old code for connecting to the database without sql alchemy. Used for running raw sql code
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='admin',
#             cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print('database connection was successful')
#         break
#     except Exception as error:
#         print(f'Connection to database failed: {error}')
#         time.sleep(2)

