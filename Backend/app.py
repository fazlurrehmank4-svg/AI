"""
CropGuard AI: FastAPI Backend Application
Main entry point orchestrating ML predictors, local NLP chatbot,
real-time weather queries, and Supabase data operations.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from Backend.routes import health, weather, predict, chat, history, profile

app = FastAPI(
    title="CropGuard AI Backend API",
    description=(
        "Weather-Based Crop Health Predictor API integrating 9 AI Lab Practicals: "
        "Regression, Classification, Clustering, Search, Forward/Backward Chaining, "
        "and Local Domain-Specific NLP Chatbot (Zero external LLMs)."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
allowed_origins_raw = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [o.strip() for o in allowed_origins_raw.split(",")] if "," in allowed_origins_raw else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic Request Timing Middleware & Safe Exception Handling
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"
        return response
    except Exception as exc:
        process_time = time.time() - start_time
        # Safe error masking for security
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred while processing the agricultural request.",
                "duration": f"{process_time:.4f}s"
            }
        )

# Register Routers
app.include_router(health.router)
app.include_router(weather.router)
app.include_router(predict.router)
app.include_router(chat.router)
app.include_router(history.router)
app.include_router(profile.router)

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    print(f"Starting CropGuard AI API on http://{host}:{port}...")
    uvicorn.run("Backend.app:app", host=host, port=port, reload=True)
