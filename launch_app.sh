#!/bin/bash
# Launch the Streamlit dashboard with scanners running.
# Usage: ./launch_app.sh [TICKERS...]

cd "$(dirname "$0")" || exit 1

# Start the scanners in the background
python -m scanners.scanner_cli "$@" &

# Launch the Streamlit dashboard
streamlit run dashboard.py
