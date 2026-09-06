"""
CropGuard AI: FastAPI Backend Application
Main entry point orchestrating ML predictors, local NLP chatbot,
real-time weather queries, Plant Disease Vision, Self-Improving AI loop, and Supabase data operations.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from Backend.routes import health, weather, predict, chat, history, profile, disease_vision, self_improving

app = FastAPI(
    title="CropGuard AI Backend API",
    description=(
        "Weather-Based Crop Health Predictor & Self-Improving Agronomic Intelligence API integrating: "
        "Multi-Crop Disease Vision CNN, Crop Recommendation Ensemble, Regression, Classification, Clustering, "
        "Forward/Backward Reasoning, and Local Domain-Specific NLP Chatbot."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration for Flutter Web & Mobile Clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"],
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
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": f"An unexpected error occurred: {str(exc)}",
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
app.include_router(disease_vision.router)
app.include_router(self_improving.router)

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    print(f"Starting CropGuard AI API on http://{host}:{port}...")
    uvicorn.run("Backend.app:app", host=host, port=port, reload=True)
