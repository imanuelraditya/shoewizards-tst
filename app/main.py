from fastapi import FastAPI
import uvicorn
from app.routes import products, shoes, users, consultations, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(consultations.router)
app.include_router(shoes.router)
app.include_router(products.router)