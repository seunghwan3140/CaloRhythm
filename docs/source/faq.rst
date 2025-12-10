FAQ
===

**Is CaloRhythm free to use?**
Yes. It is fully open-source software released under the **Apache License 2.0**. You are free to use, modify, and distribute it.

**What database is required? Do I need MySQL?**
No, you do not need to install MySQL or any SQL server.
CaloRhythm uses a **file-based database system (Excel)** for portability and ease of use. You simply need to place the ``data.xlsx`` file in the project folder.

**Does the project support AI features?**
Yes! The **'Diet Optimizer' (Feature 2)** is powered by a mathematical optimization engine (**SciPy SLSQP algorithm**).
It intelligently calculates the optimal ingredient proportions to match your exact nutritional goals and constraints, which goes beyond simple calculation.

**Why do I get a "No module named scipy" error?**
This error occurs when the required scientific libraries are missing.
Please run the following command in your terminal:
``pip install -r requirements.txt``

**The Optimizer shows "NaN" or fails to find a solution. Why?**
This usually happens when the constraints are **mathematically impossible**.
*Example:* If you set a "Calorie Limit" of 100kcal but set a "Minimum Chicken Breast Intake" of 500g (approx. 550kcal), the solver cannot find a solution.
Try increasing the limits or reducing the minimum intake amounts.

**Can I contribute?**
Absolutely. We welcome contributions! Please submit Issues or Pull Requests on our GitHub repository.

**Where can I discuss new ideas?**
Please use the **Discussions** tab on our GitHub repository to share ideas or ask questions.
