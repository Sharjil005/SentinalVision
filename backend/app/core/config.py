"""
SentinalVision — Configuration Management
"""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SentinalVision"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"

    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    DATABASE_URL: str = "sqlite:///./sentinalvision.db"

    SECRET_KEY: str = "change-me-in-production-min-32-characters-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 500
    ALLOWED_VIDEO_TYPES: List[str] = [
        "video/mp4",
        "video/x-msvideo",
        "video/quicktime",
        "video/x-matroska",
    ]

    YOLO_MODEL_PATH: str = "./ml/models/yolov8n.pt"
    YOLO_CONFIDENCE_THRESHOLD: float = 0.25
    YOLO_IOU_THRESHOLD: float = 0.45
    YOLO_DEVICE: str = "cpu"

    CLASSIFIER_MODEL_PATH: str = "./ml/models/classifier_best.pt"
    CLASSIFIER_DEVICE: str = "cpu"
    CLASSIFIER_CONFIDENCE_THRESHOLD: float = 0.5

    FRAME_SAMPLE_RATE: int = 1
    MAX_FRAMES_PER_VIDEO: int = 1000
    OUTPUT_VIDEO_FPS: int = 10

    ALERT_CONFIDENCE_THRESHOLD: float = 0.7
    ALERT_COOLDOWN_SECONDS: int = 30

    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()