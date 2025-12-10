API Reference
=============

Since CaloRhythm is a single-page Streamlit application, this section documents the **internal Python functions** and **core logic blocks** used within ``main.py``.

Data Handling Module
--------------------

**load_data()**
   * **Description:**
       The primary function for data ingestion. It reads the local Excel file (``data.xlsx``), detects the header row dynamically, and cleans metadata.
   * **Returns:**
       * ``df`` (pandas.DataFrame): The cleaned nutrient dataset.
       * ``cols_map`` (dict): A mapping dictionary linking standard nutrient names (e.g., 'Carbohydrate') to the actual column names in the Excel file.
   * **Dependencies:** ``openpyxl``, ``pandas``, ``st.cache_data``

Core Feature Logic
------------------

Feature 1: Nutrition Calculator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Logic: Absolute Nutrient Aggregation**
   * **Input:** User-selected food items and their quantities (g).
   * **Process:**
       Iterates through the selected items, retrieves the nutrient value per 100g, calculates the value for the input quantity, and sums them up.
   * **Comparison Standard:**
       Compares the total sum against hardcoded **KFDA Standards**:
       * Carbohydrates: 324g
       * Protein: 55g
       * Fat: 54g

Feature 2: Diet Optimizer
~~~~~~~~~~~~~~~~~~~~~~~~~

**Logic: Constrained Optimization (SLSQP)**
   * **Library:** ``scipy.optimize.minimize``
   * **Objective Function:** **Weighted Least Squares**
       Minimizes the squared difference between the *Limit* and *Current Intake*, multiplied by a weight factor based on the user's priority.
       
       .. math::
       
          Loss = \sum (weight \times (\frac{Limit - Current}{Limit})^2)

   * **Constraints:**
       Inequality constraints ensure that the total nutrient intake does not exceed the user-defined limits.
   * **Bounds:**
       Sets the lower bound to the user's **Minimum Intake** and the upper bound to 1000g (or 2000g).

Feature 3: Food Discovery
~~~~~~~~~~~~~~~~~~~~~~~~~

**Logic: Statistical Ranking**
   * **Input:** Target Nutrient (e.g., Protein), Count ($N$).
   * **Process:**
       * **High Rank:** Uses ``df.nlargest(N, col)`` to find foods rich in the target nutrient.
       * **Low Rank:** Uses ``df.nsmallest(N, col)`` to find foods low in the target nutrient.
   * **Output:** Two DataFrames displayed side-by-side.

Utilities
---------

**safe_percentage(value, limit)**
   * **Description:** A helper function to prevent ``ZeroDivisionError`` or ``NaN`` results when calculating chart percentages.
   * **Logic:** Returns ``0.0`` if the limit is 0; otherwise returns the calculated percentage (capped at 100% for visualization safety).
