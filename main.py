import uvicorn
from fastapi import FastAPI
from database import SessionLocal, engine, Base
from routers import user as UserRouter
from routers import auth as AuthRouter
from routers import questions_ai as QuestionsAiRouter, predict as PredictRouter

Base.metadata.create_all(engine)
app = FastAPI()

@app.middleware("http")
async def set_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

app.include_router(UserRouter.router, prefix='/api/user')
app.include_router(QuestionsAiRouter.router, prefix='/api/questions-ai')
app.include_router(PredictRouter.router, prefix='/api/predict')
app.include_router(AuthRouter.router, prefix="/api/auth")