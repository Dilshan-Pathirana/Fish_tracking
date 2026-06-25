Quick Start Guide
=================

Installation (5 minutes)
~~~~~~~~~~~~~~~~~~~~~~~~

**Step 1: Clone the repository**

.. code-block:: bash

   git clone https://github.com/Dilshan-Pathirana/Fish_tracking.git
   cd Fish_tracking

**Step 2: Install Python dependencies**

Option A: **Using pip with requirements.txt** (simplest)

.. code-block:: bash

   pip install -r requirements.txt

Option B: **Using pip with modern packaging** (recommended for development)

.. code-block:: bash

   pip install -e .

**Step 3: Verify installation**

.. code-block:: bash

   python main.py  # Launch GUI

If a window appears with "Fish Tracker" title, installation is successful!

Getting Started: GUI Mode (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**For beginners** — No command line knowledge required.

1. **Launch the application:**

   .. code-block:: bash

      python main.py

2. **In the GUI window:**

   - Click **"Browse"** next to "Select Video Folder" and choose a folder containing your video files
   - Click **"Browse"** next to "Select Output Folder" and choose where to save results
   - Click **"Start Tracking"** — watch progress in the status box
   - After tracking completes, click **"Calculate Distance Summary"**
   - Results are saved in your output folder

3. **Check your results:**

   - ``outputs/data/`` — CSV files with per-frame timestamps and centroid coordinates
   - ``outputs/heatmaps/`` — PNG images showing trajectory density
   - ``outputs/distance_summary.csv`` — Total distance for each video

Getting Started: Command Line (Batch Mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**For advanced users** — Process multiple videos in one command.

.. code-block:: bash

   python No_GUI.py /path/to/videos /path/to/outputs

Results are automatically saved to ``/path/to/outputs/``.

Example with real paths:

.. code-block:: bash

   # Windows
   python No_GUI.py "C:\Videos\experiment1" "C:\Results\exp1_output"

   # Linux/Mac
   python No_GUI.py ~/Videos/experiment1 ~/Results/exp1_output

Getting Started: Single-Video Debug Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**For troubleshooting** — Test tracking on one video with ROI selection.

.. code-block:: bash

   python single_run.py /path/to/video.mp4

Steps:

1. A window will appear showing your first video frame
2. **Draw a rectangle** around your fish tank using your mouse
3. Press **ENTER** or **SPACE** to confirm selection
4. Watch live tracking with FPS display
5. Press **q** to quit or **p** to pause/resume

This mode helps you:

- Verify the tracker detects your animal
- Adjust parameters if detection fails (edit the code)
- Understand tracking behavior before batch processing

Understanding Output Files
~~~~~~~~~~~~~~~~~~~~~~~~~~

**CSV Format** (``outputs/data/video_name.csv``)

.. code-block:: csv

   Time_hh:mm:ss:ms,Centroid_X,Centroid_Y
   00:00:00:000,152,243
   00:00:00:033,154,245
   00:00:00:066,157,248

- **Time_hh:mm:ss:ms**: Elapsed time (HH:MM:SS:milliseconds)
- **Centroid_X, Centroid_Y**: Pixel coordinates of detected animal

**Heatmap** (``outputs/heatmaps/video_name.png``)

- Shows where the animal spent most time (red = most visited)
- Overlaid on the final video frame
- Helps visualize movement patterns

**Distance Summary** (``outputs/distance_summary.csv``)

.. code-block:: csv

   Video,Total Distance (cm)
   experiment_001,42.5
   experiment_002,38.2

- Total distance traveled **in real-world centimeters**
- Assumes you provide correct tank dimensions

Customizing for Your Arena
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, FishTracker assumes a **28 cm × 14 cm** tank (our validation setup).

**To use a different tank size:**

Edit ``distance_calculator.py`` and change:

.. code-block:: python

   def calculate_total_distance(
       csv_path: str,
       video_path: str,
       real_width_cm: float = 28,    # ← Change this
       real_height_cm: float = 14,   # ← Change this
       frame_skip: int = 60
   ) -> Optional[float]:

Or pass parameters directly:

.. code-block:: python

   from distance_calculator import calculate_total_distance

   distance = calculate_total_distance(
       csv_path="tracking.csv",
       video_path="video.mp4",
       real_width_cm=50,  # Your tank width
       real_height_cm=30  # Your tank height
   )

Troubleshooting
~~~~~~~~~~~~~~~

**"No video files found"**
   - Ensure your video folder contains .mp4, .avi, or .mov files
   - Check folder path is correct

**"Tracker loses the fish"**
   - Use debug mode: ``python single_run.py``
   - Ensure good lighting and contrast between animal and background
   - Consider background subtraction threshold values in ``utils/tracker.py``

**"Distance values seem wrong"**
   - Verify tank dimensions in ``distance_calculator.py``
   - Check video resolution matches your physical setup
   - Test with a known distance first

**GUI doesn't appear**
   - Linux users: May need ``sudo apt-get install python3-tk``
   - Ensure Python is correctly installed

**Import errors (ModuleNotFoundError)**
   - Reinstall dependencies: ``pip install -r requirements.txt``
   - Ensure you're in the Fish_tracking directory

Next Steps
~~~~~~~~~~

- 📖 Read the :doc:`usage` guide for detailed instructions
- 🔧 Check :doc:`architecture` to understand how the tracking works
- 🐛 If something doesn't work, see :doc:`faq`
- 💻 Want to contribute? See :doc:`contributing`

For help with a specific issue, open an issue on `GitHub Issues <https://github.com/Dilshan-Pathirana/Fish_tracking/issues>`_.
