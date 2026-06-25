"""Pytest configuration and shared fixtures for FishTracker tests."""

import os
import tempfile
import pytest
import cv2
import numpy as np
from pathlib import Path


@pytest.fixture
def temp_output_dir():
    """Create a temporary output directory for test results."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_video_file():
    """Create a minimal test video file with synthetic moving object."""
    with tempfile.TemporaryDirectory() as temp_dir:
        video_path = os.path.join(temp_dir, "test_video.mp4")

        # Create video with synthetic fish
        width, height = 640, 480
        fps = 30
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

        # Generate 100 frames with moving object
        for frame_num in range(100):
            frame = np.ones((height, width, 3), dtype=np.uint8) * 200  # Light background

            # Moving dark circle (simulating fish)
            x = int(100 + 100 * np.sin(frame_num * 0.1))
            y = int(height // 2 + 50 * np.cos(frame_num * 0.1))
            cv2.circle(frame, (x, y), radius=20, color=(50, 50, 50), thickness=-1)

            out.write(frame)

        out.release()
        yield video_path


@pytest.fixture
def sample_csv_data():
    """Return sample centroid data for testing distance calculations."""
    return [
        ["00:00:00:000", 100, 150],
        ["00:00:00:033", 102, 152],
        ["00:00:00:066", 105, 155],
        ["00:00:00:100", 110, 160],
        ["00:00:00:133", 115, 165],
    ]


@pytest.fixture
def sample_video_with_csv(temp_output_dir, sample_video_file, sample_csv_data):
    """Create test video with corresponding CSV file."""
    import csv

    # Create data subdirectory
    data_dir = os.path.join(temp_output_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Write CSV
    csv_path = os.path.join(data_dir, 'test_video.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time_hh:mm:ss:ms', 'Centroid_X', 'Centroid_Y'])
        writer.writerows(sample_csv_data)

    return {
        'csv_path': csv_path,
        'video_path': sample_video_file,
        'output_dir': temp_output_dir,
    }
