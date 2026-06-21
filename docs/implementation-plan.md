# Implementation Plan: AI-Powered Restaurant Recommendation System (Zomato Use Case)

> **Version:** 1.0  
> **Last Updated:** 2026-06-20  
> **Reference:** [architecture.md](./architecture.md) | [context.md](./context.md)  
> **LLM Provider:** Groq (via `groq` Python SDK)  
> **Dataset:** [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)

---

## Table of Contents

1. [Project Summary](#1-project-summary)
2. [Prerequisites & Environment Setup](#2-prerequisites--environment-setup)
3. [Phase Overview](#3-phase-overview)
4. [Phase 1 — Project Scaffolding & Environment](#4-phase-1--project-scaffolding--environment)
5. [Phase 2 — Data Ingestion & Preprocessing](#5-phase-2--data-ingestion--preprocessing)
6. [Phase 3 — User Input Layer](#6-phase-3--user-input-layer)
7. [Phase 4 — Integration & Filtering Layer](#7-phase-4--integration--filtering-layer)
8. [Phase 5 — Groq LLM Recommendation Engine](#8-phase-5--groq-llm-recommendation-engine)
9. [Phase 6 — Backend Pipeline Orchestration & API](#9-phase-6--backend-pipeline-orchestration--api)
10. [Phase 7 — Backend Error Handling & Edge Case Hardening](#10-phase-7--backend-error-handling--edge-case-hardening)
11. [Phase 8 — Frontend Web App Scaffolding & Core Design](#11-phase-8--frontend-web-app-scaffolding--core-design)
12. [Phase 9 — Frontend Component Development & Integration](#12-phase-9--frontend-component-development--integration)
13. [Milestone Checklist](#13-milestone-checklist)
14. [Risk Register](#14-risk-register)

---

## 1. Project Summary

This plan implements the pipeline defined in `architecture.md` across **9 distinct phases**, culminating in a high-quality frontend web application. Each phase produces a runnable, testable deliverable so progress can be validated.

```
Phases 1-5: Backend Core Data & Engine
Phase 6-7: Backend Orchestration & Hardening
Phase 8-9: Premium Frontend Web Application
```

---

## 2. Prerequisites & Environment Setup

Before starting Phase 1, ensure the following are available on your machine:

| Requirement | Version / Notes |
|-------------|----------------|
| **Python** | 3.10 or higher |
| **pip** | Latest (`pip install --upgrade pip`) |
| **Groq Account** | Sign up at [console.groq.com](https://console.groq.com) and generate an API key |
| **Groq API Key** | Store as `GROQ_API_KEY` in a `.env` file (never commit to Git) |
| **Git** | For version control |
| **VS Code / IDE** | Recommended for development |

---

## 3. Phase Overview

| Phase | Name | Key Deliverable | Estimated Effort |
|-------|------|-----------------|-----------------|
| **1** | Project Scaffolding & Environment | Working project structure, virtual env, dependencies installed | ~30 min |
| **2** | Data Ingestion & Preprocessing | Clean pandas DataFrame from Hugging Face dataset | ~1–2 hrs |
| **3** | User Input Layer | Validated `UserPreference` object from CLI input | ~1 hr |
| **4** | Integration & Filtering Layer | Filtered restaurant DataFrame from user preferences | ~1–2 hrs |
| **5** | Groq LLM Recommendation Engine | Ranked + explained recommendations from Groq API | ~2–3 hrs |
| **6** | Backend Pipeline Orchestration & API | Full end-to-end working backend system exposed via REST API | ~1–2 hrs |
| **7** | Backend Error Handling & Hardening | Robust error recovery for all failure scenarios | ~1–2 hrs |
| **8** | Frontend Web App Scaffolding & Design | Vite/React app initialized, routing, and premium CSS design system | ~2 hrs |
| **9** | Frontend Components & Integration | Search bar, Recommendation cards, API integration, and final UI polish | ~3–4 hrs |

---

## 4. Phase 1 — Project Scaffolding & Environment

### Goal
Set up the full directory structure, virtual environment, and all project dependencies.

### Steps

#### 1.1 — Create the Directory Structure

Create the following folder layout inside your project root:

```
zomato-recommendation-system/
├── docs/                        # ← Already exists
├── src/
│   ├── __init__.py
│   ├── ingestion/
│   │   └── __init__.py
│   ├── input/
│   │   └── __init__.py
│   ├── integration/
│   │   └── __init__.py
│   ├── engine/
│   │   └── __init__.py
│   └── output/
│       └── __init__.py
├── tests/
├── notebooks/
├── .env                         # ← CREATE — never commit
├── .env.example                 # ← CREATE — commit this
├── .gitignore
├── requirements.txt
└── README.md
```

#### 1.2 — Create and Activate a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

#### 1.3 — Create `requirements.txt`

```txt
# Data
datasets==2.19.0
pandas==2.2.2
numpy==1.26.4

# LLM
groq==0.9.0

# Config
python-dotenv==1.0.1

# CLI Output
rich==13.7.1

# Optional: Web UI
streamlit==1.35.0
```

#### 1.4 — Install Dependencies

```bash
pip install -r requirements.txt
```

#### 1.5 — Create `.env` and `.env.example`

**`.env`** (not committed to Git):
```
GROQ_API_KEY=your_actual_groq_api_key_here
GROQ_MODEL=llama3-8b-8192
```

**`.env.example`** (committed to Git):
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-8b-8192
```

#### 1.6 — Create `.gitignore`

```
venv/
__pycache__/
*.pyc
.env
*.egg-info/
dist/
.DS_Store
```

### ✅ Phase 1 Deliverable
- Full project folder structure created
- Virtual environment active with all dependencies installed
- `.env` configured with `GROQ_API_KEY`

---

## 5. Phase 2 — Data Ingestion & Preprocessing

### Goal
Load the Zomato dataset from Hugging Face, clean it, normalize fields, and produce a ready-to-query pandas DataFrame.

### Architecture Reference
> **Layer 1 — Data Ingestion** (`src/ingestion/`)

### Steps

#### 2.1 — Implement `src/ingestion/loader.py`

```python
# src/ingestion/loader.py

from datasets import load_dataset
import pandas as pd

DATASET_NAME = "ManikaSaini/zomato-restaurant-recommendation"

def load_raw_dataset() -> pd.DataFrame:
    """Load the Zomato dataset from Hugging Face Hub."""
    dataset = load_dataset(DATASET_NAME, split="train")
    return dataset.to_pandas()
```

**Key fields to retain from the dataset:**
- `name` — Restaurant name
- `location` / `city` — Location / city
- `cuisines` — Cuisine types (comma-separated string)
- `cost` / `approx_cost(for two people)` — Cost for two
- `rate` / `rating` — Aggregate rating
- Any other available metadata

> **Note:** Inspect the dataset first in a notebook (`notebooks/exploration.ipynb`) to confirm exact column names before writing the preprocessor.

#### 2.2 — Implement `src/ingestion/preprocessor.py`

```python
# src/ingestion/preprocessor.py

import pandas as pd

BUDGET_TIERS = {
    "low":    (0,    500),
    "medium": (501,  1200),
    "high":   (1201, float("inf")),
}

def assign_budget_tier(cost: float) -> str:
    for tier, (low, high) in BUDGET_TIERS.items():
        if low <= cost <= high:
            return tier
    return "high"

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize the raw Zomato DataFrame."""

    # 1. Rename columns to standard names (adjust based on actual dataset columns)
    df = df.rename(columns={
        "name": "name",
        "location": "location",
        "cuisines": "cuisines",
        "approx_cost(for two people)": "cost_for_two",
        "rate": "rating",
    })

    # 2. Keep only required columns
    required_cols = ["name", "location", "cuisines", "cost_for_two", "rating"]
    df = df[[c for c in required_cols if c in df.columns]].copy()

    # 3. Drop rows with missing critical fields
    df.dropna(subset=["name", "location", "cuisines", "cost_for_two", "rating"], inplace=True)

    # 4. Clean cost_for_two — remove commas, cast to float
    df["cost_for_two"] = (
        df["cost_for_two"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df = df[df["cost_for_two"].str.match(r"^\d+(\.\d+)?$")]
    df["cost_for_two"] = df["cost_for_two"].astype(float)

    # 5. Clean rating — handle "NEW", "-", etc.
    df["rating"] = (
        df["rating"]
        .astype(str)
        .str.extract(r"(\d+\.\d+|\d+)")[0]
        .astype(float)
    )
    df = df[(df["rating"] >= 1.0) & (df["rating"] <= 5.0)]

    # 6. Normalize text fields
    df["location"] = df["location"].str.strip().str.lower()
    df["cuisines"] = df["cuisines"].str.strip().str.lower()
    df["name"] = df["name"].str.strip()

    # 7. Add budget tier
    df["budget_tier"] = df["cost_for_two"].apply(assign_budget_tier)

    # 8. Reset index
    df.reset_index(drop=True, inplace=True)

    return df
```

#### 2.3 — Validate in Notebook

Create `notebooks/exploration.ipynb` and run:
```python
from src.ingestion.loader import load_raw_dataset
from src.ingestion.preprocessor import preprocess

raw_df = load_raw_dataset()
print(raw_df.columns.tolist())   # Inspect actual column names
print(raw_df.head())

clean_df = preprocess(raw_df)
print(clean_df.dtypes)
print(clean_df.shape)
print(clean_df["budget_tier"].value_counts())
print(clean_df["location"].value_counts().head(10))
```

#### 2.4 — Write Unit Test `tests/test_preprocessor.py`

```python
import pandas as pd
from src.ingestion.preprocessor import preprocess, assign_budget_tier

def test_budget_tier_assignment():
    assert assign_budget_tier(300)  == "low"
    assert assign_budget_tier(800)  == "medium"
    assert assign_budget_tier(2000) == "high"

def test_preprocess_drops_nulls():
    raw = pd.DataFrame({
        "name": ["A", None],
        "location": ["delhi", "mumbai"],
        "cuisines": ["north indian", "chinese"],
        "approx_cost(for two people)": ["500", "800"],
        "rate": ["4.1/5", "3.8/5"],
    })
    result = preprocess(raw)
    assert len(result) == 1
```

### ✅ Phase 2 Deliverable
- `loader.py` loads raw dataset from Hugging Face
- `preprocessor.py` produces a clean DataFrame with: `name`, `location`, `cuisines`, `cost_for_two`, `rating`, `budget_tier`
- Notebook validates data shape and distribution
- Unit tests pass

---

## 6. Phase 3 — User Input Layer

### Goal
Collect user preferences from the CLI, validate them, and return a structured `UserPreference` object.

### Architecture Reference
> **Layer 2 — User Input** (`src/input/`)

### Steps

#### 3.1 — Implement `src/input/models.py`

```python
# src/input/models.py

from dataclasses import dataclass, field

@dataclass
class UserPreference:
    location: str
    budget: str            # "low" | "medium" | "high"
    cuisine: str
    min_rating: float      # e.g., 3.5
    additional_prefs: str = field(default="")  # Optional free-form text
```

#### 3.2 — Implement `src/input/validator.py`

```python
# src/input/validator.py

from src.input.models import UserPreference

VALID_BUDGETS = {"low", "medium", "high"}

def collect_and_validate() -> UserPreference:
    """Interactively collect and validate user preferences from CLI."""

    print("\n🍽️  Welcome to the Zomato AI Restaurant Recommender!\n")

    location = input("📍 Enter your location (e.g., Delhi, Bangalore): ").strip()
    if not location:
        raise ValueError("Location cannot be empty.")

    budget = input("💰 Enter budget [low / medium / high]: ").strip().lower()
    if budget not in VALID_BUDGETS:
        raise ValueError(f"Budget must be one of: {', '.join(VALID_BUDGETS)}")

    cuisine = input("🍜 Enter preferred cuisine (e.g., North Indian, Chinese): ").strip()
    if not cuisine:
        raise ValueError("Cuisine cannot be empty.")

    rating_str = input("⭐ Minimum rating (1.0 – 5.0, e.g., 3.5): ").strip()
    try:
        min_rating = float(rating_str)
        if not (1.0 <= min_rating <= 5.0):
            raise ValueError()
    except ValueError:
        raise ValueError("Rating must be a number between 1.0 and 5.0.")

    additional_prefs = input(
        "✨ Any additional preferences? (e.g., family-friendly, rooftop) [Press Enter to skip]: "
    ).strip()

    return UserPreference(
        location=location.lower(),
        budget=budget,
        cuisine=cuisine.lower(),
        min_rating=min_rating,
        additional_prefs=additional_prefs,
    )
```

#### 3.3 — Write Unit Test `tests/test_validator.py`

```python
from src.input.models import UserPreference

def test_user_preference_creation():
    pref = UserPreference(
        location="delhi",
        budget="medium",
        cuisine="north indian",
        min_rating=4.0,
        additional_prefs="family-friendly"
    )
    assert pref.location == "delhi"
    assert pref.budget == "medium"
    assert pref.min_rating == 4.0
```

### ✅ Phase 3 Deliverable
- `UserPreference` dataclass defined
- CLI input collection with validation for all 5 fields
- Descriptive error messages for invalid inputs
- Unit tests pass

---

## 7. Phase 4 — Integration & Filtering Layer

### Goal
Filter the cleaned DataFrame based on `UserPreference`, format the results for LLM consumption, and construct the final Groq prompt.

### Architecture Reference
> **Layer 3 — Integration** (`src/integration/`)

### Steps

#### 4.1 — Implement `src/integration/filter_engine.py`

```python
# src/integration/filter_engine.py

import pandas as pd
from src.input.models import UserPreference

MAX_RESULTS = 15  # Maximum candidates sent to LLM

def filter_restaurants(df: pd.DataFrame, prefs: UserPreference) -> pd.DataFrame:
    """Apply sequential AND-filters based on user preferences."""

    filtered = df.copy()

    # Filter 1: Location (partial match)
    filtered = filtered[filtered["location"].str.contains(prefs.location, case=False, na=False)]

    # Filter 2: Cuisine (partial match)
    filtered = filtered[filtered["cuisines"].str.contains(prefs.cuisine, case=False, na=False)]

    # Filter 3: Budget tier (exact match)
    filtered = filtered[filtered["budget_tier"] == prefs.budget]

    # Filter 4: Minimum rating
    filtered = filtered[filtered["rating"] >= prefs.min_rating]

    # Sort by rating descending; take top-N
    filtered = filtered.sort_values("rating", ascending=False).head(MAX_RESULTS)

    return filtered.reset_index(drop=True)


def filter_with_fallback(df: pd.DataFrame, prefs: UserPreference) -> tuple[pd.DataFrame, list[str]]:
    """
    Try strict filtering first. If < 3 results, progressively relax lower-priority filters.
    Returns: (filtered_df, list of relaxed filter names)
    """
    relaxed = []
    result = filter_restaurants(df, prefs)

    if len(result) < 3:
        # Relax cuisine filter
        relaxed.append("cuisine")
        relaxed_prefs = UserPreference(
            location=prefs.location,
            budget=prefs.budget,
            cuisine="",          # Remove cuisine filter
            min_rating=prefs.min_rating,
            additional_prefs=prefs.additional_prefs,
        )
        result = filter_restaurants(df, relaxed_prefs)

    if len(result) < 3:
        # Relax budget filter
        relaxed.append("budget")
        filtered = df[df["location"].str.contains(prefs.location, case=False, na=False)]
        filtered = filtered[filtered["rating"] >= prefs.min_rating]
        result = filtered.sort_values("rating", ascending=False).head(MAX_RESULTS).reset_index(drop=True)

    return result, relaxed
```

#### 4.2 — Implement `src/integration/formatter.py`

```python
# src/integration/formatter.py

import pandas as pd

def format_restaurants_for_prompt(df: pd.DataFrame) -> str:
    """Convert filtered DataFrame rows into a structured text block for LLM."""

    if df.empty:
        return "No restaurants found matching the given criteria."

    lines = []
    for i, row in df.iterrows():
        lines.append(f"Restaurant {i + 1}:")
        lines.append(f"  Name:           {row['name']}")
        lines.append(f"  Cuisine:        {row['cuisines'].title()}")
        lines.append(f"  Location:       {row['location'].title()}")
        lines.append(f"  Rating:         {row['rating']} / 5.0")
        lines.append(f"  Cost (for 2):   ₹{int(row['cost_for_two'])} ({row['budget_tier'].capitalize()} budget)")
        lines.append("")  # Blank line between restaurants

    return "\n".join(lines)
```

#### 4.3 — Implement `src/integration/prompt_builder.py`

```python
# src/integration/prompt_builder.py

from src.input.models import UserPreference

SYSTEM_PROMPT = """You are an expert restaurant recommendation assistant.
Your task is to rank and explain restaurant suggestions based on a user's stated preferences.
Be concise, helpful, and personalized in your responses.
Always output results in the exact structured format specified — do not deviate from it."""


def build_user_prompt(formatted_restaurants: str, prefs: UserPreference) -> str:
    """Assemble the final user prompt for the Groq LLM."""

    additional = prefs.additional_prefs if prefs.additional_prefs else "None"

    return f"""The user is looking for a restaurant with the following preferences:
- Location:               {prefs.location.title()}
- Budget:                 {prefs.budget.capitalize()}
- Preferred Cuisine:      {prefs.cuisine.title()}
- Minimum Rating:         {prefs.min_rating}
- Additional Preferences: {additional}

Based on these preferences, here are the candidate restaurants retrieved from our database:

{formatted_restaurants}

Please:
1. Rank these restaurants from BEST to LEAST suitable for this user.
2. For each restaurant, provide a 2-3 sentence explanation of WHY it is a good (or less ideal) match.
3. Provide a brief 1-2 sentence overall summary of the top recommendation.

Format your response EXACTLY as follows (do not add any extra text outside this format):
---
Rank 1: [Restaurant Name]
Explanation: [Your explanation here]

Rank 2: [Restaurant Name]
Explanation: [Your explanation here]

(continue for all restaurants)
---
Overall Summary: [Brief summary of top pick]
"""
```

#### 4.4 — Write Unit Test `tests/test_filter_engine.py`

```python
import pandas as pd
from src.integration.filter_engine import filter_restaurants
from src.input.models import UserPreference

def make_test_df():
    return pd.DataFrame({
        "name": ["Spice Garden", "Pizza House", "Curry Point"],
        "location": ["delhi, connaught place", "mumbai, bandra", "delhi, lajpat nagar"],
        "cuisines": ["north indian", "italian", "north indian"],
        "cost_for_two": [600.0, 900.0, 400.0],
        "rating": [4.3, 4.1, 3.9],
        "budget_tier": ["medium", "medium", "low"],
    })

def test_filter_by_location():
    df = make_test_df()
    prefs = UserPreference(location="delhi", budget="medium", cuisine="north indian", min_rating=4.0)
    result = filter_restaurants(df, prefs)
    assert len(result) == 1
    assert result.iloc[0]["name"] == "Spice Garden"

def test_filter_returns_empty_when_no_match():
    df = make_test_df()
    prefs = UserPreference(location="kolkata", budget="low", cuisine="chinese", min_rating=4.5)
    result = filter_restaurants(df, prefs)
    assert result.empty
```

#### 4.5 — Write Unit Test `tests/test_prompt_builder.py`

```python
from src.integration.prompt_builder import build_user_prompt, SYSTEM_PROMPT
from src.input.models import UserPreference

def test_prompt_contains_preferences():
    prefs = UserPreference(location="delhi", budget="medium", cuisine="north indian", min_rating=4.0)
    prompt = build_user_prompt("Restaurant 1:\n  Name: Spice Garden\n", prefs)
    assert "Delhi" in prompt
    assert "Medium" in prompt
    assert "4.0" in prompt
    assert "Spice Garden" in prompt

def test_system_prompt_is_non_empty():
    assert len(SYSTEM_PROMPT) > 0
```

### ✅ Phase 4 Deliverable
- `filter_engine.py` correctly filters dataset with AND-chain + fallback relaxation
- `formatter.py` converts DataFrame rows to a readable text block
- `prompt_builder.py` assembles a complete, well-structured Groq prompt
- All unit tests pass

---

## 8. Phase 5 — Groq LLM Recommendation Engine

### Goal
Call the Groq API with the constructed prompt, parse the ranked + explained response, and return structured recommendation objects.

### Architecture Reference
> **Layer 4 — LLM Engine** (`src/engine/`)

### Steps

#### 5.1 — Implement `src/engine/llm_client.py`

```python
# src/engine/llm_client.py

import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds (doubles each retry)


def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY not found. Please set it in your .env file."
        )
    return Groq(api_key=api_key)


def call_groq(system_prompt: str, user_prompt: str) -> str:
    """
    Send prompt to Groq API and return the raw text response.
    Retries up to MAX_RETRIES times on failure.
    """
    client = get_groq_client()
    model = os.getenv("GROQ_MODEL", "llama3-8b-8192")

    delay = RETRY_DELAY
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=2048,
            )
            return response.choices[0].message.content

        except Exception as e:
            if attempt == MAX_RETRIES:
                raise RuntimeError(
                    f"Groq API call failed after {MAX_RETRIES} attempts: {e}"
                )
            print(f"⚠️  Groq API error (attempt {attempt}/{MAX_RETRIES}): {e}. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
```

#### 5.2 — Implement `src/engine/response_parser.py`

```python
# src/engine/response_parser.py

import re
from dataclasses import dataclass, field

@dataclass
class Recommendation:
    rank: int
    restaurant_name: str
    explanation: str

@dataclass
class RecommendationList:
    recommendations: list[Recommendation] = field(default_factory=list)
    summary: str = ""


def parse_llm_response(raw_response: str) -> RecommendationList:
    """
    Parse the structured LLM response into a RecommendationList.
    Expected format:
        Rank N: [Restaurant Name]
        Explanation: [text]
        ...
        Overall Summary: [text]
    """
    result = RecommendationList()

    # Extract overall summary
    summary_match = re.search(r"Overall Summary:\s*(.+?)(?:\n|$)", raw_response, re.IGNORECASE | re.DOTALL)
    if summary_match:
        result.summary = summary_match.group(1).strip()

    # Extract ranked entries
    rank_pattern = re.findall(
        r"Rank\s+(\d+):\s*(.+?)\nExplanation:\s*(.+?)(?=\n\nRank|\nOverall Summary|---|\Z)",
        raw_response,
        re.DOTALL | re.IGNORECASE,
    )

    for rank_str, name, explanation in rank_pattern:
        result.recommendations.append(
            Recommendation(
                rank=int(rank_str),
                restaurant_name=name.strip(),
                explanation=explanation.strip(),
            )
        )

    return result
```

#### 5.3 — Manual Integration Test (Groq API Smoke Test)

Create a scratch script `tests/test_groq_smoke.py`:

```python
# Run manually: python tests/test_groq_smoke.py
from src.engine.llm_client import call_groq
from src.integration.prompt_builder import SYSTEM_PROMPT

user_prompt = """The user wants a North Indian restaurant in Delhi with a medium budget and minimum rating 4.0.

Restaurant 1:
  Name: Spice Garden
  Cuisine: North Indian
  Rating: 4.3 / 5.0
  Cost: ₹800 (Medium budget)

Please rank and explain.

---
Rank 1: [Name]
Explanation: [text]
---
Overall Summary: [text]
"""

response = call_groq(SYSTEM_PROMPT, user_prompt)
print(response)
```

#### 5.4 — Write Unit Test `tests/test_response_parser.py`

```python
from src.engine.response_parser import parse_llm_response

SAMPLE_RESPONSE = """---
Rank 1: Spice Garden
Explanation: Spice Garden is an excellent match for your preferences. It serves authentic North Indian cuisine in Delhi and is well within the medium budget. The high rating of 4.3 confirms consistently great food and service.

Rank 2: Curry Point
Explanation: Curry Point offers good value North Indian food in Delhi. While the rating is slightly lower, it is a solid choice for budget-conscious diners.
---
Overall Summary: Spice Garden is the top pick, offering the best combination of cuisine quality, rating, and budget alignment."""

def test_parse_recommendations():
    result = parse_llm_response(SAMPLE_RESPONSE)
    assert len(result.recommendations) == 2
    assert result.recommendations[0].rank == 1
    assert result.recommendations[0].restaurant_name == "Spice Garden"
    assert "4.3" in result.recommendations[0].explanation

def test_parse_summary():
    result = parse_llm_response(SAMPLE_RESPONSE)
    assert "Spice Garden" in result.summary
```

### ✅ Phase 5 Deliverable
- `llm_client.py` calls Groq API with retry + exponential backoff
- `response_parser.py` extracts `Recommendation` objects from raw LLM response
- Smoke test confirms live Groq API connectivity
- Unit tests pass for parser

---

## 9. Phase 6 — Backend Pipeline Orchestration & API

### Goal
Wire all layers together and expose the backend logic via a REST API using FastAPI so the frontend can interact with it.

### Architecture Reference
> **Layer 5 — Output API & Orchestration**

### Steps

#### 6.1 — Implement `src/api/main.py`
Create a FastAPI application that serves endpoints for generating recommendations.
- Define request and response models using Pydantic.
- Expose a `POST /api/recommend` endpoint that accepts user preferences and returns the recommendation list.

#### 6.2 — Implement CORS & Middleware
Configure CORS to allow requests from the Vite frontend (typically `http://localhost:5173`).

#### 6.3 — API Testing
Run the server using `uvicorn` and verify the endpoints using Swagger UI (built into FastAPI) or Postman.

### ✅ Phase 6 Deliverable
- End-to-end backend pipeline orchestrated.
- FastAPI server running and exposing the `/api/recommend` endpoint.

---

## 10. Phase 7 — Backend Error Handling & Edge Case Hardening

### Goal
Add robust error handling for all failure scenarios on the backend API, ensuring safe and predictable responses.

### Steps

#### 7.1 — Global Exception Handlers
Add global exception handlers to the FastAPI app to catch and format:
- Dataset or model loading errors.
- External API timeouts (e.g., Groq API failures).
- Empty result sets.

#### 7.2 — Request Validation
Ensure strict validation of user inputs via Pydantic to avoid malformed data reaching the engine.

#### 7.3 — Logging & Monitoring
Add comprehensive logging for incoming API requests, errors, and fallback activations.

### ✅ Phase 7 Deliverable
- Resilient API that returns appropriate HTTP status codes (e.g., 400 for bad input, 502 for Groq timeout).
- Logging writing to `backend.log`.

---

## 11. Phase 8 — Frontend Web App Scaffolding & Core Design

### Goal
Initialize a premium frontend web application using Vite, React, and Vanilla CSS with a focus on modern, rich aesthetics.

### Steps

#### 8.1 — Web Application Scaffolding
Create a new Vite app with React:
```bash
npm create vite@latest frontend -- --template react
```
Set up the directory structure (`components`, `pages`, `styles`, `api`) and configure routing.

#### 8.2 — Core Design System
Establish a premium design aesthetic using Vanilla CSS (`index.css`):
- Define a rich color palette (e.g., vibrant primary colors, sleek dark mode).
- Integrate modern typography (e.g., Google Fonts: Inter or Outfit).
- Create utility classes for micro-animations, glassmorphism effects, and smooth hover transitions.

### ✅ Phase 8 Deliverable
- Running Vite dev server.
- Comprehensive `index.css` defining the design system.
- Basic routing configured for a `Home` page.

---

## 12. Phase 9 — Frontend Component Development & Integration

### Goal
Build beautiful, interactive React components and connect them to the backend API.

### Steps

#### 9.1 — Build Interactive Components
- **Search Hero Section**: Input fields with animated placeholders and focus effects for Location, Cuisine, Budget, and Rating.
- **Recommendation Cards**: Rich cards with hover lifts, glowing borders for Rank 1, and expandable AI explanations.
- **Loading States**: Engaging loading skeletons or spinner animations while waiting for the backend API.

#### 9.2 — API Integration & Polish
- Create API service functions (`api/recommendations.js`) to call the backend endpoint `POST /api/recommend`.
- Handle edge cases gracefully in the UI (e.g., "No results found" or network errors).
- Perform a final visual and performance review.

### ✅ Phase 9 Deliverable
- Fully functional end-to-end web application delivering AI recommendations with a WOW factor.

---

## 13. Milestone Checklist

```
Phase 1 — Project Scaffolding & Environment
  [ ] Directory structure created
  [ ] Virtual environment active
  [ ] requirements.txt installed
  [ ] .env configured with GROQ_API_KEY

Phase 2 — Data Ingestion & Preprocessing
  [ ] loader.py loads raw dataset from Hugging Face
  [ ] preprocessor.py produces clean DataFrame
  [ ] test_preprocessor.py passes

Phase 3 — User Input Layer
  [ ] UserPreference dataclass defined
  [ ] CLI input validation tested

Phase 4 — Integration & Filtering Layer
  [ ] filter_engine.py with AND-chain + fallback relaxation
  [ ] prompt_builder.py assembles complete Groq prompt
  [ ] test_filter_engine.py passes

Phase 5 — Groq LLM Recommendation Engine
  [ ] llm_client.py calls Groq with retry logic
  [ ] response_parser.py extracts RecommendationList
  [ ] test_response_parser.py passes

Phase 6 — Backend Pipeline Orchestration & API
  [ ] FastAPI app implemented
  [ ] /api/recommend endpoint exposed
  [ ] CORS configured

Phase 7 — Backend Error Handling & Hardening
  [ ] Global exception handlers added
  [ ] Logging implemented
  [ ] Fallback mechanisms tested

Phase 8 — Frontend Web App Scaffolding & Core Design
  [ ] Vite/React scaffolding and routing
  [ ] Premium design system (CSS) implemented

Phase 9 — Frontend Components & Integration
  [ ] Core components (Search, Cards) built
  [ ] API integration complete
  [ ] UI polish and animations added
```

## 14. Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|-----------|
| 1 | Hugging Face dataset column names differ from expected | Medium | High | Inspect columns in notebook (Phase 2.3) before writing preprocessor |
| 2 | Groq API rate limit hit during testing | Low | Medium | Use `llama3-8b-8192` (faster, cheaper); add retry + backoff |
| 3 | Very sparse dataset for some cities / cuisines | High | Medium | Implement filter fallback relaxation (Phase 4.1) |
| 4 | LLM response format deviates from expected | Medium | Medium | Robust regex parser + raw response fallback (Phase 5.2) |
| 5 | Cost-for-two values have inconsistent formatting | High | High | Defensive preprocessing with regex cleaning (Phase 2.2 step 4) |
| 6 | Context window exceeded (too many restaurants in prompt) | Low | Medium | Hard cap at `MAX_RESULTS = 15` candidates sent to LLM |
| 7 | `.env` file accidentally committed to Git | Low | Critical | Verify `.gitignore` includes `.env` before first commit |

---

*Generated from [architecture.md](./architecture.md) and [context.md](./context.md)*
