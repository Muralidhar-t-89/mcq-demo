from fastapi import FastAPI

#from src.app.middlewares import store_request_logs
from src.app.routes.mcq_routes import mcq_blueprint
from src.app.orm.mcq_orm import start_mappers

mcq_app = FastAPI()

start_mappers()

mcq_app.include_router(mcq_blueprint)

@mcq_app.get("/")
async def root():
    return {"message": "Welcome, MCQ App is running now...."}
