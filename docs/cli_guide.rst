CLI User Guide
===============

Usage: ``python No_GUI.py <video_dir> <output_dir>``

Example
~~~~~~~

.. code-block:: bash

   python No_GUI.py ./videos ./outputs

This processes all .mp4, .avi, .mov files in ``./videos`` and saves results to ``./outputs``.

Output Files
~~~~~~~~~~~~

- ``outputs/data/`` — CSV centroid data
- ``outputs/heatmaps/`` — PNG heatmap images
- ``outputs/distance_summary.csv`` — Batch distance results
- ``outputs/batch_log_YYYY-MM-DD_HH-MM-SS.txt`` — Processing log

Options
~~~~~~~

Currently no command-line options. To customize:

- Tank dimensions: Edit ``distance_calculator.py``
- Detection thresholds: Edit ``utils/tracker.py``
