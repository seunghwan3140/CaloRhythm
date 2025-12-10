How to Use
==========

CaloRhythm is designed with an intuitive sidebar navigation. You can access three
primary features to manage your diet and nutrition goals effectively.

1. Nutrition Calculator (Standard)
----------------------------------
Calculate the exact nutritional breakdown of your meal and compare it against
recommended daily intake standards.

**Steps:**

1.  **Select Ingredients:** Search and select multiple food items from the database.
2.  **Input Quantities:** Enter the gram (g) amount for each ingredient.
3.  **Analyze:** Click the "Analyze" button to view the total energy, carbs, protein, and fat.

**Key Feature:**
The results include a bar chart comparing your intake against the **Korean Daily
Nutritional Standards (KFDA)** for adults (e.g., 324g Carbs, 55g Protein, 54g Fat),
helping you identify deficiencies or excesses immediately.

2. AI Diet Optimizer
--------------------
This is the core feature of CaloRhythm. It uses a mathematical optimization algorithm
(SLSQP) to calculate the optimal portion sizes for your selected ingredients.

**Steps:**

1.  **Set Constraints:** Define your upper limits for Calories, Carbs, Protein, and Fat per meal.
2.  **Select Ingredients:** Choose the foods available in your fridge.
3.  **Set Minimum Intake (Optional):** Specify a minimum amount (g) for specific foods you want to ensure are included.
4.  **Choose Priority:** Select a priority mode (e.g., **Protein First**, **Balanced**, **Low Fat**).
    The algorithm will weight the optimization to favor your priority while respecting limits.
5.  **Get Recipe:** The system outputs the exact grams for each ingredient to match your goals.

3. Food Discovery by Nutrient
-----------------------------
Discover foods based on their nutrient density to make smarter dietary choices.
Data is based on standard **100g servings**.

**Steps:**

1.  **Select Nutrient:** Choose a target nutrient (Carbohydrate, Protein, or Fat).
2.  **Adjust Rank Count:** Use the slider to determine how many items to display (Top 3 to 100).
3.  **View Rankings:**
    * **High Rank (Red):** Foods with the highest content of the selected nutrient.
    * **Low Rank (Blue):** Foods with the lowest content of the selected nutrient.

This feature is useful for finding high-protein sources or low-fat ingredients quickly.
