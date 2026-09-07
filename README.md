# SentinalVision — End-to-End AI Surveillance & Threat Detection System

## Problem Statement

Security monitoring traditionally relies on human operators watching multiple video feeds simultaneously, which is error-prone, fatiguing, and doesn't scale. This project builds a **prototype AI-powered surveillance system** that automatically processes video streams, detects objects of interest, classifies predefined visual threat categories, and generates configurable alerts for human review.

**This is a decision-support prototype, not an autonomous security system.**

---

## Objectives

1. Build a complete end-to-end AI/ML pipeline: video → frames → detection → classification → alerts → API → dashboard
2. Demonstrate practical computer vision: OpenCV, YOLO object detection, CNN transfer learning
3. Implement production-grade backend: FastAPI, SQLAlchemy, authentication, monitoring
4. Build a professional frontend: React, TypeScript, Tailwind CSS, real-time updates
5. Containerize with Docker for reproducible deployment
6. Document thoroughly for final-year project presentation and technical interviews

---

## Features

| Category | Features |
|----------|----------|
| **Video Processing** | Upload validation, frame extraction, FPS handling, resolution handling |
| **Object Detection** | YOLOv8 inference, bounding boxes, confidence scores, class labels |
| **Threat Classification** | CNN/Transfer Learning on detected regions, predefined visual categories |
| **Alert System** | Configurable thresholds, severity levels, human-verification workflow |
| **Backend API** | RESTful endpoints, JWT auth, analysis history, statistics |
| **Frontend Dashboard** | Upload, processing status, annotated video, charts, history |
| **Monitoring** | Structured logs, inference metrics, processing time, health checks |
| **Deployment** | Docker Compose, environment configuration, GPU/CPU support |

---

## Technology Stack

### Backend
- **Python 3.11+**
- **FastAPI** — Modern async web framework
- **Pydantic** — Data validation & serialization
- **SQLAlchemy** — ORM with SQLite (dev) / PostgreSQL (prod)
- **Uvicorn** — ASGI server
- **PyTest** — Testing

### AI/ML
- **PyTorch** — Deep learning framework
- **Ultralytics YOLOv8** — Object detection
- **torchvision** — Pretrained CNN models (ResNet, MobileNet, EfficientNet)
- **OpenCV** — Video/frame processing
- **scikit-learn** — Metrics, preprocessing
- **Albumentations** — Data augmentation

### Frontend
- **React 18 + TypeScript**
- **Vite** — Build tool
- **Tailwind CSS** — Utility-first styling
- **Recharts** — Data visualization
- **Axios** — API client

### Infrastructure
- **Docker & Docker Compose**
- **GitHub Actions** (basic CI)
- **Structured logging** (JSON format)

---

## Architecture Overview

```
┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│   Video      │────▶│  Frame        │────▶│  Preprocess  │
│   Upload     │     │  Extraction   │     │  (resize,    │
│   / Webcam   │     │  (OpenCV)     │     │   normalize) │
└──────────────┘     └───────────────┘     └──────┬───────┘
                                                   │
                                    ┌──────────────┘
                                    ▼
                           ┌──────────────────┐
                           │  YOLO Detection  │  ← "Where are objects?"
                           │  (bounding box)  │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │  Crop Regions    │
                           │  of Interest     │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │  CNN Classifier  │  ← "What category?"
                           │  (Transfer       │
                           │   Learning)      │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │  Confidence +    │
                           │  Alert Rules     │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │  FastAPI + DB    │
                           └────────┬─────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
             ┌────────────┐  ┌────────────┐  ┌────────────┐
             │  Dashboard │  │  Logs/     │  │  Model     │
             │  (React)   │  │  Metrics   │  │  Version   │
             └────────────┘  └────────────┘  └────────────┘
```

---

## Responsible AI Limitations

### This System DOES NOT:
- ❌ Identify or recognize specific individuals (no facial recognition)
- ❌ Predict criminal intent or future behavior
- ❌ Determine guilt or innocence
- ❌ Guarantee security or safety
- ❌ Replace trained security personnel
- ❌ Make autonomous decisions without human verification

### This System DOES:
- ✅ Detect predefined visual patterns in video frames
- ✅ Classify cropped regions into configured categories
- ✅ Generate alerts with confidence scores
- ✅ Flag content for **human operator review**
- ✅ Provide decision-support data

