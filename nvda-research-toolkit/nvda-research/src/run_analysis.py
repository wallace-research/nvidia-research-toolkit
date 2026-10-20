from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd
from src.data_fetch import download_price_history, download_nvda_info, save_prices_to_csv
from src.metrics import period_returns, relative_to_spy, simple_dcf


def fmt_pct(x) -> str:
    if pd.isna(x):
        return "N/A"
    return f"{x:.2%}"


def main() -> None:
    print("=" * 64)
    print("  NVDA Research Toolkit")
    print("=" * 64)

    # ------------------------------------------------------------------
    # 1. Prices
    # ------------------------------------------------------------------
    print("\n[1/4] Downloading NVDA + SPY price history (5 years)...")
    prices = download_price_history(["NVDA", "SPY"], period="5y")
    save_prices_to_csv(prices, "nvda_spy_prices.csv", folder=ROOT / "data")

    # ------------------------------------------------------------------
    # 2. Performance table
    # ------------------------------------------------------------------
    print("\n[2/4] Calculating returns...")
    returns = period_returns(prices)
    returns = relative_to_spy(returns)

    # Pretty version for printing
    display = returns.copy()
    for col in ["1m_return", "3m_return", "6m_return", "ytd_return", "1y_return", "rel_1y_vs_spy"]:
        if col in display.columns:
            display[col] = display[col].map(fmt_pct)

    print("\nPerformance summary:")
    print(display.to_string(index=False))

    out_path = ROOT / "output" / "nvda_performance.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    returns.to_csv(out_path, index=False)
    print(f"\nSaved → {out_path}")

    # ------------------------------------------------------------------
    # 3. Fundamental snapshot
    # ------------------------------------------------------------------
    print("\n[3/4] NVIDIA fundamental snapshot...")
    info = download_nvda_info()
    for k, v in info.items():
        if k == "marketCap" and isinstance(v, (int, float)):
            print(f"  {k:20}: ${v/1e9:.1f} billion")
        else:
            print(f"  {k:20}: {v}")

    # ------------------------------------------------------------------
    # 4. Illustrative DCF
    # ------------------------------------------------------------------
    print("\n[4/4] Illustrative DCF (teaching example only)...")
    print("  Assumptions: starting FCF = $50 billion, explicit growth 15%,")
    print("               terminal growth 3%, discount rate 10%, 5-year horizon.")
    print("  These numbers are illustrative – not a recommendation.\n")

    dcf = simple_dcf(
        free_cash_flow=50_000,   # $ millions
        growth_rate=0.15,
        terminal_growth=0.03,
        discount_rate=0.10,
        years=5,
    )

    print(f"  Sum of PV (explicit years) : ${dcf['sum_pv_explicit_years']:,.0f} m")
    print(f"  Terminal value             : ${dcf['terminal_value']:,.0f} m")
    print(f"  PV of terminal value       : ${dcf['pv_of_terminal']:,.0f} m")
    print(f"  Approx. enterprise value   : ${dcf['enterprise_value_approx']:,.0f} m")

    # Save a small DCF summary
    dcf_summary = pd.DataFrame([{
        "starting_fcf_m": 50_000,
        "growth_explicit": 0.15,
        "terminal_growth": 0.03,
        "discount_rate": 0.10,
        "years": 5,
        "enterprise_value_m": round(dcf["enterprise_value_approx"]),
        "pv_explicit_m": round(dcf["sum_pv_explicit_years"]),
        "pv_terminal_m": round(dcf["pv_of_terminal"]),
    }])
    dcf_path = ROOT / "output" / "nvda_illustrative_dcf.csv"
    dcf_summary.to_csv(dcf_path, index=False)
    print(f"\nSaved → {dcf_path}")

    print("\n" + "=" * 64)
    print("Done. Open the CSVs in the output/ and data/ folders to explore further.")
    print("=" * 64)


if __name__ == "__main__":
    main()
