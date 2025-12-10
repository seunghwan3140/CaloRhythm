Getting Started
===============

This guide explains how to install and run the CaloRhythm application locally.

Prerequisites
-------------
Before you begin, ensure you have the following installed:

- **Python 3.9+** (Tested on Python 3.9 and 3.10)
- **Git** (for version control)
- **pip** package manager

You will also need the **National Standard Food Composition Database (Excel file)**, which is essential for the application to function.

Installation
------------

1. **Clone the repository:**

   .. code-block:: bash

      git clone https://github.com/seunghwan3140/CaloRhythm.git
      cd CaloRhythm

2. **Install dependencies:**
   
   The project requires scientific computing libraries such as ``streamlit``, ``pandas``, ``scipy``, ``altair``, and ``openpyxl``.

   .. code-block:: bash

      pip install -r requirements.txt

Database Setup
--------------
CaloRhythm operates on a file-based database system using the **Korean National Standard Food Composition Database**.
**No SQL server installation (MySQL, PostgreSQL) is required.**

Follow these steps to set up the data:

1.  **Download Data:**
    Visit the [Rural Development Administration (RDA)](http://koreanfood.rda.go.kr/) website and download the latest **"National Standard Food Composition Database (v10.3)"** in Excel format.

2.  **Prepare the File:**
    * Open the Excel file.
    * **Important:** Keep only the main datasheet (usually named 'Database') and **delete all other sheets** (Introduction, Appendices, etc.) to prevent loading errors.
    * Save the file as ``data.xlsx``.

3.  **Place the File:**
    Move the ``data.xlsx`` file into the **root directory** of the project (the same folder where ``main.py`` is located).

    ::

        CaloRhythm/
        ├── .git/
        ├── docs/
        ├── main.py
        ├── requirements.txt
        └── data.xlsx  <-- Place file here

Running the Application
-----------------------

Once the dependencies are installed and ``data.xlsx`` is in place, start the application using Streamlit:

.. code-block:: bash

   streamlit run main.py

The application will launch in your default web browser (usually at ``http://localhost:8501``).
You will see the **Home** screen confirming that the database has been loaded successfully.
