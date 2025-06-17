import argparse
from pathlib import Path
import pandas as pd


def preprocess_underlying(csv_path: Path) -> pd.DataFrame:
    """Clean and add basic features to underlying data."""
    df = pd.read_csv(csv_path, parse_dates=['Date'])
    df = df.sort_values('Date').drop_duplicates()
    df = df.ffill()
    df['close_ma5'] = df['Close'].rolling(5).mean()
    df['close_ma20'] = df['Close'].rolling(20).mean()
    df['returns'] = df['Close'].pct_change()
    return df


def preprocess_options(csv_path: Path, underlying_price: float) -> pd.DataFrame:
    """Clean options data and compute simple features."""
    df = pd.read_csv(csv_path)
    df = df.drop_duplicates()
    df['spread'] = df['Ask'] - df['Bid']
    df['moneyness'] = (underlying_price - df['Strike']) / df['Strike']
    df = df.fillna(0)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess underlying and options data")
    parser.add_argument("underlying", help="CSV file with historical underlying data")
    parser.add_argument("options", help="CSV file with options chain")
    parser.add_argument("--output", default="cleaned", help="Directory to store processed CSV files")
    args = parser.parse_args()

    underlying_path = Path(args.underlying)
    options_path = Path(args.options)
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)

    underlying_df = preprocess_underlying(underlying_path)
    latest_close = underlying_df['Close'].iloc[-1]
    options_df = preprocess_options(options_path, latest_close)

    underlying_df.to_csv(output_dir / "underlying_clean.csv", index=False)
    options_df.to_csv(output_dir / "options_clean.csv", index=False)
    print(f"Saved cleaned data to {output_dir}")


if __name__ == "__main__":
    main()
