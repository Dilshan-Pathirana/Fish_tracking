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

        width, height = 640, 480
        fps = 30
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

        for frame_num in range(100):
            frame = np.ones((height, width, 3), dtype=np.uint8) * 200
            x = int(100 + 100 * np.sin(frame_num * 0.1))
            y = int(height // 2 + 50 * np.cos(frame_num * 0.1))
            cv2.circle(frame, (x, y), radius=20, color=(50, 50, 50), thickness=-1)
            out.write(frame)

        out.release()
        yield video_path


@pytest.fixture
def sample_csv_data():
    """Return 65 rows of centroid data.

    65 rows ensures frame_skip=60 (df.iloc[::60]) yields 2 points (rows 0 and 60),
    allowing real distance calculation rather than the early-exit zero return.
    """
    rows = []
    for i in range(65):
        ms = i * 33
        hh = ms // 3600000
        remainder = ms % 3600000
        mm = remainder // 60000
        remainder = remainder % 60000
        ss = remainder // 1000
        ms_part = remainder % 1000
        timestamp = "{:02}:{:02}:{:02}:{:03}".format(hh, mm, ss, ms_part)
        rows.append([timestamp, 100 + i * 2, 150 + i])
    return rows


@pytest.fixture
def sample_video_with_csv(temp_output_dir, sample_video_file, sample_csv_data):
    """Create test video with corresponding CSV file."""
    import csv

    data_dir = os.path.join(temp_output_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

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
