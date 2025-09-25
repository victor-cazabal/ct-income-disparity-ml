import numpy as np
import pandas as pd

CT_PUMA_GROUPS = {
    1100: [1100, 1101],             #New London
    300:  [301, 302, 303, 304, 305, 306],  #Hartford
    900:  [900, 901, 902, 903, 904, 905, 906],  #New Haven
    100:  [100, 101, 102, 103, 104, 105],       #Fairfield
}

CAT_COLS = [
    'PUMA', 'Tenure', 'Grandparents','MLTG_HH', 'Citizenship?', 'COW',
    'Speaks_English','Other_Lang_Home','Marital_Status', 'Military',
    'Education', 'Parent_Employment','Employment', 'Hispanic', 'IND',
    'Place_of_Birth', 'Race'
]

def _collapse_puma(df: pd.DataFrame) -> pd.DataFrame:
    rev = {puma: key for key, vals in CT_PUMA_GROUPS.items() for puma in vals}
    return df.assign(PUMA=df['PUMA'].replace(rev))

def preprocess_ct_data(df: pd.DataFrame, cols_to_nan: list[str]) -> pd.DataFrame:
    #replace sentinel 'b'
    df = df.copy()
    df[cols_to_nan] = df[cols_to_nan].replace('b', np.nan)
    for col in ['Children', '#_of_marriages']:
        if col in df.columns:
            df[col] = df[col].replace('b', 0)

    #coerce numerics where possible
    df = df.apply(pd.to_numeric, errors='ignore')

    #regroup Education (1–11 -> 11) and Hispanic (2–24 -> 2)
    if 'Education' in df.columns:
        df['Education'] = df['Education'].replace(list(range(1,12)), 11)
    if 'Hispanic' in df.columns:
        df['Hispanic'] = df['Hispanic'].replace(list(range(2,25)), 2)

    #PUMA collapse
    if 'PUMA' in df.columns:
        df = _collapse_puma(df)

    #one-hot
    present_cats = [c for c in CAT_COLS if c in df.columns]
    df = pd.get_dummies(df, columns=present_cats, prefix=present_cats, dummy_na=True)

    return df

def load_three_years(p2018: str, p2019: str, p2021: str):
    cols_to_nan = ['Tenure','Grandparents','MLTG_HH','COW','Speaks_English',
                   'Parent_Employment','Military','Employment']
    d18 = preprocess_ct_data(pd.read_csv(p2018), cols_to_nan)
    d19 = preprocess_ct_data(pd.read_csv(p2019), cols_to_nan)
    d21 = preprocess_ct_data(pd.read_csv(p2021, low_memory=False), cols_to_nan)

    #align columns across years
    common = set(d18.columns) & set(d19.columns) & set(d21.columns)
    #keep target if present
    common |= {'Income'} if 'Income' in d18.columns else set()
    d18 = d18[[c for c in d18.columns if c in common]]
    d19 = d19[[c for c in d19.columns if c in common]]
    d21 = d21[[c for c in d21.columns if c in common]]
    return d18, d19, d21