Technical Overview
==================

Architecture
------------
The CaloRhythm system follows a streamlined, single-page application (SPA) architecture
powered by Streamlit. It consists of three major layers:

1. Streamlit Frontend (UI Layer)
   - Provides an interactive user interface for ingredient selection, data input, and visualization.
   - Utilizes **Altair** for rendering responsive charts (e.g., nutrient breakdown, rank comparisons).

2. Backend Processing (Logic Layer)
   - **Data Processing:** Uses **Pandas** for high-performance data manipulation and cleaning.
   - **Optimization Engine:** Implements the **SLSQP (Sequential Least SQuares Programming)** algorithm via **SciPy**.
     This engine solves constrained optimization problems to calculate ideal food portions.
   - **Ranking System:** Statistical sorting and filtering logic for the 'Food Discovery' feature.

3. Data Layer
   - Currently operates on a **File-based Database** system.
   - Integrates the **National Standard Food Composition Database (Version 10.3)** provided by the Rural Development Administration (RDA) of Korea.
   - Data is loaded into memory using **OpenPyXL** for fast access during runtime.

Technologies Used
-----------------
The project relies on a robust set of Python libraries:

- **Python 3.9+** (Core Language)
- **Streamlit** (Web Application Framework)
- **Pandas** (Data Analysis & Manipulation)
- **SciPy** (Mathematical Optimization & Scientific Computing)
- **Altair** (Declarative Statistical Visualization)
- **OpenPyXL** (Excel File I/O Engine)

All dependencies are managed via ``requirements.txt``.

Core Components
---------------
The application logic is modularized within ``main.py`` and helper modules:

- **Smart Data Loader:** Automatically detects header rows and cleans metadata from the raw Excel dataset.
- **Diet Optimizer Engine:** Defines objective functions (Least Squares) and constraints (Nutrient Limits) to compute optimal recipes.
- **Nutrient Calculator:** Computes absolute nutrient values against KFDA standards.
- **Food Discovery Module:** Filters and ranks foods based on specific nutrient density (Top/Bottom N).

Future Directions
-----------------
Planned improvements to scale the project include:

- **Database Migration:** Transition from Excel files to a relational database (MySQL/PostgreSQL) for scalability.
- **User Authentication:** Implementing login features to save user preferences and history.
- **Image Recognition:** Integrating OpenCV/PyTorch to recognize food from photos and estimate calories.
- **Mobile Application:** Porting the logic to a mobile-native environment (Flutter or React Native).
