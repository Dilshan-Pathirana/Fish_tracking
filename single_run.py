import cv2
import time
import numpy as np

class SimpleFishTracker:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        self.last_bbox = None
        self.no_movement_frames = 0
        self.max_no_movement_frames = 90
        self.trail = []
        self.prev_gray = None
        self.roi = None  # (x, y, w, h)

    def select_roi(self):
        print("🖱️ Select the ROI (fish tank area), then press ENTER or SPACE.")
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Couldn't read frame to select ROI.")

        # Resize window for selection
        frame_resized = frame.copy()
        cv2.namedWindow("Select ROI", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Select ROI", 1024, 768)

        self.roi = cv2.selectROI("Select ROI", frame_resized, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select ROI")

        if self.roi == (0, 0, 0, 0):
            raise ValueError("No ROI selected!")

        print(f"✅ ROI selected: {self.roi}")
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to first frame after ROI selection

    def process_frame(self, frame):
        x, y, w, h = self.roi
        roi_frame = frame[y:y+h, x:x+w]
        gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

        # Detect dark objects
        _, dark_mask = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)

        if self.prev_gray is None:
            self.prev_gray = gray.copy()
            return frame  # Skip first frame

        # Detect motion
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        frame_diff = cv2.absdiff(blurred, self.prev_gray)
        _, motion_mask = cv2.threshold(frame_diff, 1, 255, cv2.THRESH_BINARY)

        # Combine masks
        combined_mask = cv2.bitwise_and(dark_mask, motion_mask)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detected = False
        cx, cy = -1, -1

        for cnt in contours:
            if cv2.contourArea(cnt) < 200:
                continue
            rx, ry, rw, rh = cv2.boundingRect(cnt)
            cx, cy = rx + rw // 2, ry + rh // 2

            # Convert ROI coordinates back to full-frame
            abs_cx, abs_cy = cx + x, cy + y
            abs_box = (rx + x, ry + y, rw, rh)
            cv2.rectangle(frame, (abs_box[0], abs_box[1]),
                          (abs_box[0] + rw, abs_box[1] + rh), (0, 255, 0), 2)

            self.last_bbox = abs_box
            detected = True
            break

        # Fallback: track still fish (dark object only)
        if not detected:
            _, dark_mask_full = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
            fallback_contours, _ = cv2.findContours(dark_mask_full, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in fallback_contours:
                if cv2.contourArea(cnt) < 300:
                    continue
                x_dark, y_dark, w_dark, h_dark = cv2.boundingRect(cnt)
                cx, cy = x_dark + w_dark // 2, y_dark + h_dark // 2

                # Convert to full-frame coordinates
                abs_x, abs_y = x_dark + x, y_dark + y
                cv2.rectangle(frame, (abs_x, abs_y), (abs_x + w_dark, abs_y + h_dark), (0, 255, 255), 2)

                self.last_bbox = (abs_x, abs_y, w_dark, h_dark)
                detected = True
                break

        # Draw trail
        if cx != -1 and cy != -1:
            self.trail.append((cx + x, cy + y))
            if len(self.trail) > 50:
                self.trail.pop(0)

        for point in self.trail:
            cv2.circle(frame, point, 2, (0, 255, 255), -1)

        # Draw the selected ROI on top
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Update previous
        self.prev_gray = gray.copy()

        return frame

    def run(self):
        self.select_roi()

        window_name = "Simple Fish Tracker (ROI)"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 1024, 768)

        while self.cap.isOpened():
            start_time = time.time()
            ret, frame = self.cap.read()
            if not ret:
                break

            processed = self.process_frame(frame)

            # Show FPS
            fps = 1 / (time.time() - start_time + 1e-5)
            cv2.putText(processed, f"FPS: {fps:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            cv2.imshow(window_name, processed)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'):
                print("⏸ Paused. Press 'p' again to resume.")
                while True:
                    if cv2.waitKey(0) & 0xFF == ord('p'):
                        print("▶️ Resumed.")
                        break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "videos/20.mp4"  # 🔁 Replace with your video file
    tracker = SimpleFishTracker(video_path)
    tracker.run()
