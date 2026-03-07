import os
import sys
import uuid
import psycopg2
import pandas as pd
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from utils.db_handler import DatabaseHandler 


#env variables
load_dotenv(override=True)

#PostgreSQL connection for Render
URI_database = os.environ.get('External_Database_URI')

#Initialize engine database
engine = create_engine(URI_database)
SessionLocal = sessionmaker(bind = engine, autoflush=False, autocommit=False)

Base = declarative_base()








