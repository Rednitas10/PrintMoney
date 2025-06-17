import argparse
from pathlib import Path
import pandas as pd

try:
    import yfinance as yf
except ImportError:  # pragma: no cover - handle missing dependency
    yf = None


def collect_underlying(ticker: str, period: str = "1y", sample_dir: Path | None = None) -> pd.DataFrame:
    """Download historical data for the underlying asset.

    When network access is unavailable, a CSV from ``sample_dir`` can be used
    as a fallback if provided.
    """
    if yf is None:
        raise RuntimeError("yfinance is not installed. Try `pip install yfinance`.")
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period=period)
        if hist.empty:
            raise ValueError("No data returned")
        return hist
    except Exception as exc:
        if sample_dir:
            sample_path = sample_dir / f"{ticker}_underlying.csv"
            if sample_path.exists():
                return pd.read_csv(sample_path, index_col=0, parse_dates=True)
        raise RuntimeError(f"Failed to download underlying data: {exc}") from exc


def collect_options(ticker: str, sample_dir: Path | None = None) -> pd.DataFrame:
    """Fetch the first available options chain for the ticker."""
    if yf is None:
        raise RuntimeError("yfinance is not installed. Try `pip install yfinance`.")
    try:
        asset = yf.Ticker(ticker)
        expirations = asset.options
        if not expirations:
            return pd.DataFrame()
        first_exp = expirations[0]
        chain = asset.option_chain(first_exp)
        calls = chain.calls.assign(type="call")
        puts = chain.puts.assign(type="put")
        options = pd.concat([calls, puts], ignore_index=True)
        options["expiration"] = first_exp
        return options
    except Exception as exc:
        if sample_dir:
            sample_path = sample_dir / f"{ticker}_options.csv"
            if sample_path.exists():
                return pd.read_csv(sample_path)
        raise RuntimeError(f"Failed to download options data: {exc}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect underlying and options data")
    parser.add_argument("ticker", help="Ticker symbol, e.g. AAPL")
    parser.add_argument("--period", default="1y", help="Historical period for underlying data")
    parser.add_argument("--output", default="data", help="Directory to store CSV files")
    parser.add_argument("--sample-dir", default=None, help="Use CSV files from this directory if downloads fail")
    args = parser.parse_args()

    sample_dir = Path(args.sample_dir) if args.sample_dir else None

    underlying = collect_underlying(args.ticker, args.period, sample_dir)
    options = collect_options(args.ticker, sample_dir)

    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    underlying.to_csv(output_dir / f"{args.ticker}_underlying.csv")
    options.to_csv(output_dir / f"{args.ticker}_options.csv", index=False)
    print(f"Saved data to {output_dir}")


if __name__ == "__main__":
    main()
