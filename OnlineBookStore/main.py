from fastapi import FastAPI
from database import engine, Base
from routers import books, users, carts

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(books.router)
app.include_router(carts.router)
# app.include_router(orders.router)
