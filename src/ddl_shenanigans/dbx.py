import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine(os.environ["DATABASE_URL"])
Session = sessionmaker(bind=engine)

def connect():
    return Session()
