from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from app.routes import products
from app.routes import consultations
from app.routes import shoes
from app.routes import users
from app.routes import auth
from app import oauth2
from app.routes import smartcart_cart
from app.routes import smartcart_transaction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(auth.router)
app.include_router(oauth2.router)
app.include_router(users.router)
app.include_router(consultations.router)
app.include_router(shoes.router)
app.include_router(products.router)
app.include_router(smartcart_cart.router)
app.include_router(smartcart_transaction.router)