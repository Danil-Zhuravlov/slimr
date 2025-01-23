from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

# We'll add these modules as we build them
# from app.api import routes
# from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manager for the FastAPI app.
    This runs when the server starts and stops.
    Perfect for database connections, loading ML models, etc.
    """
    # Startup: Load things we need throughout the app's life
    print("Starting up Slimr...")
    # Here we'll later add:
    # - Database connection
    # - Loading ML models
    # - Initializing services
    
    yield  # App runs here
    
    # Shutdown: Clean up resources
    print("Shutting down Slimr...")
    # Here we'll later add:
    # - Close database connections
    # - Save any pending data
    # - Clean up resources

# Create the FastAPI app
app = FastAPI(
    title="Slimr API",
    description="Smart analytics and pricing optimization for Belgian SMEs",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Simple endpoint to check if API is running"""
    return {"status": "healthy", "version": "0.1.0"}

# Root endpoint
@app.get("/")
async def root():
    """Welcome message and basic API info"""
    return {
        "message": "Welcome to Slimr API",
        "docs": "/docs",  # Link to automatic API documentation
        "status": "operational"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
