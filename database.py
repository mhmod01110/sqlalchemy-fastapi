from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the environment variable
# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = "mysql://avnadmin:AVNS_0K7EcwWjHq22FAEWcoV@mysql-01110-mhmod-01110.h.aivencloud.com:20017/defaultdb?ssl-mode=REQUIRED"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
