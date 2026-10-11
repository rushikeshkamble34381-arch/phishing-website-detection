"""Train PhishGuard's URL-feature phishing classifier.

Expected dataset: data/phishing.csv
Expected target column: result (-1 = phishing, 1 = legitimate)
"""

from pathlib import Path
import re
import sys

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import pickle

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "phishing.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "url_only_phishing_model.pkl"

# These names are used consistently by both training and app.py.
FEATURE_NAMES = [
    "having_ip_address",
    "url_length",
    "shortining_service",
    "having_at_symbol",
    "double_slash_redirecting",
    "prefix_suffix",
    "having_sub_domain",
    "https_token",
]

# Dataset column names differ slightly across Kaggle copies. Normalize names
# and map common variants instead of assuming one exact capitalization.
COLUMN_ALIASES = {
    "having_ip_address": {"havingipaddress", "ipaddress"},
    "url_length": {"urllength", "lengthofurl"},
    "shortining_service": {"shortiningservice", "shorteningservice"},
    "having_at_symbol": {"havingatsymbol", "atsymbol"},
    "double_slash_redirecting": {"doubleslashredirecting", "doubleslash"},
    "prefix_suffix": {"prefixsuffix", "prefixsuffixdomain"},
    "having_sub_domain": {"havingsubdomain", "subdomain"},
    "https_token": {"httpstoken", "httpsinthedomain"},
}


def normalize_column_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def find_column(columns, feature_name):
    normalized = {normalize_column_name(column): column for column in columns}
    for alias in COLUMN_ALIASES[feature_name]:
        if alias in normalized:
            return normalized[alias]
    return None


def main():
    if not DATA_PATH.exists():
        print(f"ERROR: Dataset not found: {DATA_PATH}")
        print("Make sure phishing.csv is inside the project's data folder.")
        sys.exit(1)

    df = pd.read_csv(DATA_PATH)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    target_column = next(
        (column for column in df.columns if normalize_column_name(column) == "result"),
        None,
    )
    if target_column is None:
        print("ERROR: Could not find target column named 'result'.")
        print("Columns found:", list(df.columns))
        sys.exit(1)

    selected_columns = {}
    missing_features = []
    for feature in FEATURE_NAMES:
        source_column = find_column(df.columns, feature)
        if source_column is None:
            missing_features.append(feature)
        else:
            selected_columns[feature] = source_column

    if missing_features:
        print("ERROR: Dataset is missing required feature columns:")
        for feature in missing_features:
            print(" -", feature)
        print("Columns found:", list(df.columns))
        sys.exit(1)

    X = df[[selected_columns[name] for name in FEATURE_NAMES]].copy()
    X.columns = FEATURE_NAMES
    y = pd.to_numeric(df[target_column], errors="coerce")

    valid_rows = y.isin([-1, 1]) & X.notna().all(axis=1)
    X = X.loc[valid_rows].apply(pd.to_numeric, errors="coerce")
    y = y.loc[valid_rows].astype(int)

    valid_rows_again = X.notna().all(axis=1)
    X = X.loc[valid_rows_again]
    y = y.loc[valid_rows_again]

    if len(X) < 20 or y.nunique() != 2:
        print("ERROR: Not enough valid rows or dataset does not contain both labels -1 and 1.")
        print("Valid rows:", len(X), "Labels:", sorted(y.unique().tolist()))
        sys.exit(1)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
        min_samples_leaf=2,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    bundle = {
        "model": model,
        "feature_names": FEATURE_NAMES,
        "target_mapping": {-1: "Potential Phishing", 1: "Potentially Legitimate"},
        "test_accuracy": float(accuracy),
        "dataset_path": "data/phishing.csv",
        "training_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
    }
    with open(MODEL_PATH, "wb") as file:
        pickle.dump(bundle, file)

    # Save a confusion matrix image for the dashboard.
    cm = confusion_matrix(y_test, y_pred, labels=[-1, 1])
    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["Phishing (-1)", "Legitimate (1)"],
    )
    fig, ax = plt.subplots(figsize=(7, 5))
    display.plot(ax=ax, cmap="Blues", colorbar=False, values_format="d")
    ax.set_title("PhishGuard Model Confusion Matrix")
    fig.tight_layout()
    fig.savefig(MODEL_DIR / "confusion_matrix.png", dpi=160)
    plt.close(fig)

    # Save feature importance image.
    importance = pd.Series(model.feature_importances_, index=FEATURE_NAMES).sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    importance.plot(kind="barh", ax=ax, color="#2463a6")
    ax.set_title("URL Feature Importance")
    ax.set_xlabel("Importance")
    fig.tight_layout()
    fig.savefig(MODEL_DIR / "feature_importance.png", dpi=160)
    plt.close(fig)

    print("\nTraining completed successfully.")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Test accuracy: {accuracy * 100:.2f}%")
    print("\nClassification report:")
    print(classification_report(
        y_test,
        y_pred,
        labels=[-1, 1],
        target_names=["Potential Phishing", "Potentially Legitimate"],
        zero_division=0,
    ))
    print("Confusion matrix saved to:", MODEL_DIR / "confusion_matrix.png")
    print("Feature importance saved to:", MODEL_DIR / "feature_importance.png")
    print("\nNote: accuracy is measured on the held-out dataset; it does not guarantee correct predictions for every real-world URL.")


if __name__ == "__main__":
    main()
