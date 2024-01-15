from fastapi import FastAPI

from routers import auth as AuthRouter
from routers import predict as PredictRouter
from routers import user as UserRouter

app = FastAPI()


@app.middleware("http")
async def set_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


# app.include_router(QuestionsAiRouter.router, prefix='/api/questions-ai')
app.include_router(PredictRouter.router, prefix='/api')
app.include_router(AuthRouter.router, prefix='/api')
app.include_router(UserRouter.router, prefix='/api')
