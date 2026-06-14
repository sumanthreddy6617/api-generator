"""Train Decision Tree classifier for API category prediction."""
import os, json, joblib, pandas as pd, numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix)

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "dataset.csv")
OUT = os.path.join(HERE, "api_classifier.pkl")

METHOD_MAP = {"GET":0,"POST":1,"PUT":2,"DELETE":3}

def main():
    df = pd.read_csv(CSV)
    df["method_id"] = df["method"].map(METHOD_MAP)
    X = df[["method_id","num_fields","name_hash"]].values
    y = df["category"].values

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = DecisionTreeClassifier(max_depth=8, random_state=42)
    clf.fit(Xtr, ytr)
    pred = clf.predict(Xte)
    labels = sorted(list(set(y)))

    meta = {
        "accuracy":  float(accuracy_score(yte, pred)),
        "precision": float(precision_score(yte, pred, average="weighted", zero_division=0)),
        "recall":    float(recall_score(yte, pred, average="weighted", zero_division=0)),
        "f1":        float(f1_score(yte, pred, average="weighted", zero_division=0)),
        "confusion_matrix": confusion_matrix(yte, pred, labels=labels).tolist(),
        "labels": labels,
    }
    joblib.dump({"model": clf, "meta": meta}, OUT)
    print("Saved model →", OUT)
    print(json.dumps(meta, indent=2))

if __name__ == "__main__":
    main()
