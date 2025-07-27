import os
import re
from multiprocessing import Pool
from tracker_wrapper import process_video  # Shared logic
from functools import partial

NUM_WORKERS = 10
BATCH_SIZE = 10

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def extract_number(filename):
    match = re.match(r"(\d+)", filename)
    return int(match.group(1)) if match else float('inf')

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    video_dir = os.path.join(base_dir, "videos")
    output_dir = os.path.join(base_dir, "outputs")

    videos = sorted(
        [f for f in os.listdir(video_dir) if f.lower().endswith(".mp4")],
        key=extract_number
    )
    video_paths = [os.path.join(video_dir, f) for f in videos]
    total = len(video_paths)

    print(f"🎞️ Found {total} videos. Running in batches of {BATCH_SIZE} using {NUM_WORKERS} workers.")

    batches = list(chunk_list(video_paths, BATCH_SIZE))

    for i, batch in enumerate(batches, 1):
        print(f"\n🚀 Starting batch {i}/{len(batches)}:")
        print("   🎬 Videos:", ', '.join([os.path.basename(b) for b in batch]))

        with Pool(processes=NUM_WORKERS) as pool:
            results = pool.map(partial(process_video, output_dir=output_dir), batch)

        for res in results:
            print("   " + res)

    print("\n✅ All batches processed.")

if __name__ == "__main__":
    main()
