import re

file_path = "docs/implementation-plan.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace Table of Contents
old_toc = """## Table of Contents

1. [Project Summary](#1-project-summary)
2. [Prerequisites & Environment Setup](#2-prerequisites--environment-setup)
3. [Phase Overview](#3-phase-overview)
4. [Phase 1 — Project Scaffolding & Environment](#4-phase-1--project-scaffolding--environment)
5. [Phase 2 — Data Ingestion & Preprocessing](#5-phase-2--data-ingestion--preprocessing)
6. [Phase 3 — User Input Layer](#6-phase-3--user-input-layer)
7. [Phase 4 — Integration & Filtering Layer](#7-phase-4--integration--filtering-layer)
8. [Phase 5 — Groq LLM Recommendation Engine](#8-phase-5--groq-llm-recommendation-engine)
9. [Phase 6 — Output Display Layer](#9-phase-6--output-display-layer)
10. [Phase 7 — Pipeline Orchestration & Integration Testing](#10-phase-7--pipeline-orchestration--integration-testing)
11. [Phase 8 — Error Handling & Edge Case Hardening](#11-phase-8--error-handling--edge-case-hardening)
12. [Phase 9 — (Optional) Web Interface with Streamlit](#12-phase-9--optional-web-interface-with-streamlit)
13. [Milestone Checklist](#13-milestone-checklist)
14. [Risk Register](#14-risk-register)"""

new_toc = """## Table of Contents

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
14. [Risk Register](#14-risk-register)"""

content = content.replace(old_toc, new_toc)

# 2. Replace Project Summary
old_summary = """## 1. Project Summary

This plan implements the pipeline defined in `architecture.md` across **2 main phases** (Backend and Frontend). Each step produces a runnable, testable deliverable so progress can be validated.

```
Phase 1: Backend
Scaffold ──► Ingest ──► Input ──► Filter ──► LLM ──► CLI Output ──► Orchestrate ──► Harden
   │
   └──► Phase 2: Frontend
        Vite/React Setup ──► Design System ──► Components ──► Integration
```"""

new_summary = """## 1. Project Summary

This plan implements the pipeline defined in `architecture.md` across **9 distinct phases**, culminating in a high-quality frontend web application. Each phase produces a runnable, testable deliverable so progress can be validated.

```
Phases 1-5: Backend Core Data & Engine
Phase 6-7: Backend Orchestration & Hardening
Phase 8-9: Premium Frontend Web Application
```"""

content = content.replace(old_summary, new_summary)

# 3. Replace Phase Overview
old_overview = """## 3. Phase Overview

### Phase 1: Backend Development
| Step | Name | Key Deliverable | Estimated Effort |
|------|------|-----------------|-----------------|
| **1.1** | Project Scaffolding & Environment | Working project structure, virtual env, dependencies installed | ~30 min |
| **1.2** | Data Ingestion & Preprocessing | Clean pandas DataFrame from Hugging Face dataset | ~1–2 hrs |
| **1.3** | User Input Layer | Validated `UserPreference` object from CLI input | ~1 hr |
| **1.4** | Integration & Filtering Layer | Filtered restaurant DataFrame from user preferences | ~1–2 hrs |
| **1.5** | Groq LLM Recommendation Engine | Ranked + explained recommendations from Groq API | ~2–3 hrs |
| **1.6** | Output Display Layer | Formatted CLI recommendation cards | ~1 hr |
| **1.7** | Pipeline Orchestration | Full end-to-end working system via `main.py` | ~1–2 hrs |
| **1.8** | Error Handling & Hardening | Robust error recovery for all failure scenarios | ~1–2 hrs |

### Phase 2: Frontend Development
| Step | Name | Key Deliverable | Estimated Effort |
|------|------|-----------------|-----------------|
| **2.1** | Web Application Scaffolding | Vite/React app initialized, routing set up | ~1 hr |
| **2.2** | Core Design System | Global CSS, themes, variables, animations | ~1–2 hrs |
| **2.3** | Component Development | Search bar, Recommendation cards, skeletons | ~2–3 hrs |
| **2.4** | API Integration & Polish | Frontend calling backend API, final UI polish | ~2 hrs |"""

new_overview = """## 3. Phase Overview

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
| **9** | Frontend Components & Integration | Search bar, Recommendation cards, API integration, and final UI polish | ~3–4 hrs |"""

content = content.replace(old_overview, new_overview)

# 4. Fix headers for Phases 1-5
content = content.replace("## 4. Phase 1: Backend Development\n\n### Step 1.1 — Project Scaffolding & Environment", "## 4. Phase 1 — Project Scaffolding & Environment")
content = content.replace("### ✅ Step 1.1 Deliverable", "### ✅ Phase 1 Deliverable")

content = content.replace("### Step 1.2 — Data Ingestion & Preprocessing", "## 5. Phase 2 — Data Ingestion & Preprocessing")
content = content.replace("### ✅ Step 1.2 Deliverable", "### ✅ Phase 2 Deliverable")

content = content.replace("### Step 1.3 — User Input Layer", "## 6. Phase 3 — User Input Layer")
content = content.replace("### ✅ Step 1.3 Deliverable", "### ✅ Phase 3 Deliverable")

content = content.replace("### Step 1.4 — Integration & Filtering Layer", "## 7. Phase 4 — Integration & Filtering Layer")
content = content.replace("### ✅ Step 1.4 Deliverable", "### ✅ Phase 4 Deliverable")

content = content.replace("### Step 1.5 — Groq LLM Recommendation Engine", "## 8. Phase 5 — Groq LLM Recommendation Engine")
content = content.replace("### ✅ Step 1.5 Deliverable", "### ✅ Phase 5 Deliverable")

# 5. Replace everything from "### Step 1.6 — Output Display Layer" down to Risk Register
new_phases_6_9 = """## 9. Phase 6 — Backend Pipeline Orchestration & API

### Goal
Wire all layers together and expose the backend logic via a REST API (using FastAPI or Flask) so the frontend can interact with it.

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

## 14. Risk Register"""

start_idx = content.find("### Step 1.6 — Output Display Layer")
end_idx = content.find("## 7. Risk Register")

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_phases_6_9 + content[end_idx + len("## 7. Risk Register"):]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Replacement complete.")
