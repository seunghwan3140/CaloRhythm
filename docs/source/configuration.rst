Configuration Guide
===================

This guide outlines how to configure CaloRhythm for both end-users (via the UI) and developers (via the source code).

User Configuration (UI Settings)
--------------------------------
The Streamlit interface allows users to dynamically configure the optimization engine without changing the code.

**1. Nutritional Constraints**
In the **Diet Optimizer** module, users can set strict upper limits for a single meal:
* **Calories (kcal):** Maximum energy intake (Default: 500 kcal).
* **Macronutrients (g):** Maximum limits for Carbohydrates, Protein, and Fat.

**2. Optimization Priorities**
Users can adjust the "Priority Mode" to influence the AI's decision-making:
* **Balanced (Default):** All nutrients have equal weight (1:1:1:1).
* **Protein/Carb/Fat Priority:** Assigns a weight of **100** to the selected nutrient to force maximization/minimization of error.

**3. Ingredient Constraints**
* **Minimum Intake (g):** Users can define a lower bound for specific ingredients (e.g., "Must include at least 100g of Chicken Breast").

Developer Configuration (Codebase)
----------------------------------
Developers can modify hardcoded constants and settings within ``main.py``.

**1. Database Path**
The application expects the food database file to be in the root directory.
To change the filename or path, modify the ``load_data`` function:

.. code-block:: python

    # main.py
    file_path = os.path.join(current_dir, 'data.xlsx')  # Change 'data.xlsx' if needed

**2. KFDA Reference Standards**
The **Nutrition Calculator** uses hardcoded daily intake standards for Korean adults.
These can be updated in the Feature 1 section:

.. code-block:: python

    # Default KFDA Standards (2,000 kcal basis)
    std_carb = 324.0  # Carbohydrates (g)
    std_prot = 55.0   # Protein (g)
    std_fat = 54.0    # Fat (g)

**3. Optimization Hyperparameters**
The **Diet Optimizer** uses the SciPy ``SLSQP`` solver.
Developers can tweak the **weights** dictionary in Feature 2 to change how aggressive the priority mode is:

.. code-block:: python

    # Current weights for priority mode
    weights = {'cal': 1, 'carb': 1, 'prot': 1, 'fat': 1}
    # Modify '100' to a higher value for stricter prioritization

Requirements
------------
All Python dependencies are defined in ``requirements.txt``.
Key libraries include:

* ``streamlit``
* ``pandas``
* ``scipy``
* ``altair``
* ``openpyxl``
