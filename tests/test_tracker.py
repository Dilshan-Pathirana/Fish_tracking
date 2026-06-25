"""Tests for tracker module (FishTracker class)."""

import os
import pytest
import csv
import cv2
import numpy as np
from utils.tracker import FishTracker


class TestFishTrackerInitialization:
    """Test FishTracker initialization and setup."""

    def test_initialization(self, sample_video_file, temp_output_dir):
        """Test FishTracker initialization."""
        tracker = FishTracker(sample_video_file, temp_output_dir, show_window=False)

        assert tracker.video_path == sample_video_file
        assert tracker.output_dir == temp_output_dir
        assert tracker.last_bbox is None
        assert tracker.no_movement_frames == 0
        assert len(tracker.centroid_data) == 0
        assert len(tracker.positions) == 0

    def test_output_directories_created(self, sample_video_file, temp_output_dir):
        """Test that output directories are created on initialization."""
        tracker = FishTracker(sample_video_file, temp_output_dir)

        data_dir = os.path.join(temp_output_dir, 'data')
        heatmaps_dir = os.path.join(temp_output_dir, 'heatmaps')

        assert os.path.exists(data_dir)
        assert os.path.exists(heatmaps_dir)


class TestFishTrackerTimeHandling:
    """Test time formatting and timestamp handling."""

    def test_current_time_ms(self, sample_video_file, temp_output_dir):
        """Test current_time_ms returns valid integer."""
        tracker = FishTracker(sample_video_file, temp_output_dir)
        time_ms = tracker.current_time_ms()

        assert isinstance(time_ms, int)
        assert time_ms > 0

    def test_format_time(self, sample_video_file, temp_output_dir):
        """Test time formatting."""
        tracker = FishTracker(sample_video_file, temp_output_dir)

        # Test cases: ms -> expected format HH:MM:SS:ms
        test_cases = [
            (0, "00:00:00:000"),
            (1000, "00:00:01:000"),
            (60000, "00:01:00:000"),
            (3600000, "01:00:00:000"),
            (3661234, "01:01:01:234"),
        ]

        for ms, expected in test_cases:
            assert tracker.format_time(ms) == expected


class TestFishTrackerCentroidLogging:
    """Test centroid position logging."""

    def test_log_centroid(self, sample_video_file, temp_output_dir):
        """Test centroid logging."""
        tracker = FishTracker(sample_video_file, temp_output_dir)

        tracker.log_centroid(100, 150)

        assert len(tracker.centroid_data) == 1
        assert len(tracker.positions) == 1
        assert tracker.centroid_data[0][1] == 100
        assert tracker.centroid_data[0][2] == 150
        assert tracker.positions[0] == (100, 150)

    def test_multiple_centroid_logs(self, sample_video_file, temp_output_dir):
        """Test logging multiple centroids."""
        tracker = FishTracker(sample_video_file, temp_output_dir)

        for i in range(10):
            tracker.log_centroid(100 + i, 150 + i)

        assert len(tracker.centroid_data) == 10
        assert len(tracker.positions) == 10


class TestFishTrackerFrameProcessing:
    """Test frame processing pipeline."""

    def test_process_frame_returns_frame(self, sample_video_file, temp_output_dir):
        """Test that process_frame returns annotated frame."""
        tracker = FishTracker(sample_video_file, temp_output_dir, show_window=False)

        # Read a frame from the video
        cap = cv2.VideoCapture(sample_video_file)
        ret, frame = cap.read()
        cap.release()

        assert ret, "Could not read test video"

        result = tracker.process_frame(frame)

        assert isinstance(result, np.ndarray)
        assert result.shape == frame.shape

    def test_process_frame_logs_detection(self, sample_video_file, temp_output_dir):
        """Test that process_frame logs centroids when detection occurs."""
        tracker = FishTracker(sample_video_file, temp_output_dir, show_window=False)

        cap = cv2.VideoCapture(sample_video_file)
        ret, frame = cap.read()
        cap.release()

        initial_count = len(tracker.centroid_data)

        # Process multiple frames to ensure at least one detection
        cap = cv2.VideoCapture(sample_video_file)
        for _ in range(20):
            ret, frame = cap.read()
            if not ret:
                break
            tracker.process_frame(frame)
        cap.release()

        # Should have logged at least some frames
        assert len(tracker.centroid_data) > initial_count


