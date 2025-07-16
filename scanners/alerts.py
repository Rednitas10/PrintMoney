"""Simple alerting utilities."""
from datetime import datetime


def send_alert(message: str) -> None:
    """Send an alert message by printing with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[ALERT {timestamp}] {message}")
