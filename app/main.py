from fastapi import FastAPI
from routers import user
from models import models

app = FastAPI()

models.Base.metadata.create_all()

app.include_router(user.router, prefix="/api/user")