from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from src.app.config import settings


DATABASE_URL = (
        f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )

engine = create_engine(DATABASE_URL, echo=True)

DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(DATABASE_URL), autocommit=False, autoflush=False)


def build_postgresql_engine():
    with engine.connect() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS categories (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) UNIQUE NOT NULL,
                    created_by INTEGER NOT NULL,    
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
        )

        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role INTEGER NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
        )

        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS mcq (
                    id SERIAL PRIMARY KEY,
                    question TEXT NOT NULL,
                    options TEXT[] NOT NULL,
                    correct_option TEXT[] NOT NULL,
                    category INTEGER NOT NULL,
                    created_by INTEGER NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category) REFERENCES categories (id),
                    FOREIGN KEY (created_by) REFERENCES users (id)
                );
                """
            )
        )

        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS quiz_attempts (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    attempt_id INTEGER UNIQUE NOT NULL,
                    category_id INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    questions_attempted INTEGER NOT NULL,
                    questions_unattempted INTEGER NOT NULL,
                    correct_answers INTEGER NOT NULL,
                    score INTEGER NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                );
                """
            )
        )

        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS attempt_questions (
                    id SERIAL PRIMARY KEY,
                    attempt_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    attempted_answer TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    is_correct BOOLEAN NOT NULL,  -- 1 for correct, 0 for incorrect
                    FOREIGN KEY (attempt_id) REFERENCES quiz_attempts (attempt_id),
                    FOREIGN KEY (question_id) REFERENCES mcq (id)
                );
                """
            )
        )
        conn.commit()


def get_db():
    db = DEFAULT_SESSION_FACTORY()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    build_postgresql_engine()
