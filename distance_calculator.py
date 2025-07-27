import os
import csv
import math
import cv2

def calculate_total_distance(csv_path, video_path, real_width_cm=28, real_height_cm=14):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Warning: Could not open video {video_path}. Skipping.")
        return None

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    points = []
    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for idx, row in enumerate(reader):
                if idx % 60 != 0:
                    continue
                x = int(row['Centroid_X'])
                y = int(row['Centroid_Y'])
                points.append((x, y))
    except Exception as e:
        print(f"Error reading CSV {csv_path}: {e}")
        return None

    if len(points) < 2:
        print(f"Not enough points in {csv_path} to calculate distance.")
        return 0

    total_pixel_distance = sum(
        math.sqrt((points[i][0] - points[i-1][0])**2 + (points[i][1] - points[i-1][1])**2)
        for i in range(1, len(points))
    )

    pixel_to_cm_x = real_width_cm / frame_width
    pixel_to_cm_y = real_height_cm / frame_height
    pixel_to_cm = (pixel_to_cm_x + pixel_to_cm_y) / 2

    return total_pixel_distance * pixel_to_cm


def calculate_summary(output_root):
    data_dir = os.path.join(output_root, 'data')
    videos_dir = os.path.join(os.path.dirname(output_root), 'videos')
    summary_csv = os.path.join(output_root, 'distance_summary.csv')

    if not os.path.exists(data_dir) or not os.path.exists(videos_dir):
        print("❌ Required directories not found.")
        return None

    csv_files = [f for f in os.listdir(data_dir) if f.lower().endswith('.csv')]
    if not csv_files:
        print("❌ No CSV files found in data directory.")
        return None

    results = []
    for csv_file in csv_files:
        name = os.path.splitext(csv_file)[0]
        video_path = os.path.join(videos_dir, name + ".mp4")
        csv_path = os.path.join(data_dir, csv_file)

        if not os.path.exists(video_path):
            print(f"⚠️ Missing video for: {csv_file}")
            continue

        distance = calculate_total_distance(csv_path, video_path)
        if distance is not None:
            results.append([name, f"{distance:.2f}"])
        else:
            results.append([name, "Error"])

    os.makedirs(output_root, exist_ok=True)
    with open(summary_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Video', 'Total Distance (cm)'])
        writer.writerows(results)

    print(f"\n✅ Distance summary saved to: {summary_csv}")
    return summary_csv
