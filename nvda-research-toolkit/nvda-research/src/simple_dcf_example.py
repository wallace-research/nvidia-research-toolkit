from __future__ import annotations

from src.metrics import simple_dcf


def main() -> None:
    print("=" * 60)
    print("Illustrative DCF for NVIDIA")
    print("=" * 60)
    print(
        "\nThis example uses round numbers so the logic is easy to follow.\n"
        "It is NOT a real valuation or investment recommendation.\n"
    )

    starting_fcf = 50_000          # $ millions
    growth = 0.15
    terminal_g = 0.03
    discount = 0.10
    years = 5

    result = simple_dcf(
        free_cash_flow=starting_fcf,
        growth_rate=growth,
        terminal_growth=terminal_g,
        discount_rate=discount,
        years=years,
    )

    print("Assumptions")
    for k, v in result["assumptions"].items():
        print(f"  {k:25}: {v}")

    print("\nYear-by-year explicit forecast")
    print(f"  {'Year':<6} {'FCF ($m)':>12} {'PV ($m)':>12}")
    for row in result["year_by_year"]:
        print(f"  {row['year']:<6} {row['fcf']:>12,.0f} {row['pv']:>12,.0f}")

    print("\nSummary")
    print(f"  Sum of PV (years 1-{years})     : ${result['sum_pv_explicit_years']:,.0f} m")
    print(f"  Terminal value at year {years}    : ${result['terminal_value']:,.0f} m")
    print(f"  PV of terminal value         : ${result['pv_of_terminal']:,.0f} m")
    print(f"  Approximate enterprise value : ${result['enterprise_value_approx']:,.0f} m")

    print(
        "\nA production-quality DCF would replace these constant-growth "
        "assumptions with detailed revenue, margin, capex, and working-capital "
        "forecasts, a carefully constructed WACC, and full sensitivity tables."
    )


if __name__ == "__main__":
    main()
