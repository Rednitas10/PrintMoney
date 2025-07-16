import streamlit as st
import pandas as pd
from pathlib import Path

from scanners import scan_gappers, scan_hod_breakouts


def load_data(feature_dir: str = "features", model_dir: str = "models"):
    """Load engineered features and model scores."""
    underlying_path = Path(feature_dir) / "underlying_features.csv"
    options_path = Path(feature_dir) / "options_features.csv"
    underlying_df = pd.read_csv(underlying_path, parse_dates=["Date"])
    options_df = pd.read_csv(options_path)

    scores_file = Path(model_dir) / "scores.txt"
    scores = {}
    if scores_file.exists():
        for line in scores_file.read_text().splitlines():
            if "=" in line:
                key, val = line.split("=", 1)
                scores[key] = float(val) if val != "nan" else float("nan")
    return underlying_df, options_df, scores


def main() -> None:
    st.title("Trading Bot Dashboard")

    underlying_df, options_df, scores = load_data()

    st.subheader("Underlying Price with Moving Averages")
    st.line_chart(
        underlying_df.set_index("Date")[["Close", "close_ma5", "close_ma20"]]
    )

    st.subheader("RSI and Volatility")
    st.line_chart(underlying_df.set_index("Date")[["rsi14", "vol30d"]])

    if scores:
        st.subheader("Model Accuracy")
        score_df = pd.DataFrame(list(scores.items()), columns=["Model", "Accuracy"])
        st.table(score_df)

    st.subheader("Latest Option Features")
    st.dataframe(options_df.tail())

    st.subheader("Scanner Settings")
    tickers = st.text_input("Tickers (comma separated)", "AAPL")
    gap_threshold = st.slider("Gap threshold", min_value=0.01, max_value=0.10, value=0.04, step=0.01)
    use_sample = st.checkbox("Use sample CSV data", value=False)
    run_scan = st.button("Run Scanners")

    if run_scan:
        ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
        sample_dir = Path("sample_data") if use_sample else None

        st.subheader("Gap and Go Results")
        gappers = scan_gappers(ticker_list, gap_threshold=gap_threshold, sample_dir=sample_dir)
        if not gappers.empty:
            st.table(gappers)
        else:
            st.write("No gappers found.")

        st.subheader("HOD Breakout Results")
        breakouts = scan_hod_breakouts(ticker_list, sample_dir=sample_dir)
        if not breakouts.empty:
            st.table(breakouts)
        else:
            st.write("No breakouts found.")


if __name__ == "__main__":
    main()
