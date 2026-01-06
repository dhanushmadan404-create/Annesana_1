from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
import os
load_dotenv()

db_url= os.getenv("DATABASE_URL")
engine=create_engine( db_url)
# binding engine
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base=declarative_base()

# Dependency function to get database session
def get_db():
   
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # Initialize database - creates all tables
# def init_db():
#     """
#     Creates all tables in the database.
#     Called automatically when the application starts.
#     """
#     Base.metadata.create_all(bind=engine)

