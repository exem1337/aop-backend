import uvicorn
from fastapi import FastAPI
from database import SessionLocal, engine, Base
from routers import user as UserRouter
from routers import questions_ai as QuestionsAiRouter, predict as PredictRouter

Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(UserRouter.router, prefix='/api/user')
app.include_router(QuestionsAiRouter.router, prefix='/api/questions-ai')
app.include_router(PredictRouter.router, prefix='/api/predict')