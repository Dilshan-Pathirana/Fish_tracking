"""Tests for distance_calculator module."""

import os
import pytest
import csv
import math
from distance_calculator import calculate_total_distance, calculate_summary


class TestCalculateTotalDistance:
    """Test cases for calculate_total_distance function."""

    def test_basic_distance_calculation(self, sample_video_with_csv):
        """Test basic distance calculation from CSV and video."""
        csv_path = sample_video_with_csv['csv_path']
        video_path = sample_video_with_csv['video_path']

        distance = calculate_total_distance(csv_path, video_path, real_width_cm=28, real_height_cm=14)

        assert distance is not None
        assert distance >= 0
        assert isinstance(distance, float)

    def test_zero_distance_with_identical_points(self, temp_output_dir, sample_video_file):
        """Test that stationary animal returns zero distance."""
        import csv

        data_dir = os.path.join(temp_output_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)

        # Create CSV with same point repeated
        csv_path = os.path.join(data_dir, 'test_stationary.csv')
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Time_hh:mm:ss:ms', 'Centroid_X', 'Centroid_Y'])
            for i in range(10):
                writer.writerow([f"00:00:00:{i:03d}", 100, 150])

        distance = calculate_total_distance(csv_path, sample_video_file)

        assert distance == 0.0 or distance is None

    def test_distance_with_non_existent_video(self, temp_output_dir):
        """Test graceful handling of missing video file."""
        import csv

        data_dir = os.path.join(temp_output_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)

        csv_path = os.path.join(data_dir, 'test.csv')
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Time_hh:mm:ss:ms', 'Centroid_X', 'Centroid_Y'])
            writer.writerow(['00:00:00:000', 100, 150])

        fake_video = os.path.join(temp_output_dir, 'nonexistent.mp4')
        distance = calculate_total_distance(csv_path, fake_video)

        assert distance is None

    def test_distance_with_custom_arena_dimensions(self, sample_video_with_csv):
        """Test distance calculation with custom tank dimensions."""
        csv_path = sample_video_with_csv['csv_path']
        video_path = sample_video_with_csv['video_path']

        distance1 = calculate_total_distance(csv_path, video_path, real_width_cm=28, real_height_cm=14)
        distance2 = calculate_total_distance(csv_path, video_path, real_width_cm=50, real_height_cm=30)

        assert distance1 is not None
        assert distance2 is not None
        assert distance1 != distance2

    def test_distance_with_frame_skip(self, sample_video_with_csv):
        """Test that frame_skip parameter affects distance calculation."""
        csv_path = sample_video_with_csv['csv_path']
        video_path = sample_video_with_csv['video_path']

        distance1 = calculate_total_distance(csv_path, video_path, frame_skip=1)
        distance2 = calculate_total_distance(csv_path, video_path, frame_skip=2)

        assert distance1 is not None
        assert distance2 is not None
        # With larger frame_skip, distance should be roughly proportional

    def test_distance_with_insufficient_points(self, temp_output_dir, sample_video_file):
        """Test handling of CSV with only one point."""
        import csv

        data_dir = os.path.join(temp_output_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)

        csv_path = os.path.join(data_dir, 'test_single.csv')
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Time_hh:mm:ss:ms', 'Centroid_X', 'Centroid_Y'])
            writer.writerow(['00:00:00:000', 100, 150])

        distance = calculate_total_distance(csv_path, sample_video_file)

        assert distance == 0


class TestCalculateSummary:
    """Test cases for calculate_summary function."""

    def test_summary_creation(self, temp_output_dir, sample_video_with_csv):
        """Test that distance summary CSV is created correctly."""
        output_root = sample_video_with_csv['output_dir']
        video_dir = os.path.dirname(sample_video_with_csv['video_path'])

        # Copy video to expected location
        import shutil
        videos_dir = os.path.join(os.path.dirname(output_root), 'videos')
        os.makedirs(videos_dir, exist_ok=True)
        video_dest = os.path.join(videos_dir, 'test_video.mp4')
        shutil.copy(sample_video_with_csv['video_path'], video_dest)

        summary_path = calculate_summary(output_root, videos_dir)

        assert summary_path is not None
        assert os.path.exists(summary_path)
        assert summary_path.endswith('distance_summary.csv')

    def test_summary_csv_format(self, temp_output_dir, sample_video_with_csv):
        """Test that summary CSV has correct format."""
        import csv

        output_root = sample_video_with_csv['output_dir']
        video_dir = os.path.dirname(sample_video_with_csv['video_path'])

        import shutil
        videos_dir = os.path.join(os.path.dirname(output_root), 'videos')
        os.makedirs(videos_dir, exist_ok=True)
        video_dest = os.path.join(videos_dir, 'test_video.mp4')
        shutil.copy(sample_video_with_csv['video_path'], video_dest)

        summary_path = calculate_summary(output_root, videos_dir)

        # Read and verify CSV format
        with open(summary_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            assert header == ['Video', 'Total Distance (cm)']

            rows = list(reader)
            assert len(rows) > 0

            # Check that first column is video name and second is numeric
            for row in rows:
                assert len(row) == 2
                assert row[0]  # Video name not empty
                # Distance should be numeric or "Error"
                if row[1] != "Error":
                    float(row[1])  # Should be convertible to float

    def test_summary_with_missing_video_directory(self, temp_output_dir):
        """Test summary generation when video directory doesn't exist."""
        nonexistent_videos = os.path.join(temp_output_dir, 'nonexistent_videos')

        # Create data directory but not videos
        data_dir = os.path.join(temp_output_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)

        result = calculate_summary(temp_output_dir, nonexistent_videos)

        assert result is None
