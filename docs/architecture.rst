Architecture Overview
======================

System Architecture
~~~~~~~~~~~~~~~~~~~

::

    Video Input
        ↓
    [MOG2 Background Subtraction]
        ↓
    [Morphological Filtering (Close + Open)]
        ↓
    [Contour Detection & Analysis]
        ↓
    [Largest Contour → Centroid]
        ↓
    [Short-Gap Interpolation (hold last bbox for up to 10 frames)]
        ↓
    [CSV Export + Heatmap Generation]
        ↓
    [Distance Calculation via Pixel-to-CM Conversion]
        ↓
    Results (CSV + Heatmap + Distance Summary)

Core Modules
~~~~~~~~~~~~

**utils/tracker.py** — FishTracker class
   - Handles frame-by-frame processing
   - Background subtraction with MOG2
   - Centroid detection and logging
   - Heatmap and CSV export

**distance_calculator.py** — Distance analysis
   - Pixel-to-centimeter conversion
   - Per-video and batch distance summaries

**tracker_wrapper.py** — Video processing wrapper
   - Bridge between GUI/CLI and core tracker
   - Resource path resolution for PyInstaller

**main.py** — Tkinter GUI application
   - Interactive folder selection
   - Progress monitoring
   - Batch job execution

**No_GUI.py** — Command-line batch mode
   - Headless video processing
   - Parallel execution with ThreadPoolExecutor

**single_run.py** — Debug mode
   - Interactive ROI selection
   - Real-time visualization
   - Parameter testing

Key Algorithms
~~~~~~~~~~~~~~

1. **Background Subtraction (MOG2)**
   - Gaussian Mixture Model with 500-frame history
   - Shadow detection enabled
   - Variance threshold: 16

2. **Morphological Filtering**
   - Closing: Fill small holes in foreground
   - Opening: Remove small noise blobs

3. **Short-Gap Interpolation**
   - If no detection for ≤10 frames: use last known bounding box
   - Reduces track fragmentation during occlusion/inactivity

4. **Distance Calibration**
   - Pixel distance to real-world cm conversion
   - Uses video frame width/height and user-supplied tank dimensions
   - Assumes isotropic conversion (same scale in X and Y)

Performance Characteristics
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Speed**: ~30 FPS on modern laptop (Intel i5, 8GB RAM)
- **Memory**: ~200 MB per video in memory at once
- **Throughput**: ~10 videos in parallel with ThreadPoolExecutor
- **Accuracy**: Depends on contrast and lighting quality

Data Flow
~~~~~~~~~

1. **Input**: MP4/AVI/MOV video files
2. **Processing**: Frame-by-frame detection and logging
3. **Output**:
   - CSV: Per-frame centroid coordinates with timestamps
   - PNG: Heatmap overlaid on final frame
   - CSV: Batch distance summary

Dependencies
~~~~~~~~~~~~

Core:
   - OpenCV (cv2): Video reading, background subtraction, morphological operations
   - NumPy: Numerical arrays for image processing
   - Tkinter: GUI (usually bundled with Python)

Development:
   - pytest: Testing
   - mypy: Type checking
   - black: Code formatting
   - flake8: Linting
   - Sphinx: Documentation generation

Design Decisions
~~~~~~~~~~~~~~~~

1. **Single-animal only** — Simplified for common use case; multi-animal requires identity tracking
2. **No GPU requirement** — MOG2 efficient enough on CPU; target is resource-limited labs
3. **Background subtraction over deep learning** — No training step required
4. **Batch processing with threads** — GIL bypass with I/O-heavy operations
5. **Tkinter GUI** — No additional dependencies; cross-platform by default
