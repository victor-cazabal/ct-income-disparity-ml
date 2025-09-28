# Data

This folder contains processed ACS PUMS data for Connecticut.

## Contents
- **new_2018.csv**  
- **new_2019.csv**  
- **new_2021.csv**

Each file is ~2.6MB and includes individual-level demographic and socioeconomic characteristics.

## Notes
- **Source:** American Community Survey (ACS) 1-year PUMS (via `tidycensus`).  
- **Scope:** Connecticut respondents only.  
- **Processing:**  
  - Variables renamed and cleaned in `R/01_download_ct_acs.R`.  
  - Incomes adjusted using `ADJINC`.  
  - Negative values replaced with `"b"` (NA marker).  
  - Limited to individuals with positive incomes.

These curated files are included for reproducibility — they are much smaller than raw ACS extracts.