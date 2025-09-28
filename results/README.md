# Results

This folder contains figures, metrics, and the final project write-up.

## Contents
- **ML_final_project.pdf** – full project report (methods, results, discussion).  
- **metrics.txt / CSVs** – accuracy (R²) and error metrics for baseline, decision tree, and random forest.  
- **plots/** – visualizations (e.g., accuracy vs. tree depth, feature importance).  

## Summary of Findings
- **Baseline (Linear Regression):** R² ≈ 0.338.  
- **Decision Tree (tuned):** R² ≈ 0.345 (marginal improvement).  
- **Random Forest (best):** R² ≈ 0.435 on validation (2019), 0.415 on test (2021).  

## Insights
- **Hours worked**, **industry sector**, **education level**, **marital status**, and **county (Fairfield vs others)** were the strongest predictors.  
- COVID-era testing (2021) reduced model accuracy slightly, but not drastically, showing model robustness.  
- Ablation study confirmed the importance of industry, hours worked, and sex in shaping income disparity.

## Interpretation
This project highlights the potential of ML to address **equity issues** in real-world data:
- Predictive modeling can identify structural disparities.  
- Feature importance analysis reveals which demographic and social factors most strongly influence income.  
- Random Forests provide a balance of accuracy and interpretability, outperforming linear baselines.
