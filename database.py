from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase


URL= "sqlite:///notes.db"

engine = create_engine(URL)

sessionLocal= sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db= sessionLocal()
    try:
        yield db
    finally:
        db.close()
        