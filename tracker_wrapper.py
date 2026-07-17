"""Wrapper module for video processing with resource path resolution.

Provides a bridge between batch/GUI modes and the FishTracker core module,
handling path resolution for both PyInstaller bundled executables and
development environments.
"""

import os
import sys
from utils.tracker import FishTracker


def get_resource_path(relative_path: str) -> str:
    """Get absolute path to resource compatible with PyInstaller and dev mode.

    In PyInstaller bundled executables, locates resources relative to the
    temporary extraction directory (_MEIPASS). In development, uses the
    current working directory.

    Args:
        relative_path: Relative path to the resource.

    Returns:
        Absolute path to the resource.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def process_video(video_path: str, output_dir: str) -> str:
    """Process a single video with background-subtraction tracking.

    Initializes FishTracker, runs frame-by-frame detection, and saves
    results (CSV trajectory and heatmap image). Handles resource path
    resolution for both PyInstaller and development environments.

    Args:
        video_path: Path to input video file.
        output_dir: Directory where output files will be saved.

    Returns:
        Status message indicating success or failure with details.
    """
    try:
        # Convert to absolute resource-safe paths
        video_path = get_resource_path(video_path)
        output_dir = get_resource_path(output_dir)

        tracker = FishTracker(video_path, output_dir, show_window=False)
        tracker.run()
        tracker.save_results()
        return f"✅ Success: {os.path.basename(video_path)}"
    except Exception as e:
        return f"❌ Failed: {os.path.basename(video_path)} with error: {e}"
