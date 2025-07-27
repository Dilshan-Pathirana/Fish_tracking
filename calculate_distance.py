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

    total_pixel_distance = 0
    for i in range(1, len(points)):
        dx = points[i][0] - points[i-1][0]
        dy = points[i][1] - points[i-1][1]
        total_pixel_distance += math.sqrt(dx*dx + dy*dy)

    pixel_to_cm_x = real_width_cm / frame_width
    pixel_to_cm_y = real_height_cm / frame_height
    pixel_to_cm = (pixel_to_cm_x + pixel_to_cm_y) / 2

    total_distance_cm = total_pixel_distance * pixel_to_cm
    return total_distance_cm


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'outputs', 'data')
    videos_dir = os.path.join(base_dir, 'videos')
    output_summary_csv = os.path.join(base_dir, 'outputs', 'distance_summary.csv')

    if not os.path.exists(data_dir):
        print(f"Data directory not found: {data_dir}")
        return
    if not os.path.exists(videos_dir):
        print(f"Videos directory not found: {videos_dir}")
        return

    # Get all CSV files in data directory
    csv_files = [f for f in os.listdir(data_dir) if f.lower().endswith('.csv')]
    if not csv_files:
        print("No CSV files found in data directory.")
        return

    results = []

    for csv_file in csv_files:
        video_name, _ = os.path.splitext(csv_file)
        video_file = video_name + '.mp4'
        csv_path = os.path.join(data_dir, csv_file)
        video_path = os.path.join(videos_dir, video_file)

        if not os.path.exists(video_path):
            print(f"Warning: Video file not found for CSV {csv_file}: expected {video_file}. Skipping.")
            continue

        print(f"Processing video: {video_file}")
        distance_cm = calculate_total_distance(csv_path, video_path)

        if distance_cm is not None:
            results.append([video_name, f"{distance_cm:.2f}"])
        else:
            results.append([video_name, "Error"])

    # Write summary CSV
    os.makedirs(os.path.join(base_dir, 'outputs'), exist_ok=True)
    with open(output_summary_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Video', 'Total Distance (cm)'])
        writer.writerows(results)

    print(f"\nSummary written to {output_summary_csv}")

if __name__ == "__main__":
    main()
