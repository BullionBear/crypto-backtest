from fastapi import FastAPI
from core.config import settings

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/test")
async def test():
    return {"text": settings.SECRET_KEY}

