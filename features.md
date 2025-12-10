---
layout: custom
title: Features
---

# ✨ CaloRhythm Features

CaloRhythm offers three core features built upon Korean nutritional standards  
and scientific optimization algorithms. Each feature is powered by the  
**National Standard Food Composition Database (v10.3)** and incorporates  
KFDA guidelines for accurate dietary evaluation.

---

## 🥗 1. Standard Nutrition Calculation

Analyze the total nutritional value of any meal using official Korean food data.

**What it does:**
- Computes total **Calories, Carbohydrates, Protein, and Fat** based on ingredient quantities.
- Uses nutrient-per-100g values from the national food database.
- Compares results against **KFDA Adult Daily Standards**:  
  - Carbohydrates: **324g**  
  - Protein: **55g**  
  - Fat: **54g**

**Why it matters:**  
It enables precise evaluation of how a meal aligns with Korean dietary recommendations.

---

## ⚖️ 2. AI Diet Optimizer (SLSQP Algorithm)

A mathematically driven optimizer that computes the *exact* portion sizes  
required to meet your calorie or macronutrient goals.

**Core Logic:**
- Powered by **SciPy’s SLSQP (Sequential Least Squares Programming)** algorithm.
- Minimizes a **Weighted Least Squares** objective function  
  that adjusts ingredient amounts to match target limits.
- Supports user-defined **Minimum Intake** per ingredient.
- Applies strict inequality constraints to prevent exceeding nutrient limits.

**Priority Mode:**
Users can assign emphasis to a nutrient:
- Balanced (default)
- Protein First  
- Carb First  
- Fat First  

This increases the weight (e.g., ×100) in the optimization formula,  
guiding the solver to favor your selected nutrient while respecting all limits.

---

## 🔍 3. Food Discovery by Nutrient Density

Identify the most nutrient-dense foods for targeted dietary planning.

**How it works:**
- Ranks foods using statistical sorting:
  - **Top N**: `df.nlargest(N, nutrient)`
  - **Bottom N**: `df.nsmallest(N, nutrient)`
- Supports Korean nutrient definitions and standardized 100g servings.
- Allows dynamic adjustment of ranking size (Top/Bottom 3–100).

**Use cases:**
- Find high-protein foods quickly  
- Identify low-fat options  
- Explore balanced alternatives based on personal goals

---

## 📘 Full Documentation

For mathematical formulas, architecture details, and full API descriptions,  
visit the official documentation:

👉 [Documentation](https://calorhythm.readthedocs.io/en/latest/index.html)
