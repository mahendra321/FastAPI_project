from fastapi import FastAPI 
from .database import engine
from . import models
from .routers import posts, users, auth, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_username)


#models.Base.metadata.create_all(bind=engine)

# app object
app=FastAPI()

origins = ['https://www.youtube.com','https://www.google.com']
#origins = ['https://www.youtube.com/','https://www.amazon.in/','https://www.google.com/']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"meesage":"Hello world"} 
