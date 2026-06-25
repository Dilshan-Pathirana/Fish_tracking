"""Tests for tracker_wrapper module."""

import os
import pytest
from tracker_wrapper import get_resource_path, process_video


class TestGetResourcePath:
    """Test resource path resolution."""

    def test_get_resource_path_returns_string(self):
        """Test that get_resource_path returns a string."""
        path = get_resource_path("test_dir")
        assert isinstance(path, str)

    def test_get_resource_path_includes_relative_path(self):
        """Test that relative path is included in result."""
        relative = "some/test/path.txt"
        path = get_resource_path(relative)
        assert relative in path or path.endswith(relative.replace("/", os.sep))

    def test_get_resource_path_is_absolute(self):
        """Test that result is an absolute path."""
        path = get_resource_path("test_dir")
        assert os.path.isabs(path)


class TestProcessVideo:
    """Test video processing wrapper function."""

    def test_process_video_success(self, sample_video_file, temp_output_dir):
        """Test successful video processing."""
        result = process_video(sample_video_file, temp_output_dir)

        assert isinstance(result, str)
        assert "✅" in result or "Success" in result

    def test_process_video_returns_status_message(self, sample_video_file, temp_output_dir):
        """Test that process_video returns status message."""
        result = process_video(sample_video_file, temp_output_dir)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_process_video_creates_outputs(self, sample_video_file, temp_output_dir):
        """Test that process_video creates expected output files."""
        process_video(sample_video_file, temp_output_dir)

        # Check that tracking outputs were created
        data_dir = os.path.join(temp_output_dir, 'data')
        heatmaps_dir = os.path.join(temp_output_dir, 'heatmaps')

        assert os.path.exists(data_dir)
        assert os.path.exists(heatmaps_dir)

        # Should have CSV and heatmap files
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        heatmap_files = [f for f in os.listdir(heatmaps_dir) if f.endswith('.png')]

        assert len(csv_files) > 0
        assert len(heatmap_files) > 0

    def test_process_video_with_invalid_path(self, temp_output_dir):
        """Test graceful error handling with invalid video path."""
        result = process_video("nonexistent_video.mp4", temp_output_dir)

        assert isinstance(result, str)
        assert ("❌" in result or "Failed" in result or "Error" in result)
