"""Interactive single-video debugging module with ROI selection.

Provides SimpleFishTracker for real-time tracking validation on new footage,
combining dark-object detection with motion detection for robust tracking
in challenging lighting conditions.
"""

import cv2
import time
import numpy as np
from typing import Optional, List, Tuple


class SimpleFishTracker:
    """Interactive fish tracker with ROI selection and real-time visualization.

    Combines threshold-based dark object detection with motion detection
    to robustly track stationary and moving animals. Allows user-defined
    ROI selection before processing and real-time visualization with
    pause/resume capability.
    """

    def __init__(self, video_path: str) -> None:
        """Initialize the simple tracker.

        Args:
            video_path: Path to the input video file.

        Raises:
            IOError: If video file cannot be opened.
        """
        self.video_path: str = video_path
        self.cap: cv2.VideoCapture = cv2.VideoCapture(video_path)

        self.last_bbox: Optional[Tuple[int, int, int, int]] = None
        self.no_movement_frames: int = 0
        self.max_no_movement_frames: int = 90
        self.trail: List[Tuple[int, int]] = []
        self.prev_gray: Optional[np.ndarray] = None
        self.roi: Optional[Tuple[int, int, int, int]] = None

    def select_roi(self) -> None:
        """Interactively select region of interest (ROI) from first frame.

        Displays first frame and allows user to select a rectangular ROI
        using mouse. Resets video to frame 0 after selection.

        Raises:
            RuntimeError: If first frame cannot be read.
            ValueError: If user closes ROI selector without selecting a region.
        """
        print("🖱️ Select the ROI (fish tank area), then press ENTER or SPACE.")
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Couldn't read frame to select ROI.")

        frame_resized = frame.copy()
        cv2.namedWindow("Select ROI", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Select ROI", 1024, 768)

        self.roi = cv2.selectROI("Select ROI", frame_resized, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select ROI")

        if self.roi == (0, 0, 0, 0):
            raise ValueError("No ROI selected!")

        print(f"✅ ROI selected: {self.roi}")
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process a single frame to detect and track the animal within ROI.

        Uses combined dark-object and motion detection within the selected ROI.
        Falls back to dark-object-only detection if motion detection fails.
        Maintains a visual trail of detected positions.

        Args:
            frame: Input video frame (BGR format).

        Returns:
            Annotated frame with ROI, bounding box, and trail visualization.
        """
        if self.roi is None:
            raise RuntimeError("ROI not selected. Call select_roi() first.")

        x, y, w, h = self.roi
        roi_frame = frame[y:y+h, x:x+w]
        gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

        _, dark_mask = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)

        if self.prev_gray is None:
            self.prev_gray = gray.copy()
            return frame

        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        frame_diff = cv2.absdiff(blurred, self.prev_gray)
        _, motion_mask = cv2.threshold(frame_diff, 1, 255, cv2.THRESH_BINARY)

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

            abs_cx, abs_cy = cx + x, cy + y
            abs_box = (rx + x, ry + y, rw, rh)
            cv2.rectangle(frame, (abs_box[0], abs_box[1]),
                          (abs_box[0] + rw, abs_box[1] + rh), (0, 255, 0), 2)

            self.last_bbox = abs_box
            detected = True
            break

        if not detected:
            _, dark_mask_full = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
            fallback_contours, _ = cv2.findContours(dark_mask_full, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in fallback_contours:
                if cv2.contourArea(cnt) < 300:
                    continue
                x_dark, y_dark, w_dark, h_dark = cv2.boundingRect(cnt)
                cx, cy = x_dark + w_dark // 2, y_dark + h_dark // 2

                abs_x, abs_y = x_dark + x, y_dark + y
                cv2.rectangle(frame, (abs_x, abs_y), (abs_x + w_dark, abs_y + h_dark), (0, 255, 255), 2)

                self.last_bbox = (abs_x, abs_y, w_dark, h_dark)
                detected = True
                break

        if cx != -1 and cy != -1:
            self.trail.append((cx + x, cy + y))
            if len(self.trail) > 50:
                self.trail.pop(0)

        for point in self.trail:
            cv2.circle(frame, point, 2, (0, 255, 255), -1)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        self.prev_gray = gray.copy()

        return frame

    def run(self) -> None:
        """Process and display video with real-time tracking.

        Displays annotated video frames with tracking visualization.
        Controls:
            - q: Quit
            - p: Pause/resume playback
        """
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

def main() -> None:
    """Entry point for the interactive single-video debug mode.

    Allows user to select a video file and track with ROI selection.
    """
    import sys

    if len(sys.argv) >= 2:
        video_path = sys.argv[1]
    else:
        print("Usage: fish-tracker-debug <video_file>")
        print("\nExample: fish-tracker-debug ./videos/sample.mp4")
        sys.exit(1)

    try:
        tracker = SimpleFishTracker(video_path)
        tracker.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
