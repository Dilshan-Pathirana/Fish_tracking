import os
from utils.tracker import FishTracker

def process_video(video_path, output_dir):
    try:
        tracker = FishTracker(video_path, output_dir, show_window=False)
        tracker.run()
        tracker.save_results()
        return f"✅ Success: {os.path.basename(video_path)}"
    except Exception as e:
        return f"❌ Failed: {os.path.basename(video_path)} with error: {e}"
