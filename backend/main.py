from fastapi import FastAPI
from api.api import router as rolls_router

app = FastAPI(
    title="API",
    description="API to manage rolls",
    version="1.0.0"
)

app.include_router(rolls_router)

@app.get("/")
async def root():
    return {"message": "Rolls API is running!"}