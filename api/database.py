from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

load_dotenv()

db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(db_url)

if not database_exists(engine.url):
    create_database(engine.url)
    print("✅ Database created!")
else:
    print("✅ Database already exists!")

# Now connect normally
engine.connect()

sessionLocal = sessionmaker(autoflush=False, bind=engine)