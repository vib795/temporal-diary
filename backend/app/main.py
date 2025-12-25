from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import entries, context

app = FastAPI(
    title="Temporal Diary API",
    description="Time-shifted journaling with cosmic context",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(entries.router, prefix="/api/v1")
app.include_router(context.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Temporal Diary API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
