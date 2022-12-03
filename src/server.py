from fastapi import FastAPI, Request, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth_routes, product_routes, orders_routes

app = FastAPI()

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(product_routes.router)
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(orders_routes.router)

    