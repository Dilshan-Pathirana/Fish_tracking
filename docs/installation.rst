Installation Guide
===================

System Requirements
~~~~~~~~~~~~~~~~~~~

- **Python**: 3.8 or higher
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: 4 GB minimum (8 GB recommended for batch processing)
- **Disk**: 2 GB for dependencies and test videos

Installation Steps
~~~~~~~~~~~~~~~~~~

1. **Clone the repository:**

   .. code-block:: bash

      git clone https://github.com/Dilshan-Pathirana/Fish_tracking.git
      cd Fish_tracking

2. **Create virtual environment (optional but recommended):**

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install from requirements.txt:**

   .. code-block:: bash

      pip install -r requirements.txt

   Or with modern packaging:

   .. code-block:: bash

      pip install -e .

4. **Verify installation:**

   .. code-block:: bash

      python main.py

Platform-Specific Notes
~~~~~~~~~~~~~~~~~~~~~~~

**Windows 10/11**
   - No additional setup required
   - Python from python.org or Microsoft Store both work

**macOS**
   - May need to install XCode command line tools: ``xcode-select --install``
   - Use ``python3`` instead of ``python`` if needed

**Linux (Ubuntu/Debian)**
   - Install Tkinter: ``sudo apt-get install python3-tk``
   - Install OpenCV dependencies: ``sudo apt-get install libglib2.0-0 libsm6 libxrender1``

Development Setup
~~~~~~~~~~~~~~~~~

To contribute or modify code:

.. code-block:: bash

   pip install -e ".[dev]"

This installs development tools: pytest, mypy, black, flake8, sphinx.

Verify setup:

.. code-block:: bash

   pytest tests/          # Run tests
   mypy .                # Type checking
   black --check .       # Code formatting
   sphinx-build -b html docs/ docs/_build/  # Build documentation

Troubleshooting
~~~~~~~~~~~~~~~

**ModuleNotFoundError: No module named 'cv2'**
   - Reinstall OpenCV: ``pip install opencv-python``

**ModuleNotFoundError: No module named '_tkinter'**
   - Linux: ``sudo apt-get install python3-tk``
   - macOS: Reinstall Python from python.org

**pip: command not found**
   - Try ``python -m pip install ...`` instead

**"Permission denied" errors**
   - Use virtual environment (recommended)
   - Or use ``pip install --user`` (less recommended)

Uninstallation
~~~~~~~~~~~~~~

.. code-block:: bash

   pip uninstall fish-tracker
