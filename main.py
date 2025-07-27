# main.py

import os
from utils.tracker import FishTracker

# === Configuration ===
VIDEO_FILENAME = '11.mp4'

# Automatically resolve paths
current_dir = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(current_dir, 'videos', VIDEO_FILENAME)
output_dir = current_dir  # outputs: data/ and heatmaps/ created here

# === Run Tracker ===
tracker = FishTracker(video_path=video_path, output_dir=output_dir)
tracker.run()
tracker.save_results()
