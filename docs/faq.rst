Frequently Asked Questions
===========================

General Questions
~~~~~~~~~~~~~~~~~

**Q: What animals can FishTracker track?**
   A: Any small aquatic animal with sufficient contrast against the background: fish, tadpoles, shrimp, etc. Tested on fish and amphibian larvae.

**Q: Can it track multiple animals?**
   A: No, FishTracker is designed for single-subject tracking. For multi-animal tracking, consider idtracker.ai or TRex.

**Q: Do I need a GPU?**
   A: No. FishTracker uses CPU-based background subtraction (MOG2), which is efficient enough for real-time processing on modern laptops.

**Q: Can it track in the dark?**
   A: Background subtraction works best with adequate lighting. Infrared lighting can help with nocturnal animals.

**Q: What video formats are supported?**
   A: MP4, AVI, and MOV files. Ensure your codec is OpenCV-compatible.

Technical Questions
~~~~~~~~~~~~~~~~~~~~

**Q: How accurate is the tracking?**
   A: Depends on video quality, lighting, and arena contrast. A validation study comparing manual vs. automated tracking is in progress (see manuscript_skeleton_option_C.md).

**Q: Can I use different arena dimensions?**
   A: Yes. Edit the ``real_width_cm`` and ``real_height_cm`` parameters in ``distance_calculator.py``.

**Q: What's the frame rate requirement?**
   A: Works at any frame rate (30 fps, 60 fps, etc.). Lower frame rates may miss rapid movements.

**Q: How do I customize detection parameters?**
   A: Edit detection thresholds in ``utils/tracker.py``:
      - ``min_contour_area`` — Minimum size to consider as animal (default: 500 pixels)
      - ``max_no_movement_frames`` — Max frames to hold last bounding box (default: 10)

Troubleshooting
~~~~~~~~~~~~~~~

**Q: Tracker loses the fish intermittently. How do I fix it?**
   A:
      1. Test with debug mode: ``python single_run.py <video>``
      2. Ensure good lighting and contrast
      3. Increase ``max_no_movement_frames`` in utils/tracker.py if animal pauses
      4. Adjust contour area threshold if detection is too sensitive/insensitive

**Q: Distance values seem completely wrong. What's wrong?**
   A:
      1. Verify tank dimensions in ``distance_calculator.py`` match your actual tank
      2. Check video resolution (frame width/height)
      3. Ensure video was not cropped/zoomed

**Q: GUI doesn't appear on Linux. How do I fix it?**
   A: Install Tkinter: ``sudo apt-get install python3-tk``

**Q: I get "ModuleNotFoundError: No module named 'cv2'". What do I do?**
   A: Reinstall OpenCV: ``pip install opencv-python``

**Q: Batch processing is slow. Can I speed it up?**
   A:
      1. Reduce video resolution before processing
      2. Increase ``max_workers`` in main.py (currently 10)
      3. Use faster storage (SSD vs. HDD)

Publishing & Citation
~~~~~~~~~~~~~~~~~~~~~

**Q: How do I cite FishTracker?**
   A: Use the CITATION.cff file or cite as:

   .. code-block:: bibtex

      @article{pathirana2025fishtracker,
        title={FishTracker: a lightweight, open-source tool for video tracking
                and space-use quantification of single aquatic animals in laboratory assays},
        author={Pathirana, Dilshan},
        journal={Journal of Open Source Software},
        year={2025},
        doi={10.21105/joss.00000}
      }

**Q: Is FishTracker published?**
   A: JOSS submission in progress (paper.md). A companion validation paper is planned.

**Q: Can I use FishTracker in published research?**
   A: Yes! It's open-source (MIT license). We appreciate citations but don't require them.

Contributing & Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q: How do I contribute to FishTracker?**
   A: See CONTRIBUTING.md. We welcome bug reports, feature suggestions, and code contributions.

**Q: Can I report bugs?**
   A: Yes, open an issue on `GitHub Issues <https://github.com/Dilshan-Pathirana/Fish_tracking/issues>`_.

**Q: Can I request features?**
   A: Yes, open an issue on GitHub with a clear description and use case.

**Q: Can I fork and modify the code?**
   A: Yes! FishTracker is MIT licensed. You can fork, modify, and distribute under the same license.

If your question isn't answered here, check the full documentation or open a GitHub discussion.
