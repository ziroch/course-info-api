# course-info-python

FastAPI implementation of the sibling `course-info-spring` REST API using Python's built-in `sqlite3` module.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

By default the app stores data in `./courses.db`. Override it with:

```bash
COURSE_INFO_DATABASE=/path/to/courses.db uvicorn app.main:app --reload
```

## Test

```bash
pytest
```
