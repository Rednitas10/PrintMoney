import argparse
from pathlib import Path
import pandas as pd


def add_macd(df: pd.DataFrame) -> pd.DataFrame:
    close = df["Close"]
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    df["macd"] = macd
    df["macd_signal"] = signal
    cross_up = (macd > signal) & (macd.shift() <= signal.shift())
    cross_down = (macd < signal) & (macd.shift() >= signal.shift())
    position = pd.Series(0, index=df.index, dtype=int)
    position[cross_up] = 1
    position[cross_down] = 0
    df["macd_position"] = position.ffill().fillna(0)
    df["macd_returns"] = df["returns"] * df["macd_position"].shift()
    return df


def add_awesome_oscillator(df: pd.DataFrame) -> pd.DataFrame:
    median = (df["High"] + df["Low"]) / 2
    ao = median.rolling(window=5).mean() - median.rolling(window=34).mean()
    df["ao"] = ao
    cross_up = (ao > 0) & (ao.shift() <= 0)
    cross_down = (ao < 0) & (ao.shift() >= 0)
    position = pd.Series(0, index=df.index, dtype=int)
    position[cross_up] = 1
    position[cross_down] = 0
    df["ao_position"] = position.ffill().fillna(0)
    df["ao_returns"] = df["returns"] * df["ao_position"].shift()
    return df


def add_bollinger(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    ma = df["Close"].rolling(window=window).mean()
    std = df["Close"].rolling(window=window).std()
    upper = ma + 2 * std
    lower = ma - 2 * std
    df["bb_mid"] = ma
    df["bb_upper"] = upper
    df["bb_lower"] = lower
    buy = (df["Close"].shift(1) < lower.shift(1)) & (df["Close"] >= lower)
    sell = (df["Close"].shift(1) > ma.shift(1)) & (df["Close"] <= ma)
    position = pd.Series(0, index=df.index, dtype=int)
    position[buy] = 1
    position[sell] = 0
    df["bb_position"] = position.ffill().fillna(0)
    df["bb_returns"] = df["returns"] * df["bb_position"].shift()
    return df


def backtest(df: pd.DataFrame) -> pd.DataFrame:
    strategies = {
        "MACD": "macd_returns",
        "AO": "ao_returns",
        "Bollinger": "bb_returns",
    }
    results = []
    for name, col in strategies.items():
        cum = (1 + df[col].fillna(0)).cumprod() - 1
        results.append({"strategy": name, "cumulative_return": cum.iloc[-1]})
    return pd.DataFrame(results)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare basic trading strategies")
    parser.add_argument("features", help="CSV from feature_engineering.py containing underlying features")
    args = parser.parse_args()
    df = pd.read_csv(args.features, parse_dates=["Date"])
    if "returns" not in df.columns:
        df["returns"] = df["Close"].pct_change()
    df = add_macd(df)
    df = add_awesome_oscillator(df)
    df = add_bollinger(df)
    results = backtest(df)
    for _, row in results.iterrows():
        print(f"{row['strategy']} cumulative return: {row['cumulative_return']:.2%}")


if __name__ == "__main__":
    main()
