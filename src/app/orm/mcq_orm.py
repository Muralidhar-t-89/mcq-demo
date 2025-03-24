from datetime import datetime
from sqlalchemy import ARRAY, Boolean, Column, DateTime, Integer, MetaData, String, Table, Text, ForeignKey
from sqlalchemy.orm import registry

from src.app.entities.quiz_attempt_questions import AttemptQuestion
from src.app.entities.category import Category
from src.app.entities.mcq import MCQ
from src.app.entities.user import User
from src.app.entities.role import Role
from src.app.entities.quiz_attempt import QuizAttempt

mapper_registry = registry()

metadata = MetaData()

mcq = Table(
    "mcq",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("question", Text, nullable=False),
    Column("options", ARRAY(String), nullable=False),
    Column("category", String(50), nullable=False),
    Column("correct_option", ARRAY(String), nullable=False),
    Column("created_by", Integer, ForeignKey('users.id'), nullable=False),
    Column("created_date", DateTime, default=datetime.now()),
)

user = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("email", String, unique=True, nullable=False),
    Column("password", String(128), nullable=False),
    Column("role", Integer, ForeignKey('roles.id'), nullable=False),
    Column("created_date", DateTime, default=datetime.now(), nullable=False),
)

role = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("role_name", String(50), nullable=False),
    Column("created_date", DateTime, default=datetime.now(), nullable=False),
)

quiz_attempts = Table(
    "quiz_attempts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey('users.id'), nullable=False),
    Column("attempt_id", Integer, unique=True, nullable=False),
    Column("category_id", Integer, ForeignKey('categories.id'), nullable=False),
    Column("total_questions", Integer, nullable=False),
    Column("questions_attempted", Integer, nullable=False),
    Column("questions_unattempted", Integer, nullable=False),
    Column("correct_answers", Integer, nullable=False),
    Column("score", Integer, nullable=False),
    Column("created_date", DateTime, default=datetime.now(), nullable=False),
)

attempt_questions = Table(
    "attempt_questions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("attempt_id", String(6), ForeignKey('quiz_attempts.attempt_id'), nullable=False),
    Column("question_id", Integer, ForeignKey('mcq.id'), nullable=False),
    Column("attempted_answer", String, nullable=False),
    Column("is_correct", Boolean, nullable=False),
)


categories = Table(
    "categories",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), unique=True, nullable=False),
    Column("created_by", Integer, ForeignKey('users.id'), nullable=False),
    Column("created_date", DateTime, default=datetime.now(), nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(MCQ, mcq)
    mapper_registry.map_imperatively(User, user)
    mapper_registry.map_imperatively(Role, role)
    mapper_registry.map_imperatively(QuizAttempt, quiz_attempts)
    mapper_registry.map_imperatively(AttemptQuestion, attempt_questions)
    mapper_registry.map_imperatively(Category, categories)
