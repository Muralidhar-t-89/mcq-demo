import uvicorn

from app.app_definition import mcq_app

if __name__ == "__main__":
    uvicorn.run(mcq_app, host="0.0.0.0", port=8001)