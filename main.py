from fastapi import FastAPI
from core import init_db
from modules.auth import auth_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
init_db()
app.include_router(auth_router)


@app.get("/")

def read_root():
    return {"Test": "API is working!"}

