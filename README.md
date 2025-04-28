# MCQ API README

A FastAPI‑based backend for managing multiple‑choice questions, categories, quizzes and user authentication.

---

## Getting Started

### Prerequisites

#### Machine Setup
- [Python 3.12.x](https://www.python.org/downloads/)
- FastAPI
- [pip 23.2](https://pip.pypa.io/en/stable/installing/) (or latest version for Python 3.12)
- PostgreSQL
- Alembic (for DB migrations)
- SQLAlchemy
- JWT (for authentication)

### Clone Repository

```sh
git clone git@github.com:Muralidhar-t-89/mcq-demo.git
cd mcq-demo
```

#### How to run (using terminal/command line)
From the root directory of the project, create a Python virtual environment with:

`virtualenv venv -p python3`

Then activate it. On Windows, use:

`.venv/Scripts/activate`

On Mac or Linux, use:

`source .venv/bin/activate`

Once active, install the requirements with:

`pip install -r requirements.txt`

### Running migrations
Use `alembic` to update your local DB with

`alembic upgrade head`

### Run

Finally, run the application with:

`python -m uvicorn src.app.app_definition:mcq_app --reload`

### How to run tests (with terminal/command line)
From the root directory of the project, run:

```shell
python -m pytest ./tests/unit/
```

```shell
python -m pytest ./tests/integration/
```

---

## Authentication
The API uses JWT tokens for authentication. After logging in, you will receive a token that should be included in the `Authorization` header for all subsequent requests.


## Routes available:

### User Authentication
- **POST** `/register`  
  Register a new user.

- **POST** `/login`  
  Log in a user and return an access token.

---

### MCQ endpoints
- **GET** `/mcq`  
  List all MCQs.

- **GET** `/mcq/{id}`  
  Retrieve a single MCQ by its ID.

- **POST** `/mcq`  
  Create a new MCQ. *(Admin only)*

- **PUT** `/mcq/{id}`  
  Update an existing MCQ by ID. *(Admin only)*

- **DELETE** `/mcq/{id}`  
  Delete an MCQ by ID. *(Admin only)*

- **POST** `/mcq/bulk-upload`  
  Bulk‑upload MCQs from a CSV file. See [CSV Format](#csv-format) below. *(Admin only)*

---

### Category endpoints
- **GET** `/category`  
  List all categories.

- **GET** `/category/{id}`  
  Retrieve a single category by its ID.

- **POST** `/category`  
  Create a new category. *(Admin only)*

- **PUT** `/category/{id}`  
  Update a category by ID. *(Admin only)*

- **DELETE** `/category/{id}`  
  Delete a category by ID. *(Admin only)*

---

### Quiz endpoints
- **POST** `/quiz/start?category_id={category_id}`  
  Start a new quiz attempt for the given category (up to 25 random questions). Returns a unique `attempt_id` and the questions.

- **POST** `/quiz/submit`  
  Submit answers for an attempt. Payload must include `attempt_id`, `category_id`, and your answers. Returns your score breakdown.

- **GET** `/quiz/attempts`  
  List all past quiz attempts for the current user.

---

### Documentation
- `/docs` - Automatically-generated documentation

---

### CSV Format

Your CSV must have **exactly** these columns (in this order):

| sno | Question                                    | Options                                                 | Correct_options               | Category |
|-----|---------------------------------------------|---------------------------------------------------------|-------------------------------|----------|
| 1   | Who developed Python Programming Language?  | `['Wick van Rossum','Rasmus Lerdorf','Guido van Rossum','Niene Stom']` | `['Guido van Rossum']`        | 5        |
| 2   | Which keyword is used to define a function? | `['func','define','def','function']`                    | `['def']`                     | 5        |
| 3   | What is a list comprehension?               | `['A loop','A dict','A concise list','A set']`          | `['A concise list']`          | 5        |