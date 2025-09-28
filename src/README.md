# Python Source Code (`src/`)

This folder contains the machine learning pipeline for analyzing income disparity in Connecticut.

## Files
- **preprocess.py**  
  - Cleans the processed ACS data (replaces sentinels, groups categories, dummy encodes categorical variables).  

- **models.py**  
  - Defines regression models: Linear Regression, Decision Tree, Random Forest.  
  - Includes evaluation functions (MSE, R²).  

- **run.py**  
  - Orchestrates end-to-end workflow:  
    - Loads data (`new_2018.csv`, `new_2019.csv`, `new_2021.csv`)  
    - Preprocesses features and targets  
    - Trains and validates models (2018 → 2019)  
    - Tests final model on 2021 data  
    - Saves plots and metrics to `results/`.

## Usage
From repo root:
```bash
python3 -m src.run
```

