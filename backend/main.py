"""
Digital Game Marketplace API
Steam/Epic/GOG-like game store with role-based access control
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers import users, games, orders, auth, admin, genres, cart
from .database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Digital Game Marketplace API",
    description="A Steam/Epic/GOG-like digital game marketplace with user, developer, and admin roles",
    version="2.0.0"
)

# Configure CORS
# allow_origins=["*"] and allow_credentials=True cannot be used together (CORS spec).
# Add production origins via ALLOWED_ORIGINS environment variable.
import os
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000")
_allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"}
    )

# Include routers
app.include_router(auth.router)      # /token, /me, /become-developer
app.include_router(users.router)     # /users
app.include_router(games.router)     # /games
app.include_router(genres.router)    # /genres
app.include_router(cart.router)      # /cart
app.include_router(orders.router)    # /orders
app.include_router(admin.router)     # /admin

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Digital Game Marketplace API",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
