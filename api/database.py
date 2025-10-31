from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql://postgres:admin@localhost/fastapia"

engine = create_engine(db_url)

sessionLocal = sessionmaker(autoflush=False, bind=engine)