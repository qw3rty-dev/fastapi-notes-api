from fastapi import FastAPI
from database import Base,engine
from routes import notes,auth

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(notes.router)
app.include_router(auth.router)


