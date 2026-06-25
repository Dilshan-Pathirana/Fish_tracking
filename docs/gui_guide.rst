GUI User Guide
===============

Launching the GUI
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python main.py

A window titled "Fish Tracker" will appear with buttons and folder selection fields.

Workflow
~~~~~~~~

1. **Select Video Folder** — Click "Browse" and choose folder containing MP4/AVI/MOV files
2. **Select Output Folder** — Click "Browse" and choose where to save results
3. **Start Tracking** — Click button; watch progress bar and status messages
4. **Calculate Distance** — Click button after tracking completes
5. **Check Results** — Open output folder to view CSV, heatmaps, and summary

Status Messages
~~~~~~~~~~~~~~~

- ✅ — Success
- ❌ — Error or failure
- 🔍 — Searching for files
- ▶️ — Starting batch
- ✔️ — Batch completed
- 📏 — Calculating distances

Progress Bar
~~~~~~~~~~~~

Shows percentage completion during batch processing. Updates after each batch of 10 videos.

Log File
~~~~~~~~

A timestamped log file is created in the output folder automatically. Check this file if errors occur.
