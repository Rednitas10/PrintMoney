# PrintMoney

This repository aims to experiment with building an automated trading bot for options. Below is a suggested task list for training a model. This is **not** financial advice and profitability is not guaranteed. Proceed at your own risk and consult a professional financial advisor if needed.

## Setup

Install the Python dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Tasks

1. **Collect data**: Gather historical option prices, underlying asset data, and relevant market indicators from reliable data vendors. The `collect_data.py` script supports a `--sample-dir` option for loading CSV files when network access is unavailable.
2. **Clean and preprocess**: Handle missing values, adjust for corporate actions (splits, dividends), and align timestamps across data sources. The `preprocess_data.py` script generates cleaned CSV files with basic features like moving averages.
3. **Feature engineering**: Create additional features such as implied volatility, Greeks (delta, gamma, theta, vega), moving averages, and other technical indicators. The `feature_engineering.py` script illustrates a simple approach for adding RSI, volatility, and option time to expiration.
4. **Model selection**: Test a variety of algorithms (e.g., tree-based models, neural networks, reinforcement learning) to forecast option price movements or risk metrics. The `model_selection.py` script provides a simple logistic regression and random forest baseline. For reinforcement learning experimentation, see `reinforcement_model.py`, which trains a basic agent using PPO. It can be run with a high number of timesteps to train overnight.
5. **Backtesting**: Evaluate the model on historical data with realistic transaction costs and slippage to assess performance and drawdowns.
6. **Risk management**: Define position sizing rules and risk limits (e.g., maximum exposure per trade, stop-loss thresholds).
7. **Paper trading**: Run the strategy in a simulated environment to verify results before committing real capital.
8. **Deployment**: Automate order execution through a broker API while monitoring latency and system reliability.
9. **Monitoring and iteration**: Continuously track live performance, retrain the model with new data, and refine features or parameters as needed.

## Reinforcement Learning Training

After generating features, run the PPO training script:

```bash
python reinforcement_model.py features/underlying_features.csv --timesteps 100000
```

Increase the `--timesteps` argument to train for longer (e.g., overnight).

## Visual Dashboard

After running the preprocessing, feature engineering, and model selection steps,
launch `dashboard.py` with Streamlit to view key metrics:

```bash
streamlit run dashboard.py
```

The dashboard displays price charts with moving averages, RSI and volatility
curves, the latest model accuracy scores, and a snapshot of recent option
features.

## Disclaimer

This project is for educational purposes only. Trading options involves significant risk, and no outcome is guaranteed. You are solely responsible for any trades executed using code or models derived from this repository.
