API Reference
=============

Core Modules
~~~~~~~~~~~~

utils.tracker
^^^^^^^^^^^^^

.. automodule:: utils.tracker
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

distance_calculator
^^^^^^^^^^^^^^^^^^^

.. automodule:: distance_calculator
   :members:
   :undoc-members:
   :show-inheritance:

tracker_wrapper
^^^^^^^^^^^^^^^

.. automodule:: tracker_wrapper
   :members:
   :undoc-members:
   :show-inheritance:

GUI and CLI Modules
~~~~~~~~~~~~~~~~~~~

main
^^^^

.. automodule:: main
   :members:
   :undoc-members:
   :show-inheritance:

No_GUI
^^^^^^

.. automodule:: No_GUI
   :members:
   :undoc-members:
   :show-inheritance:

single_run
^^^^^^^^^^

.. automodule:: single_run
   :members:
   :undoc-members:
   :show-inheritance:

Data Structures
~~~~~~~~~~~~~~~

FishTracker Output Formats
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Centroid CSV Format**

Generated at: ``outputs/data/<video_name>.csv``

.. code-block:: csv

   Time_hh:mm:ss:ms,Centroid_X,Centroid_Y
   00:00:00:000,100,150
   00:00:00:033,102,152
   00:00:00:066,105,155

Fields:

- **Time_hh:mm:ss:ms**: Elapsed time in format HH:MM:SS:milliseconds
- **Centroid_X**: Horizontal centroid position in pixels
- **Centroid_Y**: Vertical centroid position in pixels

**Distance Summary CSV Format**

Generated at: ``outputs/distance_summary.csv``

.. code-block:: csv

   Video,Total Distance (cm)
   video_01,45.23
   video_02,38.91

Fields:

- **Video**: Video filename (without extension)
- **Total Distance (cm)**: Total distance traveled in centimeters

**Heatmap Output**

Generated at: ``outputs/heatmaps/<video_name>.png``

- Format: PNG image with JET colormap
- Content: Gaussian-blurred trajectory density overlaid on final video frame
- Colors: Blue (low density) → Red (high density)

Constants and Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Key Parameters (editable in code)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Background Subtraction**

.. code-block:: python

   # In utils/tracker.py, FishTracker.__init__()
   self.fgbg = cv2.createBackgroundSubtractorMOG2(
       history=500,          # Number of frames to learn background
       varThreshold=16,      # Variance threshold for background model
       detectShadows=True    # Detect and suppress shadows
   )

**Contour Detection**

.. code-block:: python

   # In utils/tracker.py, process_frame()
   min_contour_area = 500  # Minimum pixel area to consider as animal

**Short-Gap Interpolation**

.. code-block:: python

   # In utils/tracker.py, __init__()
   self.max_no_movement_frames = 10  # Max frames to hold last bounding box

**Heatmap Generation**

.. code-block:: python

   # In utils/tracker.py, save_results()
   cv2.GaussianBlur(heatmap, (51, 51), 0)  # Kernel size for blur
   cv2.circle(heatmap, (x, y), radius=3, ...)  # Circle radius for each point

**Distance Calibration**

.. code-block:: python

   # Default arena dimensions (in distance_calculator.py)
   real_width_cm = 28   # Tank width in centimeters
   real_height_cm = 14  # Tank height in centimeters

Type Hints
~~~~~~~~~~

All modules use full type hints compatible with Python 3.8+:

.. code-block:: python

   from typing import Optional, List, Tuple

   def calculate_distance(
       points: List[Tuple[int, int]],
       scale: float = 1.0
   ) -> Optional[float]:
       """Calculate total distance from centroid points."""
       ...

Common Patterns
~~~~~~~~~~~~~~~

Processing a Single Video
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from utils.tracker import FishTracker

   # Initialize tracker
   tracker = FishTracker(
       video_path="path/to/video.mp4",
       output_dir="path/to/outputs",
       show_window=False
   )

   # Run tracking
   tracker.run()

   # Save results
   tracker.save_results()

Batch Processing Multiple Videos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from tracker_wrapper import process_video
   import concurrent.futures

   videos = ["video1.mp4", "video2.mp4", "video3.mp4"]
   output_dir = "outputs"

   with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
       futures = [executor.submit(process_video, v, output_dir) for v in videos]
       for future in concurrent.futures.as_completed(futures):
           result = future.result()
           print(result)

Calculating Distance
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from distance_calculator import calculate_total_distance, calculate_summary

   # Single video
   distance = calculate_total_distance(
       csv_path="outputs/data/video.csv",
       video_path="video.mp4",
       real_width_cm=28,  # Your tank width
       real_height_cm=14   # Your tank height
   )
   print(f"Total distance: {distance:.2f} cm")

   # Batch summary
   summary_path = calculate_summary(
       output_root="outputs",
       videos_dir="path/to/videos"
   )
   print(f"Summary saved to: {summary_path}")
