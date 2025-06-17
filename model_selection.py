import argparse
from pathlib import Path
import pandas as pd

try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
except ImportError as exc:  # pragma: no cover - handle missing dependency
    raise RuntimeError(
        "scikit-learn is required. Try `pip install scikit-learn`."
    ) from exc


def load_dataset(features_path: Path) -> tuple[pd.DataFrame, pd.Series]:
    """Prepare features and target for training.

    The target is whether the next day's close is higher than today's.
    """
    df = pd.read_csv(features_path, parse_dates=["Date"])
    df = df.sort_values("Date")
    df["target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
    df = df.dropna(subset=["target"])

    feature_cols = [
        c
        for c in ["close_ma5", "close_ma20", "rsi14", "vol30d"]
        if c in df.columns
    ]
    X = df[feature_cols].fillna(0)
    y = df["target"]
    return X, y


def main() -> None:
    parser = argparse.ArgumentParser(description="Train simple models on features")
    parser.add_argument(
        "underlying_features",
        help="CSV from feature_engineering.py containing underlying features",
    )
    parser.add_argument(
        "--output",
        default="models",
        help="Directory to store model accuracy results",
    )
    args = parser.parse_args()

    X, y = load_dataset(Path(args.underlying_features))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, shuffle=False
    )

    lr = LogisticRegression(max_iter=500)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)

    # logistic regression requires at least two classes
    lr_score = float("nan")
    if y_train.nunique() > 1:
        lr.fit(X_train, y_train)
        lr_score = lr.score(X_test, y_test)

    rf.fit(X_train, y_train)
    rf_score = rf.score(X_test, y_test)

    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    scores_path = output_dir / "scores.txt"
    scores_path.write_text(
        f"logistic_regression={lr_score:.4f}\nrandom_forest={rf_score:.4f}\n"
    )

    print(f"Logistic Regression accuracy: {lr_score:.4f}")
    print(f"Random Forest accuracy: {rf_score:.4f}")
    print(f"Saved scores to {scores_path}")


if __name__ == "__main__":
    main()
