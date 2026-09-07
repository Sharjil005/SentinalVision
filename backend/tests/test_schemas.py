"""
Test Pydantic schemas
"""
import pytest
from datetime import datetime
from app.models.schemas import (
    UserCreate,
    UserResponse,
    AnalysisCreate,
    AnalysisResponse,
    DetectionCreate,
    DetectionResponse,
    AlertCreate,
    AlertResponse,
    HealthResponse,
    AnalysisStatus,
    AlertSeverity,
)


def test_user_create_schema():
    user = UserCreate(
        email="test@example.com",
        password="password123",
        full_name="Test User"
    )
    assert user.email == "test@example.com"
    assert user.password == "password123"
    assert user.full_name == "Test User"


def test_user_create_invalid_email():
    with pytest.raises(ValueError):
        UserCreate(email="invalid-email", password="password123")


def test_user_create_short_password():
    with pytest.raises(ValueError):
        UserCreate(email="test@example.com", password="short")


def test_analysis_create_schema():
    analysis = AnalysisCreate(
        filename="test.mp4",
        original_filename="test.mp4",
        file_size=1024,
        duration=30.0,
        fps=30.0,
        width=1920,
        height=1080,
        total_frames=900,
        frame_sample_rate=1
    )
    assert analysis.filename == "test.mp4"
    assert analysis.frame_sample_rate == 1


def test_detection_create_schema():
    detection = DetectionCreate(
        analysis_id=1,
        frame_number=100,
        timestamp=3.33,
        bbox_x1=100.0,
        bbox_y1=200.0,
        bbox_x2=300.0,
        bbox_y2=400.0,
        class_name="person",
        class_id=0,
        confidence=0.95
    )
    assert detection.class_name == "person"
    assert detection.confidence == 0.95


def test_alert_create_schema():
    alert = AlertCreate(
        analysis_id=1,
        alert_type="person_loitering",
        severity=AlertSeverity.WARNING,
        message="Person detected loitering",
        confidence=0.87,
        frame_number=100,
        timestamp=3.33
    )
    assert alert.alert_type == "person_loitering"
    assert alert.severity == AlertSeverity.WARNING


def test_health_response_schema():
    health = HealthResponse(
        status="healthy",
        service="SentinalVision",
        version="0.1.0"
    )
    assert health.status == "healthy"
    assert health.service == "SentinalVision"
    assert isinstance(health.timestamp, datetime)


def test_analysis_status_enum():
    assert AnalysisStatus.PENDING == "pending"
    assert AnalysisStatus.COMPLETED == "completed"
    assert AnalysisStatus.FAILED == "failed"


def test_alert_severity_enum():
    assert AlertSeverity.INFO == "info"
    assert AlertSeverity.WARNING == "warning"
    assert AlertSeverity.CRITICAL == "critical"