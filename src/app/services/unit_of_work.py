import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.build_db import DEFAULT_SESSION_FACTORY
from src.app.config import settings
from src.app.repositories.category_repository import CategoryRepository
from src.app.repositories.log_repo import LogRepository
from src.app.repositories.mcq_repository import MCQRepository
from src.app.repositories.quiz_attempt_repository import QuizAttemptRepository
from src.app.repositories.user_repository import UserRepository

# DATABASE_URL = (
#     f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@"
#     f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
# )
#
# DEFAULT_SESSION_FACTORY = sessionmaker(
#     bind=create_engine(DATABASE_URL, echo=True)
# )


class BaseUnitOfWork(abc.ABC):
    user_repo: UserRepository
    mcq_repo: MCQRepository
    category_repo: CategoryRepository
    quiz_attempt_repo: QuizAttemptRepository
    log_repo: LogRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class MCQUnitOfWork(BaseUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.user_repo = UserRepository(session=self.session)
        self.mcq_repo = MCQRepository(session=self.session)
        self.category_repo = CategoryRepository(session=self.session)
        self.quiz_attempt_repo = QuizAttemptRepository(session=self.session)
        self.log_repo = LogRepository(session=self.session)
        return self #super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
