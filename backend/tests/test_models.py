"""
Test database models
"""
import pytest
from sqlalchemy.orm import Session
from app.db.models import User, Analysis, Detection, ModelVersion, AnalysisStatus


def test_user_model(db_session: Session):
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        full_name="Test User"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.is_active is True
    assert user.created_at is not None


def test_analysis_model(db_session: Session):
    user = User(email="test2@example.com", password_hash="hash")
    db_session.add(user)
    db_session.commit()

    analysis = Analysis(
        user_id=user.id,
        filename="test_video.mp4",
        file_size=1024000,
        duration=30.5,
        fps=30.0,
        width=1920,
        height=1080,
        total_frames=915,
        status=AnalysisStatus.PENDING
    )
    db_session.add(analysis)
    db_session.commit()
    db_session.refresh(analysis)

    assert analysis.id is not None
    assert analysis.filename == "test_video.mp4"
    assert analysis.status == AnalysisStatus.PENDING
    assert analysis.user_id == user.id


def test_detection_model(db_session: Session):
    user = User(email="test3@example.com", password_hash="hash")
    db_session.add(user)
    db_session.commit()

    analysis = Analysis(
        user_id=user.id,
        filename="test.mp4",
        status=AnalysisStatus.COMPLETED
    )
    db_session.add(analysis)
    db_session.commit()

    detection = Detection(
        analysis_id=analysis.id,
        frame_number=100,
        timestamp=3.33,
        bbox_x1=100,
        bbox_y1=200,
        bbox_x2=300,
        bbox_y2=400,
        class_name="person",
        class_id=0,
        confidence=0.95
    )
    db_session.add(detection)
    db_session.commit()
    db_session.refresh(detection)

    assert detection.id is not None
    assert detection.class_name == "person"
    assert detection.confidence == 0.95


def test_model_version_model(db_session: Session):
    mv = ModelVersion(
        name="yolov8n",
        version="v1",
        yolo_model_path="./models/yolov8n.pt",
        yolo_version="8.0.0",
        is_active=True
    )
    db_session.add(mv)
    db_session.commit()
    db_session.refresh(mv)

    assert mv.id is not None
    assert mv.name == "yolov8n"
    assert mv.version == "v1"
    assert mv.is_active is True