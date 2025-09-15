# 🐟 Fish Tracking System

An AI-powered solution for aquaculture and scientific research, tracking fish movements in real time from video data. Supports heatmap generation, distance analysis, and batch video processing with both GUI and CLI modes.

---

## 🚀 Features

🎥 **Automated Tracking** — Computer vision with background subtraction, robust to occlusion and inactivity.
⚡ **Batch Processing** — Parallelized video analysis for large datasets using `concurrent.futures`.
🖥️ **GUI Application** — Desktop interface for easy folder selection, progress tracking, and control.
🔥 **Heatmap Generation** — Overlay fish trajectories on each video as visual heatmaps.
📏 **Distance Analysis** — Compute real-world distance metrics from tracked centroids, export to CSV.
⚙️ **Configurable Workflow** — Flexible setup for video folders, output locations, and tank dimensions.

---

## 🏗️ Tech Stack

**Computer Vision & Backend**

* Python (3.7+)
* OpenCV — Video and tracking
* NumPy — Data processing
* Tkinter — GUI framework
* concurrent.futures — Parallelized batch runs

**Optional Packaging**

* PyInstaller — Build standalone GUI executables

---

## ⚙️ System Architecture

📂 **Project Structure (Planned)**

```
fish-tracking-system/
│
├── tracker.py             # Core object detection + tracking
├── distance_calculator.py # Movement calculations + CSV summary
├── tracker_wrapper.py     # Unified bridge for batch/GUI modes
├── gui.py / main.py       # GUI desktop app
├── No_GUI.py              # CLI batch runner (multithreaded)
├── single_run.py          # Interactive tracking/debug for single video
├── videos/                # Raw input video files
├── outputs/               # Results: CSV, heatmaps, logs
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

---

## 🎯 Use Case Scenario

🔬 **Aquaculture & Research Example:**

* Track fish activity across multiple tanks.
* Generate heatmaps of fish trajectories for behavioral analysis.
* Log real-world distances traveled for growth and stress studies.
* Export structured CSVs for scientific publications.

---

## 🚦 Roadmap

* ✅ Build tracking pipeline with background subtraction
* ✅ Add GUI support with Tkinter
* ✅ Implement batch + single video modes
* ✅ Enable heatmap and CSV export
* ⏳ Package GUI with PyInstaller
* ⏳ Add advanced analytics dashboards

---

## 🤝 Contributing

* Follow **PEP-8** style guidelines.
* Document scientific code (see *Ten Simple Rules for Documenting Scientific Software*).
* Open issues for bugs/features.
* Pull requests welcome with code reviews.

---

## 👤 Author

Made by **Dilshan Pathirana**

---
