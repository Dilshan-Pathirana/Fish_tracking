FishTracker Documentation
==========================

**FishTracker** is a lightweight, open-source Python tool for tracking single aquatic animals in laboratory video recordings. It uses background subtraction to isolate the moving animal and generates analysis-ready CSV trajectories and heatmap visualizations.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   quickstart
   installation
   usage

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   gui_guide
   cli_guide
   distance_analysis

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide

   contributing
   architecture
   api_reference

.. toctree::
   :maxdepth: 1
   :caption: Additional Resources

   faq
   changelog

Introduction
~~~~~~~~~~~~

FishTracker fills the gap between manual stopwatch/grid scoring and heavier pipelines (idtracker.ai, TRex, DeepLabCut):

- **Lightweight** — No GPU or trained models required
- **Easy to use** — GUI for non-programmers, CLI for batch processing
- **Accurate** — Background subtraction with morphological filtering
- **Open-source** — MIT licensed, fully documented code

Key Features
~~~~~~~~~~~~

- 🎥 Automated single-subject tracking with background subtraction (MOG2)
- ⚡ Batch processing with parallel execution
- 🖥️ Tkinter GUI for interactive video processing
- 🔥 Trajectory heatmap generation with Gaussian blur
- 📏 Real-world distance quantification (cm) with arena calibration
- ⚙️ Headless CLI mode for server environments

System Requirements
~~~~~~~~~~~~~~~~~~~

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **Dependencies**: OpenCV, NumPy, Tkinter (usually bundled with Python)

Quick Start
~~~~~~~~~~~

**GUI Mode (recommended for beginners):**

.. code-block:: bash

   python main.py

**Batch Mode (CLI):**

.. code-block:: bash

   python No_GUI.py /path/to/videos /path/to/outputs

**Debug Mode (single video with ROI selection):**

.. code-block:: bash

   python single_run.py

Citation
~~~~~~~~

If you use FishTracker in published research, please cite:

.. code-block:: bibtex

   @article{pathirana2025fishtracker,
     title={FishTracker: a lightweight, open-source tool for video tracking
             and space-use quantification of single aquatic animals in laboratory assays},
     author={Pathirana, Dilshan},
     journal={Journal of Open Source Software},
     year={2025},
     doi={10.21105/joss.00000}
   }

Or use the `CITATION.cff <https://github.com/Dilshan-Pathirana/Fish_tracking/blob/main/CITATION.cff>`_ file.

Support
~~~~~~~

- 📖 **Documentation**: See the sidebar menu
- 🐛 **Issues**: Report bugs at `GitHub Issues <https://github.com/Dilshan-Pathirana/Fish_tracking/issues>`_
- 💬 **Discussions**: Ask questions at `GitHub Discussions <https://github.com/Dilshan-Pathirana/Fish_tracking/discussions>`_
- 📧 **Contact**: dilshan.pathirana.121@gmail.com

License
~~~~~~~

FishTracker is licensed under the `MIT License <https://github.com/Dilshan-Pathirana/Fish_tracking/blob/main/LICENSE>`_.
