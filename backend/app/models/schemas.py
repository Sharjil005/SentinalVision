"""
Pydantic schemas for API request/response models.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from enum import Enum


# Enums
class AnalysisStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


# Base schemas
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# User schemas
class UserBase(BaseSchema):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseSchema):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime


class UserInDB(UserResponse):
    password_hash: str


# Auth schemas
class Token(BaseSchema):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseSchema):
    user_id: Optional[int] = None
    email: Optional[str] = None


class LoginRequest(BaseSchema):
    email: EmailStr
    password: str


class RegisterRequest(UserCreate):
    pass


# Model Version schemas
class ModelVersionBase(BaseSchema):
    name: str
    version: str
    yolo_model_path: Optional[str] = None
    classifier_model_path: Optional[str] = None
    yolo_version: Optional[str] = None
    classifier_version: Optional[str] = None
    metrics_json: Optional[str] = None


class ModelVersionCreate(ModelVersionBase):
    pass


class ModelVersionResponse(ModelVersionBase):
    id: int
    is_active: bool
    created_at: datetime


# Analysis schemas
class AnalysisBase(BaseSchema):
    filename: str
    original_filename: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    duration: Optional[float] = None
    fps: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    total_frames: Optional[int] = None
    frame_sample_rate: int = 1


class AnalysisCreate(AnalysisBase):
    pass


class AnalysisUpdate(BaseSchema):
    status: Optional[AnalysisStatus] = None
    processed_frames: Optional[int] = None
    error_message: Optional[str] = None
    output_video_path: Optional[str] = None
    processing_time_seconds: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class AnalysisResponse(AnalysisBase):
    id: int
    user_id: int
    model_version_id: Optional[int] = None
    status: AnalysisStatus
    processed_frames: int
    error_message: Optional[str] = None
    output_video_path: Optional[str] = None
    processing_time_seconds: Optional[float] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Nested relationships (optional, loaded on demand)
    user: Optional[UserResponse] = None
    model_version: Optional[ModelVersionResponse] = None


class AnalysisListResponse(BaseSchema):
    items: List[AnalysisResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# Detection schemas
class DetectionBase(BaseSchema):
    frame_number: int
    timestamp: float
    bbox_x1: float
    bbox_y1: float
    bbox_x2: float
    bbox_y2: float
    class_name: str
    class_id: int
    confidence: float


class DetectionCreate(DetectionBase):
    analysis_id: int


class DetectionResponse(DetectionBase):
    id: int
    analysis_id: int


# Classification schemas
class ClassificationResultBase(BaseSchema):
    frame_number: int
    timestamp: float
    class_name: str
    confidence: float
    all_probabilities: Optional[Dict[str, float]] = None
    model_version: Optional[str] = None


class ClassificationResultCreate(ClassificationResultBase):
    analysis_id: int
    detection_id: Optional[int] = None


class ClassificationResultResponse(ClassificationResultBase):
    id: int
    analysis_id: int
    detection_id: Optional[int] = None


# Alert schemas
class AlertBase(BaseSchema):
    alert_type: str
    severity: AlertSeverity
    message: str
    confidence: float
    frame_number: Optional[int] = None
    timestamp: Optional[float] = None
    detection_ids: Optional[List[int]] = None
    classification_ids: Optional[List[int]] = None
    rule_config: Optional[Dict[str, Any]] = None


class AlertCreate(AlertBase):
    analysis_id: int


class AlertUpdate(BaseSchema):
    acknowledged: Optional[bool] = None


class AlertResponse(AlertBase):
    id: int
    analysis_id: int
    acknowledged: bool
    acknowledged_by: Optional[int] = None
    acknowledged_at: Optional[datetime] = None
    created_at: datetime


# Statistics schemas
class AnalysisStatisticBase(BaseSchema):
    total_detections: int = 0
    unique_classes: int = 0
    detections_by_class: Dict[str, int] = {}
    total_classifications: int = 0
    classifications_by_class: Dict[str, int] = {}
    total_alerts: int = 0
    alerts_by_severity: Dict[str, int] = {}
    avg_detection_confidence: Optional[float] = None
    avg_classification_confidence: Optional[float] = None
    avg_inference_time_ms: Optional[float] = None


class AnalysisStatisticResponse(AnalysisStatisticBase):
    id: int
    analysis_id: int


# Combined response schemas
class AnalysisDetailResponse(AnalysisResponse):
    detections: List[DetectionResponse] = []
    classification_results: List[ClassificationResultResponse] = []
    alerts: List[AlertResponse] = []
    statistics: Optional[AnalysisStatisticResponse] = None


# Health check
class HealthResponse(BaseSchema):
    status: str
    service: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Pagination
class PaginationParams(BaseSchema):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def create(cls, items: List[Any], total: int, page: int, page_size: int) -> "PaginatedResponse":
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
        )