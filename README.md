# MCQ API README

An API using FastAPI

## How to run (using terminal/command line)
From the root directory of the project, create a Python virtual environment with:

`virtualenv venv -p python3`

Then activate it. On Windows, use:

`.venv/Scripts/activate`

Once active, install the requirements with:

`pip install -r requirements.txt`

### Running migrations
Use `alembic` to update your local DB with

`alembic upgrade head`
