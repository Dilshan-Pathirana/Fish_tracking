<img width="1376" height="768" alt="Picsart_26-07-04_13-14-29-916" src="https://github.com/user-attachments/assets/d8e98ba4-6b55-40f2-9a20-e8362c9f8762" />
# FishTracker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A lightweight, open-source Python tool for tracking a single moving animal in laboratory video recordings, quantifying its movement, and generating space-use heatmaps — with both a GUI and a batch command-line mode.

---

## Statement of need

Behavioural researchers working with small aquatic animals (fish, amphibian larvae, aquatic invertebrates) in single-subject laboratory assays (open-field, novel-object, mirror tests, etc.) often need only **single-individual centroid tracking** — not multi-animal identity tracking or full pose estimation. Existing high-capability tools (idtracker.ai, TRex, DeepLabCut) are built for multi-animal or markerless-pose problems and typically require GPU acceleration, model training, or a steeper setup process; commercial alternatives (e.g. EthoVision XT) carry licensing costs that are prohibitive for many student and resource-limited labs.

FishTracker fills the gap between "manual stopwatch/grid scoring" and these heavier pipelines: it runs on a standard laptop with no GPU or trained model, processes many videos in parallel out of the box, and outputs analysis-ready CSVs and heatmaps with a two-click GUI (or a one-line CLI command for larger batches).

---

## Features

- 🎥 **Automated single-subject tracking** — background subtraction (MOG2) with short-gap interpolation, robust to brief occlusion or inactivity.
- ⚡ **Batch processing** — parallelized multi-video analysis via `concurrent.futures`.
- 🖥️ **GUI application** — folder selection, live progress bar, and run log, no command line required.
- 🔥 **Heatmap generation** — Gaussian-blurred trajectory heatmap overlaid on the source frame for each video.
- 📏 **Distance analysis** — converts pixel-space centroid displacement into real-world distance (cm), exported to CSV, using user-supplied arena dimensions.
- ⚙️ **CLI batch mode** — scriptable, no GUI dependency, suited to headless/server use.

---

## Installation

Requires Python 3.8+.

```bash
git clone https://github.com/Dilshan-Pathirana/Fish_tracking.git
cd Fish_tracking
pip install -r requirements.txt
```

On Linux, `tkinter` is sometimes not bundled with Python and may need a separate install:

```bash
sudo apt-get install python3-tk
```

---

## Usage

### GUI mode

```bash
python main.py
```

A modern, non-blocking desktop UI with light/dark themes:

1. **Select folders** — browse to your video folder and an output folder.
2. **Calibrate arena** — enter the real-world width/height (cm) of the tank visible in frame (defaults to 28 × 14 cm).
3. Click **Start Tracking** — videos process in parallel in the background while the UI stays responsive; a live progress bar, per-video ETA, and color-coded activity log show status. Use **Cancel** to stop a running batch.
4. The distance summary is calculated automatically once tracking finishes (or run it manually any time with **Calculate Distance Summary**).

Your folder selections, calibration values, and theme choice are remembered between sessions.

### Batch / CLI mode

```bash
python No_GUI.py <video_folder> <output_folder>
```

Processes all `.mp4` / `.avi` / `.mov` files in `video_folder` in parallel batches of 10, writes a timestamped log, and runs the distance summary automatically.

### Single-video debug mode

```bash
python single_run.py
```

Lets you manually select a region of interest (ROI) and watch the tracker run live — useful for tuning detection thresholds on a new tank/lighting setup before a full batch run.

---

## Output

For each input video `<name>.mp4`:

| File | Description |
|---|---|
| `outputs/data/<name>.csv` | Per-frame timestamp (`hh:mm:ss:ms`) and centroid pixel coordinates (`Centroid_X`, `Centroid_Y`) |
| `outputs/heatmaps/<name>.png` | Trajectory heatmap (JET colormap) overlaid on the final video frame |
| `outputs/distance_summary.csv` | Total distance travelled (cm) per video, after pixel→cm calibration |

---

## Calibrating to your own arena

Distance conversion assumes a known real-world arena size (default: 28 × 14 cm, the tank dimensions used in our validation case study — see `paper.md`). In the GUI, set **Width (cm)** / **Height (cm)** in the calibration section before starting a run. In CLI/batch mode, pass `real_width_cm` / `real_height_cm` to `calculate_total_distance()` / `calculate_summary()` in `distance_calculator.py`, or edit the defaults directly.

---

## How it works

1. **Background subtraction** (`cv2.createBackgroundSubtractorMOG2`) isolates the moving animal from a static tank background.
2. **Morphological closing + opening** removes small noise blobs from the foreground mask.
3. The **largest qualifying contour** (area > 500 px) is taken as the tracked animal; its centroid is logged.
4. If detection briefly fails (animal stationary or occluded), the **last known bounding box is held** for up to 10 frames before the track is allowed to drop, reducing fragmentation during inactivity.

---

## Limitations

- **Single-individual tracking only.** Not designed for multi-animal arenas without manual video partitioning.
- Assumes one subject with reasonable contrast against a comparatively static background; heavy reflections, multiple moving shadows, or very low contrast will degrade detection.
- No cross-video re-identification — each video is tracked independently.

If you need multi-animal identity tracking or markerless pose estimation, consider **idtracker.ai**, **TRex**, or **DeepLabCut** instead — see `paper.md` for a fuller comparison.

---

## Project structure

```
Fish_tracking/
│
├── utils/tracker.py        # Core detection + tracking + heatmap/CSV export
├── distance_calculator.py  # Pixel→cm conversion + summary CSV
├── tracker_wrapper.py      # Bridge between batch/GUI modes and the tracker
├── main.py                  # Tkinter/ttk GUI application
├── No_GUI.py                # CLI batch runner (multithreaded)
├── single_run.py            # Interactive ROI-based debug mode
├── requirements.txt
├── paper.md / paper.bib     # JOSS submission
└── README.md
```

---

## Roadmap

- [x] Background-subtraction tracking pipeline
- [x] GUI (Tkinter)
- [x] Batch + single-video modes
- [x] Heatmap + CSV export
- [x] OSI license (MIT)
- [ ] Automated test suite
- [ ] Zenodo-archived release (citable DOI)
- [ ] Optional Kalman-filter smoothing for noisier footage

---

## Citing this software

If you use FishTracker in published work, please cite the JOSS paper (`paper.md`) — see `CITATION.cff` once archived, or cite the GitHub repository directly in the meantime:

> Pathirana, D. (2025). *FishTracker: a lightweight, open-source tool for video tracking and space-use quantification of single aquatic animals in laboratory assays* [Software]. https://github.com/Dilshan-Pathirana/Fish_tracking

---

## Contributing

Pull requests are welcome. Please follow PEP 8 and document scientific code per *Ten Simple Rules for Documenting Scientific Software* (Lee et al., 2018, PLOS Computational Biology). Open an issue for bugs or feature requests before submitting a large PR.

---

## License

MIT — see [LICENSE](LICENSE).

## Author

**Dilshan Pathirana** — [github.com/Dilshan-Pathirana](https://github.com/Dilshan-Pathirana)
