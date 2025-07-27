import os
import re
from multiprocessing import Pool
from utils.tracker import FishTracker

NUM_WORKERS = 10
BATCH_SIZE = 10

def process_video(video_file):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    video_dir = os.path.join(base_dir, "videos")
    output_dir = os.path.join(base_dir, "outputs")

    video_path = os.path.join(video_dir, video_file)

    tracker = FishTracker(video_path, output_dir, show_window=False)
    try:
        tracker.run()
        tracker.save_results()
        return f"✅ Success: {video_file}"
    except Exception as e:
        return f"❌ Failed: {video_file} with error: {e}"

def chunk_list(lst, n):
    """Yield successive n-sized chunks from list."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def extract_number(filename):
    """Extract number from filename like '12.mp4' -> 12"""
    match = re.match(r"(\d+)", filename)
    return int(match.group(1)) if match else float('inf')

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    video_dir = os.path.join(base_dir, "videos")

    videos = sorted(
        [f for f in os.listdir(video_dir) if f.lower().endswith(".mp4")],
        key=extract_number
    )

    total = len(videos)
    print(f"🎞️ Found {total} videos. Running in batches of {BATCH_SIZE} using {NUM_WORKERS} workers.")

    batches = list(chunk_list(videos, BATCH_SIZE))

    for i, batch in enumerate(batches, 1):
        print(f"\n🚀 Starting batch {i}/{len(batches)}:")
        print("   🎬 Videos:", ', '.join(batch))

        with Pool(processes=NUM_WORKERS) as pool:
            results = pool.map(process_video, batch)

        for res in results:
            print("   " + res)

    print("\n✅ All batches processed.")

if __name__ == "__main__":
    main()
