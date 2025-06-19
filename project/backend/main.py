from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .services.firebase_auth import initialize_firebase
from .api import auth as auth_router
from .api import notes as notes_router
from .api import media as media_router
from .api import links as links_router
# We have removed the import for the AI router
from .db.session import engine, Base

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Personal AI Dashboard API",
    description="Backend API for the personal dashboard, managing data and AI interactions.",
    version="1.0.0"
)

# --- Add CORS Middleware ---
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "null"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- End of CORS Middleware ---


# Include routers
app.include_router(auth_router.router, prefix="/api/auth", tags=["Authentication"]) 
app.include_router(notes_router.router, prefix="/api/notes", tags=["Notes"])
app.include_router(media_router.router, prefix="/api/media", tags=["Media"])
app.include_router(links_router.router, prefix="/api/links", tags=["Links"])
# The line including the AI router has been removed


@app.on_event("startup")
async def startup_event():
    """Code to run on application startup."""
    print("🚀 Application is starting up...")
    print(f"☁️ Cloudinary Cloud Name: {settings.CLOUDINARY_CLOUD_NAME}")
    initialize_firebase()
    print("✅ Database tables checked/created.")
    print("✅ Startup complete.")


@app.on_event("shutdown")
async def shutdown_event():
    """Code to run on application shutdown."""
    print("👋 Application is shutting down.")


@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint to check if the API is running."""
    return {"status": "ok", "message": "Welcome to the Personal AI Dashboard API!"}