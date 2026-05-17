from fastapi import FastAPI
from modules.auth import auth_router

app = FastAPI()
app.include_router(auth_router)


@app.get("/")

def read_root():
    return {"Test": "API is working!"}