### Terminology Used
| Instead of... | We Say... |
|---------------|-----------|
| "Threat detected" | "Potential threat indicator" |
| "Suspicious person" | "Person detected in configured zone" |
| "Crime detected" | "Visual pattern matching configured category" |
| "Alert triggered" | "Configured condition satisfied — requires verification" |

---

## Development Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| 0 | Project Planning & Documentation | 🟢 **Current** |
| 1 | Backend Foundation (FastAPI, config, health) | ⏳ |
| 2 | Frontend Foundation (React, Vite, Tailwind) | ⏳ |
| 3 | Video Stream Processing (upload, frames) | ⏳ |
| 4 | Computer Vision Fundamentals (OpenCV lab) | ⏳ |
| 5 | YOLO Object Detection | ⏳ |
| 6 | **Define Classification Task** (dataset, classes) | ⏳ |
| 7 | CNN / Transfer Learning Classifier | ⏳ |
| 8 | Model Evaluation | ⏳ |
| 9 | Combine YOLO + Classifier | ⏳ |
| 10 | Alert Generation | ⏳ |
| 11 | Backend AI Integration | ⏳ |
| 12 | Database & Analysis History | ⏳ |
| 13 | Dashboard (real data) | ⏳ |
| 14 | Authentication & Security | ⏳ |
| 15 | Monitoring & Logs | ⏳ |
| 16 | Webcam / Live Monitoring | ⏳ |
| 17 | Docker Deployment | ⏳ |
| 18 | Testing & Final Evaluation | ⏳ |
| 19 | Documentation & Viva Prep | ⏳ |

---

## Folder Structure

```
SentinalVision/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI routes
│   │   ├── core/          # Config, security, logging
│   │   ├── db/            # SQLAlchemy models, session
│   │   ├── models/        # Pydantic schemas
│   │   ├── services/      # Business logic (AI pipeline, video, alerts)
│   │   └── main.py        # App entry point
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/      # API client
│   │   ├── hooks/
│   │   └── types/
│   ├── package.json
│   └── Dockerfile
├── ml/
│   ├── yolo/              # YOLO inference code
│   ├── classifier/        # CNN training/inference
│   ├── data/              # Dataset (not in git)
│   ├── experiments/       # Notebooks, CV fundamentals
│   └── models/            # Saved model weights
├── docker-compose.yml
├── .env.example
├── README.md
└── .gitignore
```

---

## Database Design

```sql
-- Core entities
User
  - id (PK)
  - email (unique)
  - password_hash
  - created_at

Analysis
  - id (PK)
  - user_id (FK)
  - filename, file_size, duration, fps
  - status (pending/processing/completed/failed)
  - model_version_id (FK)
  - created_at, completed_at

Detection
  - id (PK)
  - analysis_id (FK)
  - frame_number, timestamp
  - class_name, confidence
  - bbox_x1, bbox_y1, bbox_x2, bbox_y2

ClassificationResult
  - id (PK)
  - detection_id (FK)
  - class_name, confidence
  - model_version

Alert
  - id (PK)
  - analysis_id (FK)
  - severity (info/warning/critical)
  - alert_type, message
  - confidence, acknowledged, acknowledged_at

ModelVersion
  - id (PK)
  - name, version, path
  - yolo_version, classifier_version
  - metrics_json, created_at
```

---

## API Design

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/auth/register` | Register user |
| POST | `/api/v1/auth/login` | Login, return JWT |
| POST | `/api/v1/analyses` | Upload video, create analysis |
| GET | `/api/v1/analyses` | List analyses (paginated) |
| GET | `/api/v1/analyses/{id}` | Get analysis status |
| GET | `/api/v1/analyses/{id}/results` | Get detections + classifications |
| GET | `/api/v1/analyses/{id}/statistics` | Aggregated statistics |
| GET | `/api/v1/analyses/{id}/alerts` | Alerts for analysis |
| GET | `/api/v1/models/versions` | List model versions |

---

## GitHub Workflow

1. **One commit per phase** — no giant commits
2. **Meaningful messages**: `feat: add YOLO inference service`
3. **Verify before commit**: code runs, tests pass
4. **Push after each phase** to GitHub

---

## Getting Started (After Phase 17)

```bash
# Clone
git clone <your-repo-url>
cd SentinalVision

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start with Docker
docker compose up --build

# Access
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## License

This is a capstone project for educational purposes.

---

## Acknowledgments

- Ultralytics for YOLOv8
- PyTorch team for torchvision models
- FastAPI, React, and all open-source contributors