class TestFishTrackerVideoProcessing:
    """Test full video processing."""

    def test_run_processes_video(self, sample_video_file, temp_output_dir):
        """Test that run() processes entire video."""
        tracker = FishTracker(sample_video_file, temp_output_dir, show_window=False)
        tracker.run()

        # Should have logged frames
        assert len(tracker.centroid_data) > 0
        assert len(tracker.positions) > 0

    def test_run_captures_valid_frame(self, sample_video_file, temp_output_dir):
        """Test that run() captures a valid frame."""
        tracker = FishTracker(sample_video_file, temp_output_dir, show_window=False)
        tracker.run()

        assert tracker.valid_frame is not None
        assert isinstance(tracker.valid_frame, np.ndarray)


class TestFishTrackerSaveResults:
    """Test saving tracking results."""

    def test_save_results_creates_csv(self, sample_video_file, temp_output_dir):
        """Test that save_results creates CSV file."""
        tracker = FishTracker(sample_video_file, temp_output_dir, show_window=False)
        tracker.run()
        tracker.save_results()

        # Check CSV exists
        csv_path = os.path.join(temp_output_dir, 'data', 'test_video.csv')
        assert os.path.exists(csv_path)

    def test_csv_format(self, sample_video_file, temp_output_dir):
        """Test that saved CSV has correct format."""
        tracker = FishTracker(sample_video_file, temp_output_dir, show_window=False)
        tracker.run()
        tracker.save_results()

        csv_path = os.path.join(temp_output_dir, 'data', 'test_video.csv')

        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)

            assert header == ['Time_hh:mm:ss:ms', 'Centroid_X', 'Centroid_Y']

            rows = list(reader)
            assert len(rows) > 0

            # Check format of data rows
            for row in rows:
                assert len(row) == 3
                # First column is timestamp (HH:MM:SS:ms format)
                assert ':' in row[0]
                # Second and third are coordinates (numeric)
                int(row[1])  # Should be convertible
                int(row[2])

    def test_save_results_creates_heatmap(self, sample_video_file, temp_output_dir):
        """Test that save_results creates heatmap image."""
        tracker = FishTracker(sample_video_file, temp_output_dir, show_window=False)
        tracker.run()
        tracker.save_results()

        heatmap_path = os.path.join(temp_output_dir, 'heatmaps', 'test_video.png')
        assert os.path.exists(heatmap_path)

    def test_save_results_without_valid_frame(self, sample_video_file, temp_output_dir):
        """Test save_results handles case of no valid frame."""
        tracker = FishTracker(sample_video_file, temp_output_dir)
        # Don't call run(), so valid_frame is None

        # Should print message but not crash
        tracker.save_results()

        # CSV should not be created without valid_frame
        csv_path = os.path.join(temp_output_dir, 'data', 'test_video.csv')
        assert not os.path.exists(csv_path)


class TestFishTrackerIntegration:
    """Integration tests for complete tracking workflow."""

    def test_full_workflow(self, sample_video_file, temp_output_dir):
        """Test complete tracking workflow: init -> run -> save."""
        tracker = FishTracker(sample_video_file, temp_output_dir, show_window=False)

        # Process video
        tracker.run()
        assert len(tracker.centroid_data) > 0

        # Save results
        tracker.save_results()

        # Verify outputs exist
        csv_path = os.path.join(temp_output_dir, 'data', 'test_video.csv')
        heatmap_path = os.path.join(temp_output_dir, 'heatmaps', 'test_video.png')

        assert os.path.exists(csv_path)
        assert os.path.exists(heatmap_path)
        assert os.path.getsize(csv_path) > 0
        assert os.path.getsize(heatmap_path) > 0
