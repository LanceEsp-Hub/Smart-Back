#backend\app\main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine
from app.models import models
from pathlib import Path

import os
from starlette.middleware.sessions import SessionMiddleware
from app.routers import (
    auth_router, 
    # user_router, 
    google_auth_router, 
    password_reset_router, 
    pet_dashboard_router, 
    pet_router,
    user_router, notification_router,
    message_router,
    admin_router
      
)
from fastapi.staticfiles import StaticFiles  # Add this import

SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "asdasdasdsad")
UPLOAD_DIR = Path("app/uploads/pet_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]  # Add this line

)

# Include the routers
app.include_router(user_router.router)  # Added user router

app.include_router(auth_router.router, prefix="/api")
app.include_router(user_router.router, prefix="/api")
app.include_router(google_auth_router.router)
app.include_router(password_reset_router.router, prefix="/api")
app.include_router(pet_dashboard_router.router)
app.include_router(notification_router.router)
app.include_router(message_router.router)
app.include_router(admin_router.router)



# backend/app/main.py (add this line with other router includes)
app.include_router(pet_router.router)

# Mount the static directory
app.mount("/uploads/pet_images", StaticFiles(directory="app/uploads/pet_images"), name="pet_images")
app.mount("/uploads/messages", StaticFiles(directory="app/uploads/messages"), name="message_images")