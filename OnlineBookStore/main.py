from fastapi import FastAPI
from database import Base, engine
import users,books

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(books.router, prefix="/api/books", tags=["Books"])