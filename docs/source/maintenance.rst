Maintenance and Troubleshooting
===============================

Common Issues
-------------

**1. Application Does Not Start**
* **Symptom:** ``ModuleNotFoundError: No module named 'scipy'`` (or 'altair', 'openpyxl').
* **Solution:** The project relies on specific scientific libraries. Run the following command:
    ``pip install -r requirements.txt``
    (Ensure ``scipy``, ``altair``, and ``openpyxl`` are listed in your requirements file).

**2. Database Connection Error**
* **Symptom:** ``FileNotFoundError: [Errno 2] No such file or directory: 'data.xlsx'``
* **Solution:**
    * CaloRhythm uses a file-based database.
    * Ensure the **National Standard Food DB** file is renamed to ``data.xlsx``.
    * Verify that ``data.xlsx`` is located in the **same directory** as ``main.py``.

**3. Data Loading / Formatting Issues**
* **Symptom:** ``ArrowTypeError`` or weird column names like ``Unnamed: 0``.
* **Solution:**
    * The Excel file usually contains metadata in the top rows.
    * The **Smart Data Loader** in ``main.py`` is designed to automatically find the header row containing '식품명'.
    * If the error persists, check if the Excel file structure (column names) has changed significantly from the RDA standard v10.3.

**4. Optimization Failed (Diet Optimizer)**
* **Symptom:** The result shows ``NaN`` percentages or "Optimization failed" warning.
* **Solution:**
    * **Check Constraints:** This usually happens when the **'Minimum Intake'** sum exceeds the **'Nutrient Limits'**. (e.g., Minimum Chicken 500g > Calorie Limit 100kcal).
    * Increase the limits or decrease the minimum intake amounts.
    * Ensure no limit field is set to ``0``.

Recommended Maintenance
-----------------------

**Database Updates**
Since the project uses a static Excel file (``data.xlsx``), it does not update automatically. Follow these steps carefully to prevent loading errors:

1.  **Download:** Get the latest **National Standard Food Composition DB** (Excel format) from the [Rural Development Administration (RDA)](https://koreanfood.rda.go.kr/kfi/fct/fctIntro/list?menuId=PS03562).
2.  **Open & Clean:** Open the downloaded Excel file.
3.  **Select Main Sheet:** Identify the sheet containing the actual nutrient data (labeled '국가표준식품성분 Database 10.3').
4.  **Delete Others:** **Delete all other sheets** (e.g., Appendices, Change Logs, Unit Definitions).
    * *Why?* The system expects a single-sheet file to ensure it loads the correct data.
5.  **Save:** Save the cleaned file as ``data.xlsx``.
6.  **Replace:** Replace the existing file in your project folder.
7.  **Restart:** Restart the Streamlit server to load the new data.

**Dependency Management**
To ensure stability across different environments:
* Regularly update ``requirements.txt`` if you add new libraries:
    ``pip freeze > requirements.txt``
* Periodically check for library updates (Streamlit, Pandas, Scipy) for performance improvements.
