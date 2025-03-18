from fastapi import FastAPI

app = FastAPI()

from core.db import init_db

@app.on_event("startup")
def on_startup():
    init_db()