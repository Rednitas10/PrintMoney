"""Data access helpers for scanners."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

try:
    import yfinance as yf
except ImportError:  # pragma: no cover - handle missing dependency
    yf = None


def get_daily_data(ticker: str, period: str = "2d", sample_dir: Path | None = None) -> pd.DataFrame:
    """Fetch recent daily OHLC data for ``ticker``.

    The function tries to download data using :mod:`yfinance`. When network
    access is unavailable, it falls back to a CSV file in ``sample_dir`` if
    provided.
    """
    if yf is None:
        raise RuntimeError("yfinance is required. Try `pip install yfinance`.")

    try:
        df = yf.download(ticker, period=period, interval="1d", progress=False)
        if df.empty:
            raise ValueError("No data returned")
        df = df.reset_index()[["Date", "Open", "High", "Low", "Close", "Volume"]]
        return df
    except Exception as exc:
        if sample_dir:
            path = Path(sample_dir) / f"{ticker}_underlying.csv"
            if path.exists():
                return pd.read_csv(path, parse_dates=["Date"])
        raise RuntimeError(f"Failed to fetch data for {ticker}: {exc}") from exc
