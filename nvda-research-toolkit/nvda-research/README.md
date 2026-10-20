# NVIDIA Research Toolkit

A focused Python research project on **NVIDIA Corporation (NVDA)**.

This repository combines:

- Public market data retrieval
- Performance analysis versus the S&P 500 (SPY)
- A simplified illustrative discounted-cash-flow (DCF) model
- Clear, readable Python that a beginner can run and understand

This project is intentionally narrow in scope (NVIDIA) as it is meant to be an introductory Python project.  I am intending for this to complement a broader GitHub finance research website I have built as static HTML/CSS with Excel models.  My intention was to keep the code clean and the analysis  deep enough to be useful as a learning and demonstration project.

> **Disclaimer**  
> Everything in this repository is for personal research and educational purposes only.  
> It is not investment advice. The DCF example uses simplified assumptions and should never be treated as a real valuation.

---

## Project structure

```
nvda-research/
├── README.md                     ← you are here
├── requirements.txt
├── .gitignore
├── src/
│   ├── data_fetch.py             ← download prices & fundamentals
│   ├── metrics.py                ← returns + simple DCF
│   ├── run_analysis.py           ← main script (run this first)
│   └── simple_dcf_example.py     ← short DCF walk-through
├── notebooks/
│   └── 01_nvda_explore.ipynb     ← interactive version
├── data/                         ← downloaded price CSVs land here
└── output/                       ← performance table + DCF summary
```

---

## What the toolkit does

| Component                    | Purpose |
|-----------------------------|---------|
| `run_analysis.py`           | Downloads 5 years of NVDA + SPY prices, calculates multiple return windows, pulls a fundamental snapshot, runs an illustrative DCF, and saves clean CSVs. |
| `simple_dcf_example.py`     | Prints a step-by-step DCF so the arithmetic is easy to follow. |
| `data_fetch.py`             | Reusable helpers for prices and company info. |
| `metrics.py`                | Return calculations and the DCF function. |
| `01_nvda_explore.ipynb`     | Same ideas in an interactive Jupyter notebook (charts included). |

---

## How to run (step-by-step)

### 1. Check that Python is installed

Open a terminal and type:

```bash
python --version
```

or

```bash
python3 --version
```

Python 3.10 or newer is needed.

### 2. Get the code

If you cloned the repository:

```bash
cd nvda-research
```

### 3. Create a virtual environment (recommended)

This keeps the packages for this project separate from the rest of your computer.

**Windows (Command Prompt)**
```bash
python -m venv .venv
.venv\Scripts\activate.bat
```

**Windows (PowerShell)**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Mac / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` at the beginning of your prompt.

### 4. Install the required packages

```bash
pip install -r requirements.txt
```

(Only needs to be done once, or when the requirements change.)

### 5. Run the main analysis

```bash
python -m src.run_analysis
```

This will:

1. Download 5 years of daily prices for NVDA and SPY  
2. Calculate 1-month, 3-month, 6-month, YTD, and 1-year returns  
3. Show how NVDA performed relative to SPY  
4. Print a short fundamental snapshot  
5. Run a simplified illustrative DCF  
6. Save two files you can open in Excel:
   - `data/nvda_spy_prices.csv`
   - `output/nvda_performance.csv`
   - `output/nvda_illustrative_dcf.csv`

### 6. (Optional) Run the short DCF walk-through

```bash
python -m src.simple_dcf_example
```

### 7. (Optional) Explore interactively

```bash
jupyter notebook
```

Then open `notebooks/01_nvda_explore.ipynb` and run the cells one by one.  
To stop the server later, press `Ctrl+C` in the terminal.

### 8. When you are finished

```bash
deactivate
```

---

## Design choices

- **One company only** – This keeps the code and the scope of the project simple.
- **Readability first** – This provides clear variable names, comments, and interpretation.
- **Public data only** – This means that everything comes from free, publicly available sources via `yfinance`.
- **Illustrative DCF** – This DCF uses constant growth rates on purpose so the arithmetic is transparent.  A more in-depth valuation would need detailed forecasts, a proper WACC calculation, and sensitivity analysis.
- **Honest limitations** – This project outlines limitations, and is meant to be straightforward in scope, through the README; the scripts themselves state the project can and can't do.

---

## Ideas for future development (not implemented)

- Sensitivity tables around the DCF assumptions  
- Automatic chart export  
- Comparison against a small peer set (AMD, AVGO, MRVL, etc.)  
- Pulling more detailed financial-statement items
- Pairing/linking to my broader investment website (I can provide the URL to that if desired)

---

## Author

Ty Wallace  
Personal research & Python project centered on NVIDIA.
