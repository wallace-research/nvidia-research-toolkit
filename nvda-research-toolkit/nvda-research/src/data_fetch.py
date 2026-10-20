from __future__ import annotations

import yfinance as yf
import pandas as pd
from pathlib import Path
from typing import List


def download_price_history(
    tickers: List[str] | None = None,
    period: str = "5y",
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Download adjusted close prices.

    Default tickers are NVDA + SPY (the benchmark used throughout this project).
    """
    if tickers is None:
        tickers = ["NVDA", "SPY"]

    data = yf.download(
        tickers=tickers,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
        threads=True,
    )

    if len(tickers) == 1:
        close = data["Close"].to_frame(name=tickers[0])
    else:
        close = data["Close"]

    close = close.dropna(how="all")
    return close


def download_nvda_info() -> dict:
    """
    Pull a concise set of fundamental fields for NVIDIA.
    Returns a plain dictionary that is easy to print or inspect.
    """
    t = yf.Ticker("NVDA")
    info = t.info

    keys = [
        "shortName",
        "sector",
        "industry",
        "marketCap",
        "trailingPE",
        "forwardPE",
        "priceToBook",
        "dividendYield",
        "beta",
        "fiftyTwoWeekHigh",
        "fiftyTwoWeekLow",
        "currency",
        "fullTimeEmployees",
        "website",
    ]

    summary = {k: info.get(k) for k in keys}
    summary["ticker"] = "NVDA"
    return summary


def save_prices_to_csv(
    prices: pd.DataFrame,
    filename: str = "nvda_prices.csv",
    folder: str | Path = "data",
) -> Path:
    """Save a price DataFrame to CSV inside the data/ folder."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / filename
    prices.to_csv(path)
    print(f"Saved → {path}")
    return path


if __name__ == "__main__":
    print("Downloading NVDA + SPY (5 years)...")
    prices = download_price_history()
    print(prices.tail())
    save_prices_to_csv(prices)
    print("\nNVIDIA snapshot:")
    for k, v in download_nvda_info().items():
        print(f"  {k:20}: {v}")
