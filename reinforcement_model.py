import argparse
from pathlib import Path
import numpy as np
import pandas as pd

try:
    import gym
    from gym import spaces
    from stable_baselines3 import PPO
    from stable_baselines3.common.vec_env import DummyVecEnv
except ImportError as exc:  # pragma: no cover - handle missing dependency
    raise RuntimeError(
        "stable-baselines3 and gym are required. Try `pip install stable-baselines3 gym`."
    ) from exc


class TradingEnv(gym.Env):
    """A simple trading environment for reinforcement learning."""

    metadata = {"render.modes": ["human"]}

    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__()
        self.df = df.reset_index(drop=True)
        self.features = [
            c for c in ["Close", "close_ma5", "close_ma20", "rsi14", "vol30d"] if c in df.columns
        ]
        shape = (len(self.features),)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=shape, dtype=np.float32)
        self.action_space = spaces.Discrete(2)  # 0=flat, 1=long
        self.current_step = 0

    def _get_obs(self) -> np.ndarray:
        row = self.df.loc[self.current_step, self.features].fillna(0)
        return row.to_numpy(dtype=np.float32)

    def reset(self) -> np.ndarray:  # type: ignore[override]
        self.current_step = 0
        return self._get_obs()

    def step(self, action: int):  # type: ignore[override]
        done = False
        reward = 0.0
        if self.current_step < len(self.df) - 1:
            curr_price = self.df.loc[self.current_step, "Close"]
            next_price = self.df.loc[self.current_step + 1, "Close"]
            if action == 1:
                reward = float((next_price - curr_price) / curr_price)
            self.current_step += 1
            done = self.current_step >= len(self.df) - 1
        obs = self._get_obs()
        info: dict[str, float] = {}
        return obs, reward, done, info


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a simple RL trading agent")
    parser.add_argument(
        "underlying_features",
        help="CSV from feature_engineering.py containing underlying features",
    )
    parser.add_argument(
        "--output", default="models", help="Directory to store the trained RL model"
    )
    parser.add_argument(
        "--timesteps", type=int, default=50000, help="Number of training timesteps"
    )
    args = parser.parse_args()

    df = pd.read_csv(args.underlying_features, parse_dates=["Date"])
    env = DummyVecEnv([lambda: TradingEnv(df)])

    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=args.timesteps)

    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    model_path = output_dir / "ppo_trading"
    model.save(model_path)
    print(f"Saved RL model to {model_path}")


if __name__ == "__main__":
    main()
