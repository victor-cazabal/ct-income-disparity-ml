# Income Disparity in Connecticut Using Machine Learning

**Author:** Victor Cazabal  
**Repo Purpose:** Final project for Machine Learning class, repurposed as a portfolio project.  

---

## Overview
This project applies machine learning models to study **income disparity in Connecticut**, one of the most unequal states in the U.S. By leveraging data from the American Community Survey (ACS, 2018–2021), I explored how individual and household characteristics influence income levels. The project demonstrates both technical modeling skills and an application of data science to issues of **social justice and equity**.

---

## Motivation
Connecticut ranks 5th in the nation for largest wealth gaps, with stark differences by race and ethnicity. Understanding drivers of income can:
- Guide more equitable policy design  
- Help target resources toward under-served groups  
- Highlight systemic inequities (gender, race, industry, geography)

---

## Data
- **Source:** ACS 1-year PUMS (2018, 2019, 2021) via [`tidycensus`](https://walker-data.com/tidycensus/) in R  
- **Features:** 32+ variables (demographics, education, employment, household context, etc.)  
- **Target:** Individual pre-tax income (`PINCP`, adjusted to 2017 dollars with `ADJINC`)  
- **Files included:** Cleaned CSVs (~2.6MB each) for CT only  

See [`data/README.md`](data/README.md) for details.

---

## Methods
- **Baseline:** Linear regression (R² ≈ 0.338)  
- **Decision Trees:** Tuned via `max_depth` (best R² ≈ 0.345)  
- **Random Forest:** Tuned via `n_estimators`, `max_features`, and `max_depth`.  
  - Best R² ≈ 0.435 (on 2019 validation set)  
  - Tested on unseen 2021 data (COVID-era): R² ≈ 0.415  

See [`results/README.md`](results/README.md) for visualizations, metrics, and discussion.

---

## Repository Structure

- 📂 **[R/](R/)** — R scripts to download and clean ACS PUMS data (2018, 2019, 2021)  
- 📂 **[data/](data/)** — Processed CT datasets (~2.6MB each, already cleaned & recoded)  
- 📂 **[src/](src/)** — Python source code (preprocessing, model training, evaluation)  
- 📂 **[results/](results/)** — Figures, metrics, and full project write-up (PDF)  
- 📂 **[slides/](slides/)** — Final project presentation (PDF export)  
- 📄 **README.md** — Project overview (this file)  

Each folder has its own [README](R/README.md) with more details about the contents.

---

## Key Findings
- Random Forests outperformed both linear regression and decision trees, showing the power of ensemble methods in socioeconomic prediction tasks.  
- **Most important predictors:** hours worked, age, industry sector, education level, marital status, and county (Fairfield vs others).  
- Ablation studies confirmed the **large role of industry and gender** in driving income disparities.  

---

## Reproducibility
1. **Data prep:**  
   Run [`R/01_download_ct_acs.R`](R/01_download_ct_acs.R) to download ACS PUMS and generate the cleaned CSVs in `data/`.

2. **Modeling:**  
   Run Python scripts in [`src/`](src/) to preprocess and fit models:  
   ```bash
   python3 -m src.run
   ```
   
3. **Results:**
  Outputs (figures, metrics) are stored in [`results/`](results/).
  
## References

- U.S. Census Bureau. *American Community Survey (ACS) Public Use Microdata Sample (PUMS)*. Retrieved via the [`tidycensus`](https://cran.r-project.org/package=tidycensus) R package.  
- R Core Team (2024). *R: A Language and Environment for Statistical Computing*. Vienna, Austria: R Foundation for Statistical Computing.  
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825–2830.  
- Hunter, J. D. (2007). *Matplotlib: A 2D Graphics Environment*. Computing in Science & Engineering, 9(3), 90–95.  
- McKinney, W. (2010). *Data Structures for Statistical Computing in Python*. Proceedings of the 9th Python in Science Conference, 51–56.  

