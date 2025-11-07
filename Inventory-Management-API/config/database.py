from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

db_url = "postgresql://postgres:1@localhost:5232/mahaInventory"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)