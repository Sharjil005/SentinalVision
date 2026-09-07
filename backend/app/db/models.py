"""
SQLAlchemy database models for SentinalVision.
"""

import enum
from datetime import datetime
from typing import Optional, List

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Float, ForeignKey, Enum, Index, Boolean
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class AnalysisStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AlertSeverity(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class User(Base):
    """User model for authentication."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


class ModelVersion(Base):
    """Track ML model versions used for analyses."""
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # e.g., "yolov8n", "resnet18"
    version = Column(String(50), nullable=False)  # e.g., "v1", "2024.01"
    yolo_model_path = Column(String(500))
    classifier_model_path = Column(String(500))
    yolo_version = Column(String(50))
    classifier_version = Column(String(50))
    metrics_json = Column(Text)  # JSON string of evaluation metrics
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    analyses = relationship("Analysis", back_populates="model_version")

    def __repr__(self):
        return f"<ModelVersion({self.name} v{self.version})>"


class Analysis(Base):
    """Video analysis record."""
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    model_version_id = Column(Integer, ForeignKey("model_versions.id"), index=True)

    # File info
    filename = Column(String(500), nullable=False)
    original_filename = Column(String(500))
    file_size = Column(Integer)  # bytes
    mime_type = Column(String(100))
    file_path = Column(String(1000))  # Path to stored file

    # Video properties
    duration = Column(Float)  # seconds
    fps = Column(Float)
    width = Column(Integer)
    height = Column(Integer)
    total_frames = Column(Integer)

    # Processing info
    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING, index=True)
    processed_frames = Column(Integer, default=0)
    frame_sample_rate = Column(Integer, default=1)
    error_message = Column(Text)

    # Output
    output_video_path = Column(String(1000))
    processing_time_seconds = Column(Float)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="analyses")
    model_version = relationship("ModelVersion", back_populates="analyses")
    detections = relationship("Detection", back_populates="analysis", cascade="all, delete-orphan")
    classification_results = relationship("ClassificationResult", back_populates="analysis", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="analysis", cascade="all, delete-orphan")
    statistics = relationship("AnalysisStatistic", back_populates="analysis", cascade="all, delete-orphan", uselist=False)

    def __repr__(self):
        return f"<Analysis(id={self.id}, filename='{self.filename}', status={self.status})>"


class Detection(Base):
    """Object detection result from YOLO."""
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False, index=True)

    frame_number = Column(Integer, index=True)
    timestamp = Column(Float)  # seconds from video start

    # Bounding box (pixel coordinates)
    bbox_x1 = Column(Float)
    bbox_y1 = Column(Float)
    bbox_x2 = Column(Float)
    bbox_y2 = Column(Float)

    # Detection info
    class_name = Column(String(100), index=True)
    class_id = Column(Integer)
    confidence = Column(Float)

    # Relationships
    analysis = relationship("Analysis", back_populates="detections")
    classification_results = relationship("ClassificationResult", back_populates="detection", cascade="all, delete-orphan")

    # Index for common queries
    __table_args__ = (
        Index("ix_detections_analysis_class", "analysis_id", "class_name"),
        Index("ix_detections_analysis_frame", "analysis_id", "frame_number"),
    )

    def __repr__(self):
        return f"<Detection(id={self.id}, class='{self.class_name}', conf={self.confidence:.2f})>"


class ClassificationResult(Base):
    """Threat classification result from CNN."""
    __tablename__ = "classification_results"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False, index=True)
    detection_id = Column(Integer, ForeignKey("detections.id"), index=True)

    frame_number = Column(Integer)
    timestamp = Column(Float)

    # Classification info
    class_name = Column(String(100), index=True)
    confidence = Column(Float)
    all_probabilities = Column(Text)  # JSON string of all class probabilities

    # Model info
    model_version = Column(String(100))

    # Relationships
    analysis = relationship("Analysis", back_populates="classification_results")
    detection = relationship("Detection", back_populates="classification_results")

    __table_args__ = (
        Index("ix_classification_analysis_class", "analysis_id", "class_name"),
        Index("ix_classification_analysis_frame", "analysis_id", "frame_number"),
    )

    def __repr__(self):
        return f"<ClassificationResult(class='{self.class_name}', conf={self.confidence:.2f})>"


class Alert(Base):
    """Generated alert from threat classification."""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False, index=True)

    alert_type = Column(String(100), index=True)  # e.g., "person_loitering", "unattended_object"
    severity = Column(Enum(AlertSeverity), default=AlertSeverity.INFO, index=True)
    message = Column(Text)
    confidence = Column(Float)

    # Context
    frame_number = Column(Integer)
    timestamp = Column(Float)
    detection_ids = Column(Text)  # JSON array of related detection IDs
    classification_ids = Column(Text)  # JSON array of related classification IDs

    # Acknowledgment
    acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(Integer, ForeignKey("users.id"))
    acknowledged_at = Column(DateTime)

    # Metadata
    rule_config = Column(Text)  # JSON of rule that triggered this alert
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    analysis = relationship("Analysis", back_populates="alerts")

    __table_args__ = (
        Index("ix_alerts_analysis_severity", "analysis_id", "severity"),
        Index("ix_alerts_created", "created_at"),
    )

    def __repr__(self):
        return f"<Alert(type='{self.alert_type}', severity={self.severity}, conf={self.confidence:.2f})>"


class AnalysisStatistic(Base):
    """Aggregated statistics for an analysis."""
    __tablename__ = "analysis_statistics"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), unique=True, nullable=False)

    # Detection counts
    total_detections = Column(Integer, default=0)
    unique_classes = Column(Integer, default=0)
    detections_by_class = Column(Text)  # JSON: {"person": 45, "car": 12, ...}

    # Classification counts
    total_classifications = Column(Integer, default=0)
    classifications_by_class = Column(Text)  # JSON

    # Alert counts
    total_alerts = Column(Integer, default=0)
    alerts_by_severity = Column(Text)  # JSON: {"info": 2, "warning": 1, "critical": 0}

    # Performance
    avg_detection_confidence = Column(Float)
    avg_classification_confidence = Column(Float)
    avg_inference_time_ms = Column(Float)

    # Relationships
    analysis = relationship("Analysis", back_populates="statistics")

    def __repr__(self):
        return f"<AnalysisStatistic(analysis_id={self.analysis_id}, detections={self.total_detections})>"