"""Gap and Go scanner implementation."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

from .data_access import get_daily_data


def scan_gappers(tickers: list[str], gap_threshold: float = 0.04, sample_dir: Path | None = None) -> pd.DataFrame:
    """Scan tickers for gap ups exceeding ``gap_threshold``.

    Parameters
    ----------
    tickers: list of ticker symbols to scan
    gap_threshold: minimum percent gap from previous close to current open
    sample_dir: optional directory containing sample CSVs for offline mode

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns ``ticker`` and ``gap_percent`` sorted by gap.
    """
    results = []
    for ticker in tickers:
        df = get_daily_data(ticker, period="2d", sample_dir=sample_dir)
        if len(df) < 2:
            continue
        prev_close = df.iloc[-2]["Close"]
        today_open = df.iloc[-1]["Open"]
        gap_pct = (today_open - prev_close) / prev_close
        if gap_pct >= gap_threshold:
            results.append({"ticker": ticker, "gap_percent": gap_pct})
    return pd.DataFrame(results).sort_values("gap_percent", ascending=False)
