# DAT5501 Climate–Economic Risk Analysis

This project investigates the relationship between **per-capita CO₂ emissions** and **economic outcomes** (GDP per capita growth and volatility) using country-level panel data. The analysis builds a reproducible pipeline that:
- loads and cleans two OWID-style datasets,
- engineers features (growth, rolling exposure, volatility, emission groups, baseline controls),
- produces EDA figures and modelling outputs (correlations + OLS regression),
- and validates key steps with automated unit tests and CI.

## Research question and hypothesis

**Research question:**  
How are long-run CO₂ emissions per capita associated with economic performance and stability across countries?

**Working hypothesis:**  
Countries with higher long-term per-capita CO₂ emissions exhibit **greater GDP per capita growth volatility** and potentially **lower average GDP per capita growth**, even after controlling for baseline income.

## Data sources

Two CSV datasets are used (placed in `data/raw/`):
- **CO₂ emissions per capita** (OWID-style export)
- **GDP per capita** (Maddison Project Database / OWID-style export)

> Note: Column names are harmonised into a standard schema during loading/cleaning.

## Repository structure

```text
.
├── main.py
├── requirements.txt
├── README.md
├── data/
│   ├── raw/               # source CSVs (input)
│   └── processed/         # generated cleaned + feature datasets (output)
├── outputs/
│   ├── figures/           # saved plots for EDA + modelling
│   └── tables/            # saved CSV tables (correlations + regressions)
├── notebooks/
│   └── exploration.ipynb  # lightweight exploratory checks (optional)
├── src/
│   ├── data_loading.py
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── exploratory_analysis.py
│   ├── modelling.py
│   ├── modelling_visualisations.py
│   └── utils.py
└── tests/
    ├── conftest.py
    ├── test_data_loading.py
    ├── test_data_cleaning.py
    ├── test_feature_engineering.py
    ├── test_models.py
    └── test_modelling_visualisations.py