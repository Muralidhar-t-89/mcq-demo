import pytest
from sqlalchemy.orm import clear_mappers

from src.app.orm.mcq_orm import start_mappers
from src.app.services.unit_of_work import DEFAULT_SESSION_FACTORY


@pytest.fixture
def session():
    start_mappers()
    yield DEFAULT_SESSION_FACTORY()
    clear_mappers()
