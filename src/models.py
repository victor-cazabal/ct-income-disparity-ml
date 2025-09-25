import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

def train_and_eval(X_train, y_train, X_test, y_test):
    results = {}

    #linear
    lin = LinearRegression().fit(X_train, y_train)
    y_pred = lin.predict(X_test)
    results['linear'] = {'r2': float(r2_score(y_test, y_pred)),
                         'rmse': float(mean_squared_error(y_test, y_pred, squared=False))}

    #decision tree
    dt = DecisionTreeRegressor(max_depth=7, random_state=42).fit(X_train, y_train)
    y_pred = dt.predict(X_test)
    results['decision_tree'] = {'r2': float(r2_score(y_test, y_pred)),
                                'rmse': float(mean_squared_error(y_test, y_pred, squared=False))}

    #random forest
    rf = RandomForestRegressor(n_estimators=500, max_features=20, max_depth=20, random_state=42)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    results['random_forest'] = {'r2': float(r2_score(y_test, y_pred)),
                                'rmse': float(mean_squared_error(y_test, y_pred, squared=False))}
    return results, dt, rf, lin

def curve_dt_depth(X_train, y_train, X_test, y_test, out_png: Path):
    depths = range(1, 20)
    scores = []
    for d in depths:
        m = DecisionTreeRegressor(max_depth=d, random_state=42).fit(X_train, y_train)
        scores.append(r2_score(y_test, m.predict(X_test)))
    plt.figure(figsize=(7,4))
    plt.plot(depths, scores, marker='o')
    plt.title('DecisionTree: R² vs max_depth')
    plt.xlabel('max_depth'); plt.ylabel('R²'); plt.grid(True)
    plt.tight_layout(); plt.savefig(out_png)

def curve_rf_max_features(X_train, y_train, X_test, y_test, out_png: Path):
    step = max(1, X_train.shape[1] // 12)
    feats = list(range(1, X_train.shape[1] + 1, step))
    scores = []
    for f in feats:
        m = RandomForestRegressor(n_estimators=100, max_features=f, max_depth=20, random_state=42)
        m.fit(X_train, y_train); scores.append(r2_score(y_test, m.predict(X_test)))
    plt.figure(figsize=(7,4))
    plt.plot(feats, scores, marker='o')
    plt.title('RandomForest: R² vs max_features')
    plt.xlabel('max_features'); plt.ylabel('R²'); plt.grid(True)
    plt.tight_layout(); plt.savefig(out_png)

def save_metrics(metrics: dict, out_json: Path):
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(metrics, indent=2))