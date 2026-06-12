from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

load_dotenv()

class DatabaseManager:
    def __init__(self):
        DATABASE_URL = os.getenv("DATABASE_URL")
        self.engine = create_engine(
            DATABASE_URL, 
            echo = False
        )
        self.session = sessionmaker(
            bind=self.engine
        )
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def create_session(self):
        return self.session()