from fastapi import FastAPI
import requests


app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"Page statistics"}
