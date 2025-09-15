# Fish Tracking System

## Overview

A robust, automated fish tracking solution for scientific research and aquaculture, featuring computer vision, batch processing, and a user-friendly GUI. Tracks fish movement, generates heatmaps, and computes real-world distance metrics from video data.

---

## Table of Contents

- Features
- Project Structure
- Installation
- Usage
  - GUI Mode
  - Batch Mode
  - Single Run Mode
- Inputs & Outputs
- Requirements
- Contributing
- License
- Author

---

## Features
- **Automated Fish Tracking:** Computer vision-based tracking with background subtraction, robust to occlusion and inactivity.
- **Batch Processing:** Parallelized video analysis for large datasets using `concurrent.futures`.
- **GUI Application:** Desktop interface for folder selection, progress tracking, and operation.
- **Heatmap Generation:** Visual overlays of fish trajectories for each video.
- **Distance Analysis:** Computes real-world movement from tracked centroids; outputs summary CSVs.
- **Configurable Workflow:** Customizable video folders, output locations, and tank dimensions.

---

## Project Structure
| Path                   | Purpose                                              |
|------------------------|------------------------------------------------------|
| tracker.py     | Core object detection and tracking class             |
| distance_calculator.py| Movement calculation and summary utilities           |
| tracker_wrapper.py   | Unified video processing bridge for batch/GUI modes  |
| gui.py / main.py   | GUI desktop application                              |
| No_GUI.py            | CLI batch runner (multithreaded)                     |
| single_run.py        | Interactive tracking/debug for single video          |
| videos              | Raw input video files                                |
| outputs             | Result files: CSV, heatmaps, logs                    |
| requirements.txt     | Python library dependencies                          |
| README.md            | Project documentation                                |

---

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/Dilshan-Pathirana/fish-tracking.git
cd fish-tracking
```

### 2. Set Up Python Environment
- **Python 3.7+ required**
```sh
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

---

## Usage

### GUI Mode
Start the graphical application:
```sh
python gui.py
# or
python main.py
```
- Select the video folder and output folder.
- Press **Start Tracking** to begin.
- Use **Calculate Distance Summary** for summary metrics.

### Batch Mode
Run batch processing (no GUI):
```sh
python No_GUI.py [video_directory] [output_directory]
```
- Requires at least two arguments, or set paths inside the script.

### Single Run Mode
Track a single video interactively:
```sh
python single_run.py
```
- Follow the ROI selection prompt for the fish tank region.

---

## Inputs & Outputs
| Type           | Details                                                        |
|----------------|----------------------------------------------------------------|
| Input Videos   | Supported formats: `.mp4`, `.avi`, `.mov` (place in videos) |
| CSV Output     | Centroid tracking data per video (data): Time, X, Y |
| Heatmap Images | Overlay images of fish paths (heatmaps): PNG format |
| Summary CSV    | Distance traveled summary for all processed videos (distance_summary.csv) |
| Logs           | Batch logs (timestamped) per run (`outputs/batch_log_*.txt`)   |

---

## Requirements
- **Python:** 3.7+
- **Libraries:**
  - `opencv-python>=4.7.0`
  - `numpy>=1.21.0`
  - `tkinter` (standard, no installation needed)
  - `concurrent.futures` (bundled from Python 3.2+)
  - `pyinstaller` (optional, for packaging GUI as executable)

> **Note:** If packaging with PyInstaller, ensure plugin inclusion for Tkinter.

---

## Contributing
- Follow [PEP-8](https://peps.python.org/pep-0008/) style guide.
- Write clear comments for scientific code ([Ten Simple Rules for Documenting Scientific Software](https://doi.org/10.1371/journal.pcbi.1006561)).
- Submit issues and feature requests via [GitHub Issues](https://github.com/Dilshan-Pathirana/fish-tracking/issues).
- For significant changes, open pull requests with code reviews.

---

## Author
Made by [Dilshan Pathirana](https://github.com/Dilshan-Pathirana)

---

## Additional Notes
- `Tkinter` is built-in with standard Python distributions (no pip needed).
- If GUI packaging is desired, add `pyinstaller` as an optional dependency.
- To regenerate requirements.txt from imports, use:
  ```sh
  pipreqs .
  ```

---