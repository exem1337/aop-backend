from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import auth as AuthRouter
from routers import predict as PredictRouter
from routers import user as UserRouter
from routers import courses as CoursesRouter
from routers import themes as ThemeRouter

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(QuestionsAiRouter.router, prefix='/api/questions-ai')
app.include_router(PredictRouter.router, prefix='/api')
app.include_router(AuthRouter.router, prefix='/api')
app.include_router(UserRouter.router, prefix='/api')
app.include_router(CoursesRouter.router, prefix='/api')
app.include_router(ThemeRouter.router, prefix='/api')
