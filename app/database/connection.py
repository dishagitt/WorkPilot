from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DB_URL = "postgresql://postgres:1234@localhost:5432/workpilot"

engine = create_engine(DB_URL)

session = sessionmaker(autocommit= False, autoflush= False, bind= engine)

Base = declarative_base()