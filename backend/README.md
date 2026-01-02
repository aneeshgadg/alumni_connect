# Alumni Connect Backend

FastAPI backend application for the Alumni Connect platform.

## Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your database and Redis credentials
   ```

4. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Run development server**:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/          # API version 1 endpoints
│   │       ├── students/
│   │       ├── alumni/
│   │       ├── requests/
│   │       ├── introductions/
│   │       └── outcomes/
│   ├── core/             # Core configuration
│   │   ├── config.py     # Settings
│   │   ├── database.py   # Database setup
│   │   └── security.py   # Auth utilities
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── main.py          # FastAPI app
├── alembic/              # Database migrations
├── tests/                # Test files
└── requirements.txt      # Dependencies
```

## Development

- **Format code**: `black app/`
- **Lint code**: `ruff check app/`
- **Type check**: `mypy app/`
- **Run tests**: `pytest`

