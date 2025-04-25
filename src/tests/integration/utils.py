from fastapi.testclient import TestClient

from src.app.app_definition import mcq_app

client = TestClient(mcq_app)
