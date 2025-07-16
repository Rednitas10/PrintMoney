"""Command-line interface for running scanners."""
from __future__ import annotations

import argparse
from pathlib import Path

from .gap_scanner import scan_gappers
from .hod_scanner import scan_hod_breakouts
from .alerts import send_alert


def main() -> None:
    parser = argparse.ArgumentParser(description="Run stock scanners")
    parser.add_argument("tickers", nargs="*", help="List of tickers to scan")
    parser.add_argument("--sample-dir", default=None, help="Directory with sample CSVs")
    parser.add_argument("--gap-threshold", type=float, default=0.04, help="Gap percentage threshold")
    args = parser.parse_args()

    tickers = args.tickers or ["AAPL"]
    sample_dir = Path(args.sample_dir) if args.sample_dir else None

    gappers = scan_gappers(tickers, gap_threshold=args.gap_threshold, sample_dir=sample_dir)
    breakouts = scan_hod_breakouts(tickers, sample_dir=sample_dir)

    if not gappers.empty:
        send_alert("Gapper alerts:")
        for _, row in gappers.iterrows():
            send_alert(f"{row['ticker']} gapped {row['gap_percent']:.2%}")

    if not breakouts.empty:
        send_alert("HOD breakout alerts:")
        for _, row in breakouts.iterrows():
            send_alert(f"{row['ticker']} broke to {row['new_high']}")


if __name__ == "__main__":
    main()
