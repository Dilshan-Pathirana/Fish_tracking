def main():
    # Safe path resolution for bundled or normal mode
    video_dir = get_resource_path("videos")
    output_dir = get_resource_path("outputs")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

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
