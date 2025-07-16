"""High-of-day breakout scanner."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

from .data_access import get_daily_data


def scan_hod_breakouts(tickers: list[str], sample_dir: Path | None = None) -> pd.DataFrame:
    """Detect tickers making new highs compared to the previous day."""
    results = []
    for ticker in tickers:
        df = get_daily_data(ticker, period="2d", sample_dir=sample_dir)
        if len(df) < 2:
            continue
        prev_high = df.iloc[-2]["High"]
        today_high = df.iloc[-1]["High"]
        if today_high > prev_high:
            results.append({"ticker": ticker, "new_high": today_high})
    return pd.DataFrame(results).sort_values("new_high", ascending=False)
