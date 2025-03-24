from sqlalchemy import create_engine, text


def build_new_sqlite_db():
    engine = create_engine("sqlite+pysqlite:///mcq_database.db", echo=True)

    with engine.connect() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_by INTEGER NOT NULL,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
        )

        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role INTEGER NOT NULL,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
        )

        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS mcq (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    options TEXT NOT NULL,
                    correct_option TEXT NOT NULL,
                    category INTEGER NOT NULL,
                    created_by INTEGER NOT NULL,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
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
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    attempt_id INTEGER UNIQUE NOT NULL,
                    category_id INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    questions_attempted INTEGER NOT NULL,
                    questions_unattempted INTEGER NOT NULL,
                    correct_answers INTEGER NOT NULL,
                    score INTEGER NOT NULL,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
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
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
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


if __name__ == "__main__":
    build_new_sqlite_db()
