Distance Analysis
==================

How It Works
~~~~~~~~~~~~

FishTracker converts pixel distances to real-world centimeters using:

1. **Pixel distances** — Calculated from centroid coordinates in video
2. **Arena calibration** — User provides tank width and height (cm)
3. **Conversion** — ``distance_cm = distance_px × (arena_cm / frame_px)``

The conversion assumes isotropic scaling (same scale in X and Y directions).

Customizing Arena Dimensions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 28 cm × 14 cm (our validation setup)

Edit ``distance_calculator.py``:

.. code-block:: python

   def calculate_total_distance(
       csv_path: str,
       video_path: str,
       real_width_cm: float = 28,  # ← Change to your tank width
       real_height_cm: float = 14,  # ← Change to your tank height
       ...
   ) -> Optional[float]:

Interpreting Results
~~~~~~~~~~~~~~~~~~~~

``distance_summary.csv`` contains total distance traveled per video in centimeters.

Example:

.. code-block:: csv

   Video,Total Distance (cm)
   exp_001,42.5
   exp_002,38.2

This means the fish in exp_001 traveled 42.5 cm in total.

Common Questions
~~~~~~~~~~~~~~~~

**Q: Why are my distances much larger/smaller than expected?**
   A: Check arena dimensions in distance_calculator.py. Ensure they match your actual tank.

**Q: Should I calibrate with a ruler?**
   A: Yes, measure your tank's actual width and height to ensure accuracy.

**Q: Does resolution affect distance calculation?**
   A: Resolution indirectly affects it through video frame dimensions. Higher resolution = more precise pixel detection.
