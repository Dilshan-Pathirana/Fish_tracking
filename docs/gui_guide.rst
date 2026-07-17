GUI User Guide
===============

Launching the GUI
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python main.py

A window titled "FishTracker" will appear with a themed, responsive layout.

Workflow
~~~~~~~~

1. **Select folders** — Browse to a video folder (MP4/AVI/MOV) and an output folder.
2. **Calibrate arena** — Enter the real-world width/height (cm) of the tank visible in
   frame. Defaults to 28 x 14 cm; change this before starting if your tank differs.
3. **Start Tracking** — Videos are processed in parallel on a background thread, so the
   window stays responsive throughout. A progress bar, per-video count, and estimated
   time remaining update live as each video finishes.
4. **Cancel** — Available while tracking is running; stops the batch after in-flight
   videos complete, without corrupting already-saved results.
5. **Distance summary** — Calculated automatically once tracking completes, using the
   calibration values entered in step 2. You can also trigger it manually at any time
   with **Calculate Distance Summary** (e.g. to recompute with different calibration
   without re-running tracking).
6. **Check results** — Use **Open Output Folder** to jump straight to the CSVs,
   heatmaps, and summary file.

Theme
~~~~~

Toggle light/dark mode from the header. Your choice, along with the last-used folders
and calibration values, is saved automatically and restored the next time you launch
the app.

Activity Log
~~~~~~~~~~~~

The log panel is color-coded:

- Green — a video succeeded
- Red — a video failed (hover/read the message for the underlying error)
- Amber — a warning (e.g. batch cancelled)
- Muted — informational messages

A timestamped log file is also written to the output folder automatically. Check this
file if you need to review results after closing the app.

Progress
~~~~~~~~

The progress bar and label reflect real per-video completion (not per-batch), including
a live estimated-time-remaining based on the average time per video so far.
