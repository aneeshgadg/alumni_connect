# Alumni Connect Platform

A career navigation and warm-introduction platform connecting university students with alumni professionals.

## Project Structure

```
alumni_connect/
├── backend/          # FastAPI backend application
├── frontend/         # Next.js frontend application
├── docs/            # Architecture and design documentation
└── README.md         # This file
```

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js 14+ (React) with TypeScript
- **Database**: PostgreSQL
- **Cache**: Redis
- **Cloud**: AWS

See [TECH_STACK.md](./TECH_STACK.md) for detailed technology specifications.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+

### Development Setup

1. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   ```

3. **Environment Variables**:
   - Copy `.env.example` to `.env` in both `backend/` and `frontend/`
   - Configure database and API keys

4. **Run Development Servers**:
   ```bash
   # Backend (from backend/)
   uvicorn app.main:app --reload

   # Frontend (from frontend/)
   npm run dev
   ```

## Documentation

- [Architecture](./ARCHITECTURE.md) - System architecture and design
- [Data Model](./DATA_MODEL.md) - Database schema and models
- [API Specification](./API_SPECIFICATION.md) - REST API documentation
- [Tech Stack](./TECH_STACK.md) - Technology choices and rationale

## License

[To be determined]
