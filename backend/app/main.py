"""
Alumni Connect Platform - FastAPI Application
Main entry point for the backend API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Create FastAPI app instance
app = FastAPI(
    title="Alumni Connect API",
    description="Career navigation and warm-introduction platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Alumni Connect API",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


# Include API routers (will be added in future steps)
# from app.api.v1 import students, alumni, requests, introductions, outcomes
# app.include_router(students.router, prefix=settings.API_V1_PREFIX, tags=["students"])
# app.include_router(alumni.router, prefix=settings.API_V1_PREFIX, tags=["alumni"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

