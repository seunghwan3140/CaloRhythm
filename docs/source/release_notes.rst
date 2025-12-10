Release Notes
=============

v0.1.0 — Functional Beta Release
--------------------------------
*Release Date: 2025-12-10*

This release marks the transition from a prototype to a fully functional MVP (Minimum Viable Product).
It includes the integration of the Korean National Food Database and three core AI/Data-driven features.

**New Features**

* **Core System & Data**
    * Integrated **National Standard Food Composition Database (v10.3)** provided by RDA.
    * Implemented **Smart Data Loader** to handle Excel metadata and clean column headers automatically.
    * Adopted **Altair** for advanced data visualization (horizontal labels, responsive charts).

* **Feature 1: Nutrition Calculator**
    * Calculates total calories and macronutrients based on selected ingredients.
    * Provides absolute value comparison against **KFDA Adult Daily Standards** (Carbs 324g, Protein 55g, Fat 54g).

* **Feature 2: AI Diet Optimizer**
    * Implemented a mathematical optimization engine using **SciPy (SLSQP)**.
    * Added **Constraint Logic**: Optimizes quantities while respecting Calorie/Nutrient limits and user-defined **Minimum Intake**.
    * Introduced **Priority Mode (Weighted Least Squares)**: Allows users to prioritize specific nutrients (e.g., "Protein First") during optimization.

* **Feature 3: Food Discovery**
    * Added sorting algorithms to rank foods by nutrient density (Top/Bottom N).
    * Supports dynamic filtering for Carbohydrates, Protein, and Fats.

**Bug Fixes**

* Fixed ``ArrowTypeError`` caused by uncleaned Excel header rows.
* Resolved ``NaN`` percentage calculation issues when limits are set to zero.
* Fixed chart label orientation issues by migrating from ``st.bar_chart`` to ``Altair``.

v0.0.1 — Initial Setup
----------------------
*Release Date: 2025-11-21*

- Base project structure created with Sphinx documentation.
- Streamlit entry point (``main.py``) established.
- Defined project roadmap and "CaloRhythm" branding.
