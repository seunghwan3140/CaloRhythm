# CaloRhythm

CaloRhythm is an intelligent, open-source nutrition management system designed for the **Korean dietary environment**.  
It provides accurate nutrient analysis, AI-driven meal optimization, and nutrient-density food discovery powered by:

- **National Standard Food Composition Database (v10.3)**  
- **KFDA Adult Daily Nutrient Standards**  
- **SciPy SLSQP Optimization Engine**  
- **Streamlit Single-Page Application (SPA)**

Our mission is to help users develop a **healthy, sustainable dietary rhythm** based on reliable data and scientific computation.

---

## 🔍 Overview

Modern diets often lead to nutritional imbalance. Many users lack tools that reflect **Korea-specific nutrition data**  
or provide precise nutrient breakdowns for everyday foods.

CaloRhythm addresses this by combining:

- Verified government datasets  
- Mathematical optimization  
- Real-time nutrient analysis  
- Searchable nutrient-density rankings  

This allows users to understand their meals with clarity and make informed dietary choices.

---

## ✨ Key Features

### 1. Standard Nutrition Calculation
- Computes total calories and macronutrients based on selected ingredients.  
- All values sourced from **RDA Food Composition DB (v10.3)**.  
- Results compared against **KFDA Daily Standards**:  
  - Carbs: 324g  
  - Protein: 55g  
  - Fat: 54g  

---

### 2. AI Diet Optimizer (SLSQP)
- Computes *optimal* ingredient quantities with **SciPy's SLSQP solver**.  
- Supports:
  - Nutrient limits (Calories, Carbs, Protein, Fat)  
  - Minimum intake constraints  
  - Priority Mode (Weighted Least Squares)  
- Produces mathematically sound portion sizes tailored to the user’s nutritional goals.

---

### 3. Food Discovery by Nutrient Density
- Ranks foods using statistical methods:  
  - **Top N** (highest in selected nutrient)  
  - **Bottom N** (lowest in selected nutrient)  
- Ideal for exploring high-protein foods, low-fat alternatives, or balanced ingredients.  
- All values normalized per **100g**.

---

## 🛠 Technology Stack

- **Python 3.9+**  
- **Streamlit** (UI/SPA)  
- **Pandas / NumPy** (data processing)  
- **SciPy SLSQP** (optimization engine)  
- **Altair** (statistical visualization)  
- **OpenPyXL** (Excel ingestion)  
- **Sphinx + ReadTheDocs** (documentation)

---

## 🤝 Contributing

We welcome contributions!  
See **[Contributing](Contributing.md)** for branching strategy, PR guidelines, and development setup.

---

## 📜 Code of Conduct

CaloRhythm maintains an inclusive and respectful community.  
See **[Code of Conduct](Code_of_conduct.md)** for details.

---

## 📦 Requirements

Install all dependencies with:
pip install -r requirements.txt


See **requirements.md** for more details.

---

## 🪪 License

CaloRhythm is released under the **Apache License 2.0**.  
Refer to the **LICENSE** file for full terms.

---

## 💬 Community & Discussions

For idea sharing, Q&A, and collaboration:  
Use the **GitHub Discussions** tab.

---

**Documentation and project structure may evolve as the project grows.**
