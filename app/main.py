from fastapi import FastAPI
from app.routes import incidents

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to BlackLine RMS API"}

app.include_router(incidents.router)
