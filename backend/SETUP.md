# Backend Setup Guide

## Initial Setup

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
```

### 2. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI and Uvicorn
- SQLAlchemy and Alembic
- PostgreSQL drivers
- JWT and password hashing libraries
- And all other dependencies

### 4. Verify Installation

Check that Alembic is installed:
```bash
alembic --version
```

You should see something like: `alembic 1.12.1`

### 5. Configure Environment Variables

Make sure you have a `.env` file in the `backend/` directory with:
- `DATABASE_URL` (from Supabase)
- `SECRET_KEY` (generate with: `openssl rand -hex 32`)
- Other required variables

### 6. Run Database Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration: create users, students, alumni tables"

# Apply migration
alembic upgrade head
```

### 7. Run Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### "alembic: command not found"
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check that `venv/bin` (or `venv\Scripts` on Windows) is in your PATH

### "Module not found" errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Database connection errors
- Verify `DATABASE_URL` in `.env` is correct
- Check that Supabase database is accessible
- Ensure your IP is whitelisted in Supabase (or use connection pooling)

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description"

# Run server
uvicorn app.main:app --reload

# Deactivate virtual environment (when done)
deactivate
```


