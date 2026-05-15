# 🛡️ ATSParser: AI-Driven Hiring Intelligence

A high-performance, production-ready ATS Resume Parsing and Scoring system built with **FastAPI**, **Next.js 15**, and **NLP (spaCy + SentenceTransformers)**.

## ✨ Key Features
- **God-Mode Strictness:** Advanced profession matching that automatically detects and filters irrelevant candidates (e.g., Designer vs. Software Engineer) with zero-tolerance scoring.
- **Deep Skill Gap Analysis:** Semantic skill extraction using spaCy, identifying exactly what's missing from a resume.
- **Live Match Analytics:** A beautiful, responsive dashboard with real-time stats on hiring trends and candidate quality.
- **Async Pipeline:** Heavy NLP processing handled by Celery background workers for a seamless user experience.
- **Top-to-Bottom PDF Extraction:** Intelligent text block sorting ensures candidate contact info is never missed.

## 🚀 Quick Start

### 1. Start the Backend (FastAPI)
```powershell
uvicorn backend.main:app --reload --port 8000
```
*Verify at `http://localhost:8000/health`*

### 2. Start the Celery Brain
```powershell
# In a new terminal
celery -A backend.tasks.celery_app worker --loglevel=info -P solo
```
*Note: Requires Redis running on localhost:6379.*

### 3. Start the UI (Next.js)
```bash
npm run dev
```
*Visit `http://localhost:3000`*

## 🛠️ Tech Stack
- **Frontend:** Next.js 15, Tailwind CSS 4, Framer Motion, Lucide Icons.
- **Backend:** FastAPI, SQLAlchemy (SQLite), Pydantic.
- **AI/NLP:** spaCy (NER & Pos-Tagging), SentenceTransformers (Cosine Similarity), Sklearn.
- **Infrastructure:** Celery, Redis, R2-Compatible Storage.

---
*Built for precision. Made for recruiters.*
