import os
import logging
import time
from typing import Literal
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import pandas as pd

from src.ingestion.loader import load_raw_dataset
from src.ingestion.preprocessor import preprocess
from src.input.models import UserPreference
from src.integration.filter_engine import filter_with_fallback
from src.integration.formatter import format_restaurants_for_prompt
from src.integration.prompt_builder import SYSTEM_PROMPT, build_user_prompt
from src.engine.llm_client import call_groq
from src.engine.response_parser import parse_llm_response

# ── 7.3 Logging & Monitoring Setup ────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("backend.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global DataFrame to hold our data
clean_df = pd.DataFrame()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global clean_df
    logger.info("Loading and preprocessing dataset on startup...")
    try:
        clean_df = load_raw_dataset()
        logger.info(f"Dataset loaded successfully. {len(clean_df)} records available.")
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}", exc_info=True)
        # We don't raise RuntimeError here so the server can still start and return 503s
        # instead of crashing outright, though raising is also an option.
    yield
    # Shutdown logic if any
    clean_df = pd.DataFrame()
    logger.info("Application shutdown.")

app = FastAPI(
    title="Zomato Recommendation API",
    description="API for recommending restaurants using Groq LLM.",
    version="1.0.0",
    lifespan=lifespan
)

# ── Middleware ────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for Vercel integration
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
    return response

# ── 7.1 Global Exception Handlers ─────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected internal server error occurred. Please check the logs."}
    )

# ── 7.2 Request Validation Models ─────────────────────────────────────
class RecommendationRequest(BaseModel):
    location: str = Field(default="any", description="City or location name")
    budget: str = Field(default="any", description="Budget tier")
    cuisine: str = Field(default="any", description="Preferred cuisine")
    min_rating: float = Field(default=1.0, ge=1.0, le=5.0, description="Minimum rating between 1.0 and 5.0")
    additional_prefs: str = Field(default="", description="Any free-form additional preferences")

@app.post("/api/recommend")
async def recommend_restaurants(req: RecommendationRequest):
    if clean_df is None or clean_df.empty:
        logger.warning("Recommendation requested but dataset is not loaded.")
        raise HTTPException(status_code=503, detail="Dataset not loaded or is empty. Please check server logs.")
    
    # 1. Map to internal model
    prefs = UserPreference(
        location=req.location.lower(),
        budget=req.budget.lower(),
        cuisine=req.cuisine.lower(),
        min_rating=req.min_rating,
        additional_prefs=req.additional_prefs
    )

    # 2. Filter data
    filtered_df, relaxed_filters = filter_with_fallback(clean_df, prefs)
    
    if filtered_df.empty:
        logger.info("No restaurants found matching criteria. Returning empty results.")
        return {
            "recommendations": [],
            "summary": "No restaurants found matching your criteria.",
            "relaxed_filters": relaxed_filters
        }
    
    # 3. Format & Build Prompt
    formatted_data = format_restaurants_for_prompt(filtered_df)
    user_prompt = build_user_prompt(formatted_data, prefs)
    
    # 4. Call LLM
    try:
        raw_response = call_groq(SYSTEM_PROMPT, user_prompt)
    except Exception as e:
        logger.error(f"LLM API Error: {e}", exc_info=True)
        # 502 Bad Gateway is appropriate for upstream API failure
        raise HTTPException(status_code=502, detail=f"LLM upstream request failed: {str(e)}")
    
    # 5. Parse Response
    rec_list = parse_llm_response(raw_response)
    
    return {
        "recommendations": rec_list.recommendations,
        "summary": rec_list.summary,
        "relaxed_filters": relaxed_filters
    }

# ── 8.1 Serve Frontend ────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")

@app.get("/{filename}")
async def serve_files(filename: str):
    import os
    file_path = os.path.join("frontend", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

