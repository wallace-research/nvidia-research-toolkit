"""
metrics.py
----------
Performance calculations and a simple illustrative DCF for NVIDIA.
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Dict


def total_return(prices: pd.Series) -> float:
    """Total return from first to last observation."""
    if len(prices) < 2:
        return np.nan
    start, end = prices.iloc[0], prices.iloc[-1]
    if start == 0 or pd.isna(start):
        return np.nan
    return (end / start) - 1.0


def period_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    For each ticker column, compute:
    - 1-month, 3-month, 6-month, YTD, and 1-year returns
    """
    results = []

    for ticker in prices.columns:
        series = prices[ticker].dropna()
        if series.empty:
            continue

        last_date = series.index[-1]
        last_price = series.iloc[-1]

        def ret_from(days: int) -> float:
            target = last_date - pd.Timedelta(days=days)
            past = series[series.index <= target]
            if past.empty:
                return np.nan
            return (last_price / past.iloc[-1]) - 1.0

        # Year-to-date
        ytd_start = pd.Timestamp(year=last_date.year, month=1, day=1)
        past_ytd = series[series.index >= ytd_start]
        r_ytd = (last_price / past_ytd.iloc[0]) - 1.0 if len(past_ytd) >= 2 else np.nan

        results.append({
            "ticker": ticker,
            "1m_return": ret_from(30),
            "3m_return": ret_from(90),
            "6m_return": ret_from(180),
            "ytd_return": r_ytd,
            "1y_return": ret_from(365),
            "last_price": round(last_price, 2),
            "last_date": last_date.date(),
        })

    return pd.DataFrame(results)


def relative_to_spy(returns_df: pd.DataFrame) -> pd.DataFrame:
    """Add a column showing 1-year excess return versus SPY."""
    if "SPY" not in returns_df["ticker"].values:
        print("Warning: SPY not found – skipping relative performance")
        return returns_df

    spy_1y = returns_df.loc[returns_df["ticker"] == "SPY", "1y_return"].values[0]
    df = returns_df.copy()
    df["rel_1y_vs_spy"] = df["1y_return"] - spy_1y
    return df


def simple_dcf(
    free_cash_flow: float,
    growth_rate: float = 0.15,
    terminal_growth: float = 0.03,
    discount_rate: float = 0.10,
    years: int = 5,
) -> Dict[str, float]:
    """
    Simplified illustrative DCF.

    - Projects FCF for `years` at a constant growth rate
    - Applies a Gordon-growth terminal value
    - Discounts everything back to present value

    This is a teaching tool only. Real valuations require far more
    detailed forecasts, a proper WACC, and sensitivity analysis.
    """
    if discount_rate <= terminal_growth:
        raise ValueError("Discount rate must exceed terminal growth rate")

    explicit = []
    for t in range(1, years + 1):
        fcf_t = free_cash_flow * ((1 + growth_rate) ** t)
        pv = fcf_t / ((1 + discount_rate) ** t)
        explicit.append({"year": t, "fcf": fcf_t, "pv": pv})

    fcf_n = explicit[-1]["fcf"]
    terminal = fcf_n * (1 + terminal_growth) / (discount_rate - terminal_growth)
    terminal_pv = terminal / ((1 + discount_rate) ** years)

    total_pv = sum(c["pv"] for c in explicit) + terminal_pv

    return {
        "enterprise_value_approx": total_pv,
        "sum_pv_explicit_years": sum(c["pv"] for c in explicit),
        "terminal_value": terminal,
        "pv_of_terminal": terminal_pv,
        "assumptions": {
            "starting_fcf": free_cash_flow,
            "growth_rate_explicit": growth_rate,
            "terminal_growth": terminal_growth,
            "discount_rate": discount_rate,
            "projection_years": years,
        },
        "year_by_year": explicit,
    }


if __name__ == "__main__":
    print("Illustrative DCF with $50bn starting FCF, 15% growth, 10% discount:")
    result = simple_dcf(50_000)  # $ millions
    for k, v in result.items():
        if k != "year_by_year":
            print(f"  {k}: {v}")
