from fastapi import FastAPI
from app.routes import incidents, users, auth

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to BlackLine RMS API"}

app.include_router(auth.router)
app.include_router(incidents.router)
app.include_router(users.router)
