from fastapi import FastAPI
from src.api.routers import drugs  # This line works now

app = FastAPI()

app.include_router(drugs.router, prefix="/drugs", tags=["Drugs"])

@app.get("/")
def root():
    return {"message": "MedBrain API is live"}
