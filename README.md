# Day Dash Prototype

This repository is a fresh start toward building an open source trading dashboard inspired by Ross Cameron's **Day Dash**. The previous automated trading bot code has been removed to focus on creating a streamlined interface for monitoring the market and running simple scanners.

## Vision

The goal is to provide a lightweight dashboard that shows real‑time price action, watch lists and scan results. The project is in its earliest stages and currently only contains a minimal Streamlit app.

## Planned Roadmap

1. **Real‑time Data Feed** – Integrate a data provider such as `yfinance` or a broker API to stream live prices.
2. **Gap & Go Scanner** – Implement a morning gap scanner similar to the one featured in Day Dash. Results will be displayed directly on the dashboard.
3. **Watch Lists** – Allow users to maintain custom watch lists that update intraday with price and volume information.
4. **Charting Widgets** – Add candlestick charts, moving averages and other basic indicators using libraries like Plotly.
5. **Notifications** – Provide optional alerts (email or desktop) when scan criteria are met or key levels are reached.
6. **Deployment** – Package the app so it can be run locally or deployed to a small cloud instance.

This outline is subject to change as the project evolves.

## Running the Prototype

Install the requirements and start the Streamlit app:

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

The current app only displays a placeholder message, but it serves as the foundation for future features.

## Disclaimer

This project is for educational purposes only. No trading advice is provided and you are solely responsible for your trading decisions.
