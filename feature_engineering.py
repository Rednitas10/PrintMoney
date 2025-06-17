import argparse
from pathlib import Path
import pandas as pd


def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """Compute the Relative Strength Index (RSI)."""
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    df[f'rsi{window}'] = 100 - 100 / (1 + rs)
    return df


def add_volatility(df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
    """Annualized rolling volatility based on returns."""
    df[f'vol{window}d'] = df['returns'].rolling(window=window).std() * (252 ** 0.5)
    return df


def engineer_underlying_features(path: Path) -> pd.DataFrame:
    """Load cleaned underlying data and compute indicators."""
    df = pd.read_csv(path, parse_dates=['Date'])
    if 'returns' not in df.columns:
        df['returns'] = df['Close'].pct_change()
    df = add_rsi(df)
    df = add_volatility(df)
    return df


def engineer_option_features(path: Path, reference_date: pd.Timestamp) -> pd.DataFrame:
    """Add basic option-related features."""
    df = pd.read_csv(path)
    df['mid_price'] = (df['Bid'] + df['Ask']) / 2
    df['time_to_expiration'] = (pd.to_datetime(df['expiration']) - reference_date).dt.days
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate engineered features for trading models")
    parser.add_argument("underlying", help="CSV file output from preprocess_data.py for the underlying")
    parser.add_argument("options", help="CSV file output from preprocess_data.py for options")
    parser.add_argument("--output", default="features", help="Directory to store feature CSV files")
    args = parser.parse_args()

    underlying_path = Path(args.underlying)
    options_path = Path(args.options)
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)

    underlying_df = engineer_underlying_features(underlying_path)
    latest_date = underlying_df['Date'].max()
    options_df = engineer_option_features(options_path, latest_date)

    underlying_df.to_csv(output_dir / "underlying_features.csv", index=False)
    options_df.to_csv(output_dir / "options_features.csv", index=False)
    print(f"Saved engineered features to {output_dir}")


if __name__ == "__main__":
    main()
