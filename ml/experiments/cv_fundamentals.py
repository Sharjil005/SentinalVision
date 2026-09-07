"""
Phase 4: Computer Vision Fundamentals - OpenCV Experiment
This script demonstrates basic OpenCV operations for learning purposes.
Run with: python ml/experiments/cv_fundamentals.py
"""

import cv2
import numpy as np
from pathlib import Path


def experiment_1_basic_image_info():
    """Experiment 1: Load image and display basic information."""
    print("=" * 50)
    print("Experiment 1: Basic Image Information")
    print("=" * 50)

    # Create a synthetic image for demonstration
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.rectangle(img, (100, 100), (300, 300), (0, 255, 0), -1)  # Green rectangle
    cv2.circle(img, (400, 200), 50, (255, 0, 0), -1)  # Blue circle
    cv2.putText(img, "OpenCV Demo", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    print(f"Image shape: {img.shape}")  # (height, width, channels)
    print(f"Image dtype: {img.dtype}")  # uint8 (0-255)
    print(f"Image size: {img.size} pixels")
    print(f"Channels: {img.shape[2]} (BGR order in OpenCV)")

    # Show pixel values at specific locations
    print(f"\nPixel at (100, 100) [B,G,R]: {img[100, 100]}")  # Inside green rect
    print(f"Pixel at (400, 200) [B,G,R]: {img[400, 200]}")  # Inside blue circle
    print(f"Pixel at (0, 0) [B,G,R]: {img[0, 0]}")  # Background (black)

    # Save for visual inspection
    output_path = Path("ml/experiments/output_basic.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), img)
    print(f"\nSaved demo image to: {output_path}")

    return img


def experiment_2_color_spaces():
    """Experiment 2: Color space conversions."""
    print("\n" + "=" * 50)
    print("Experiment 2: Color Spaces")
    print("=" * 50)

    img = experiment_1_basic_image_info()

    # BGR to RGB (for display with matplotlib)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(f"RGB shape: {rgb.shape}")
    print(f"Sample RGB pixel: {rgb[100, 100]}")

    # BGR to Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"Grayscale shape: {gray.shape}")
    print(f"Sample gray pixel: {gray[100, 100]}")

    # BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print(f"HSV shape: {hsv.shape}")
    print(f"Sample HSV pixel: {hsv[100, 100]}")

    return rgb, gray, hsv


def experiment_3_resize_normalize():
    """Experiment 3: Resizing and normalization (preprocessing for ML)."""
    print("\n" + "=" * 50)
    print("Experiment 3: Resize & Normalize")
    print("=" * 50)

    img = experiment_1_basic_image_info()

    # Resize to common model input size (224x224 for ResNet, etc.)
    target_size = (224, 224)
    resized = cv2.resize(img, target_size, interpolation=cv2.INTER_LINEAR)
    print(f"Resized shape: {resized.shape}")

    # Normalize to [0, 1] range (typical for neural networks)
    normalized = resized.astype(np.float32) / 255.0
    print(f"Normalized range: [{normalized.min():.4f}, {normalized.max():.4f}]")
    print(f"Normalized dtype: {normalized.dtype}")

    # Standardize with ImageNet mean/std (common for transfer learning)
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    standardized = (normalized - mean) / std
    print(f"Standardized range: [{standardized.min():.4f}, {standardized.max():.4f}]")

    # Convert to CHW format (PyTorch expects channels first)
    chw = standardized.transpose(2, 0, 1)  # HWC -> CHW
    print(f"CHW shape: {chw.shape}")  # (3, 224, 224)

    # Add batch dimension
    batch = chw[np.newaxis, ...]  # (1, 3, 224, 224)
    print(f"Batch shape: {batch.shape}")

    return batch


def experiment_4_video_frames():
    """Experiment 4: Video frame extraction."""
    print("\n" + "=" * 50)
    print("Experiment 4: Video Frame Extraction")
    print("=" * 50)

    # Create a simple test video
    output_path = Path("ml/experiments/test_video.mp4")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    frame_size = (640, 480)
    out = cv2.VideoWriter(str(output_path), fourcc, fps, frame_size)

    for i in range(90):  # 3 seconds at 30fps
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Moving circle
        x = 50 + int(i * 6)
        y = 240
        cv2.circle(frame, (x, y), 30, (0, 255, 255), -1)
        cv2.putText(frame, f"Frame {i}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        out.write(frame)

    out.release()
    print(f"Created test video: {output_path}")

    # Now read it back
    cap = cv2.VideoCapture(str(output_path))
    print(f"Video FPS: {cap.get(cv2.CAP_PROP_FPS)}")
    print(f"Frame count: {cap.get(cv2.CAP_PROP_FRAME_COUNT)}")
    print(f"Width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
    print(f"Height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")

    # Read first few frames
    for i in range(3):
        ret, frame = cap.read()
        if ret:
            print(f"Frame {i} shape: {frame.shape}, mean pixel: {frame.mean():.1f}")

    cap.release()

    # Frame sampling example
    print("\nFrame sampling (every 10th frame):")
    cap = cv2.VideoCapture(str(output_path))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    sample_rate = 10

    for i in range(0, frame_count, sample_rate):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            print(f"  Sampled frame {i}: shape={frame.shape}")

    cap.release()


def experiment_5_bounding_boxes():
    """Experiment 5: Working with bounding boxes."""
    print("\n" + "=" * 50)
    print("Experiment 5: Bounding Boxes")
    print("=" * 50)

    img = experiment_1_basic_image_info().copy()

    # Simulate YOLO-style detections: [x1, y1, x2, y2, confidence, class_id]
    detections = [
        [100, 100, 300, 300, 0.95, 0],  # Green rectangle
        [350, 150, 450, 250, 0.87, 1],  # Blue circle area
    ]

    class_names = ["rectangle", "circle"]
    colors = [(0, 255, 0), (255, 0, 0)]

    for det in detections:
        x1, y1, x2, y2, conf, cls_id = det
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

        # Draw bounding box
        color = colors[int(cls_id)]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        # Draw label
        label = f"{class_names[int(cls_id)]}: {conf:.2f}"
        (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(img, (x1, y1 - label_h - 10), (x1 + label_w, y1), color, -1)
        cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Calculate center and dimensions
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        width = x2 - x1
        height = y2 - y1
        print(f"Detection: class={class_names[int(cls_id)]}, conf={conf:.2f}")
        print(f"  BBox: [{x1}, {y1}, {x2}, {y2}]")
        print(f"  Center: ({center_x:.1f}, {center_y:.1f}), Size: {width}x{height}")

    output_path = Path("ml/experiments/output_detections.png")
    cv2.imwrite(str(output_path), img)
    print(f"\nSaved detection visualization to: {output_path}")


def main():
    """Run all experiments."""
    print("Computer Vision Fundamentals - OpenCV Experiments")
    print("This script demonstrates core concepts for Phase 4.\n")

    experiment_1_basic_image_info()
    experiment_2_color_spaces()
    experiment_3_resize_normalize()
    experiment_4_video_frames()
    experiment_5_bounding_boxes()

    print("\n" + "=" * 50)
    print("All experiments completed!")
    print("=" * 50)
    print("\nKey Concepts Learned:")
    print("1. Images are numpy arrays (H, W, C) with BGR channel order in OpenCV")
    print("2. Pixel values are uint8 (0-255), normalized to float32 [0,1] for ML")
    print("3. Common preprocessing: resize -> normalize -> standardize -> CHW -> batch")
    print("4. Video = sequence of frames; use cv2.VideoCapture for reading")
    print("5. Bounding boxes: [x1, y1, x2, y2] format, can convert to center/size")
    print("6. Color spaces: BGR (OpenCV), RGB (display), HSV (color analysis), Gray (edges)")


if __name__ == "__main__":
    main()