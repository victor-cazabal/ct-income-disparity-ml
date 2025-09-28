# R Scripts

This folder contains R code to download, clean, and prepare ACS PUMS data for Connecticut.

## Files
- **01_download_ct_acs.R**  
  - Uses `tidycensus` to fetch ACS 1-year PUMS (2018, 2019, 2021).  
  - Recodes key demographic, socioeconomic, and household variables.  
  - Adjusts income variables using `ADJINC` to account for inflation.  
  - Writes cleaned CSVs into the `data/` folder.

## Usage
```r
# First time only: set your Census API key
tidycensus::census_api_key("YOUR_KEY", install = TRUE)

# Run script
source("R/01_download_ct_acs.R")
```

The output files are:

- data/new_2018.csv
- data/new_2019.csv
- data/new_2021.csv