from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from app.api.routes import router as csv_router

# Run the FastAPI app with Uvicorn:
# uvicorn app.main:app --reload

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manager for the FastAPI app.
    This runs when the server starts and stops.
    Perfect for database connections, loading ML models, etc.
    """
    # Startup: Load things we need throughout the app's life
    print("Starting up Slimr...")
    
    yield 
    
    print("Shutting down Slimr...")

# Create the FastAPI app
app = FastAPI(
    title="Slimr API",
    description="Smart analytics and pricing optimization for Belgian SMEs",
    version="0.1.0",
    lifespan=lifespan
)


# Add this after creating the FastAPI app
app.include_router(csv_router, prefix="/api", tags=["csv"])

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
