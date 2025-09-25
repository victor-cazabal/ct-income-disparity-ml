#R/01_download_ct_acs.R
#Downloads & tidies ACS PUMS (CT) for selected years, writes CSVs for Python.

library(tidycensus)
library(dplyr)
library(readr)
library(stringr)
library(purrr)

# ---- config ---------------------------------------------------------------

YEARS <- c(2018, 2019, 2021)

#output dir
out_dir <- "data"

#INDP bin edges (closed on left, open on right), with integer labels
INDP_bins   <- c(0, 169, 290, 490, 690, 770, 3990, 4590, 5790, 6390,
                 6780, 7190, 7790, 7890, 8290, 8470, 8690, 9290, 9590,
                 9870, 9920)
INDP_labels <- 1:(length(INDP_bins) - 1)

#variables to request from PUMS
vars <- c(
  "PUMA","SEX","AGEP","SCHL","PINCP","RAC1P","HISP","ENG","MAR","PAP","DIS",
  "ESR","HICOV","CIT","LANX","MARHT","MIL","ESP","SSP","WKHP","WAOB",
  "PRIVCOV","PUBCOV","ADJINC","FS","TEN","HUGCL","MULTG","NPF","NRC","INDP","COW"
)

# ---- helpers --------------------------------------------------------------

rename_to_friendly <- function(df) {
  df %>%
    select(-SERIALNO, -SPORDER, -WGTP, -ST) %>%  # drop IDs & state code
    rename(
      PWeight            = PWGTP,
      Age                = AGEP,
      Sex                = SEX,
      Income             = PINCP,
      PA_Inc             = PAP,
      SS_Inc             = SSP,
      Hours_Worked       = WKHP,
      `Citizenship?`     = CIT,
      Speaks_English     = ENG,
      Other_Lang_Home    = LANX,
      Marital_Status     = MAR,
      `#_of_marriages`   = MARHT,
      Military           = MIL,
      Education          = SCHL,
      Disability         = DIS,
      Parent_Employment  = ESP,
      Employment         = ESR,
      Health_Cov         = HICOV,
      Hispanic           = HISP,
      Place_of_Birth     = WAOB,
      Private_HI         = PRIVCOV,
      Public_HI          = PUBCOV,
      Race               = RAC1P,
      Fam_Size           = NPF,
      Children           = NRC,
      FoodSnap           = FS,
      Tenure             = TEN,
      Grandparents       = HUGCL,
      MLTG_HH            = MULTG,
      IND                = INDP
    )
}

adjust_money <- function(df) {
  # multiply income-like columns by ADJINC, then drop ADJINC
  df %>%
    mutate(
      across(c(Income, PA_Inc, SS_Inc), ~ as.numeric(.x) * as.numeric(ADJINC))
    ) %>%
    select(-ADJINC) %>%
    # move Income to rightmost position (nice for eyeballing CSV)
    select(-Income, everything(), Income)
}

clean_year <- function(year) {
  message("Downloading CT ACS PUMS for ", year, " ...")
  dat <- get_pums(
    variables = vars,
    state     = "CT",
    survey    = "acs1",
    year      = year
  )
  
  #special patch for 2021: convert "000N" to numeric lower bound (0169) if present
  if (year == 2021) {
    dat[] <- lapply(dat, function(x) ifelse(x == "000N", "0169", x))
  }
  
  #harmonize INDP into bins
  dat$INDP <- suppressWarnings(as.numeric(dat$INDP))
  dat$INDP <- cut(dat$INDP, breaks = INDP_bins, labels = INDP_labels,
                  right = FALSE, include.lowest = TRUE)
  
  #rename to friendlier column names
  dat <- rename_to_friendly(dat)
  
  #drop negative income rows (invalid)
  dat <- dat %>% filter(as.numeric(Income) >= 0)
  
  #replace sentinel -1 with "b" (NA-like marker used in your Python step)
  dat[] <- lapply(dat, function(x) ifelse(x == -1, "b", x))
  
  #adjust monetary columns to nominal dollars using ADJINC
  dat <- adjust_money(dat)
  
  dat
}
  
# ---- run ------------------------------------------------------------------

if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

res_list <- lapply(YEARS, clean_year)

#write each CSV
purrr::walk2(res_list, YEARS, function(df, yr) {
  out_path <- file.path(out_dir, paste0("new_", yr, ".csv"))
  message("Writing: ", out_path)
  write_csv(df, out_path)
})

message("Done. Files in ", out_dir)
  

