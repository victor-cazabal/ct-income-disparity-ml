import argparse
from pathlib import Path
from src.preprocess import load_three_years
from src.models import train_and_eval, curve_dt_depth, curve_rf_max_features, save_metrics
from sklearn.model_selection import train_test_split

def main(args):
    d18, d19, d21 = load_three_years(args.y2018, args.y2019, args.y2021)

    X18, y18 = d18.drop(columns=['Income']), d18['Income']
    X19, y19 = d19.drop(columns=['Income']), d19['Income']
    X21, y21 = d21.drop(columns=['Income']), d21['Income']

    #internal split (optional)
    X18_tr, X18_te, y18_tr, y18_te = train_test_split(X18, y18, test_size=0.2, random_state=42)

    #train on 2018, test on 2019
    metrics_2019, dt, rf, lin = train_and_eval(X18, y18, X19, y19)
    save_metrics(metrics_2019, Path(args.out) / "metrics_2019.json")

    #curves
    curve_dt_depth(X18, y18, X19, y19, Path(args.out) / "dt_depth_curve.png")
    curve_rf_max_features(X18, y18, X19, y19, Path(args.out) / "rf_max_features_curve.png")

    #test 2021
    metrics_2021, *_ = train_and_eval(X18, y18, X21, y21)
    save_metrics(metrics_2021, Path(args.out) / "metrics_2021.json")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--y2018", default="data/new_2018.csv")
    ap.add_argument("--y2019", default="data/new_2019.csv")
    ap.add_argument("--y2021", default="data/new_2021.csv")
    ap.add_argument("--out",   default="results")
    main(ap.parse