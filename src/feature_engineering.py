import numpy as np
import pandas as pd


def add_gdp_growth(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add year-on-year GDP per capita growth rate per country.
    Growth is computed as pct_change of gdp_per_capita within each iso_code.
    """
    out = df.copy()
    out = out.sort_values(["iso_code", "year"])
    out["gdp_pc_growth"] = (
        out.groupby("iso_code")["gdp_per_capita"]
        .pct_change()
    )
    return out


def add_rolling_features(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """
    Add rolling CO2 exposure (mean) and rolling GDP growth volatility (std dev)
    per country using a specified window (default 5 years).

    min_periods=window ensures we only compute once a full window exists.
    """
    out = df.copy()
    out = out.sort_values(["iso_code", "year"])

    out[f"co2_pc_rolling_{window}y"] = (
        out.groupby("iso_code")["co2_per_capita"]
        .rolling(window=window, min_periods=window)
        .mean()
        .reset_index(level=0, drop=True)
    )

    out[f"gdp_growth_volatility_{window}y"] = (
        out.groupby("iso_code")["gdp_pc_growth"]
        .rolling(window=window, min_periods=window)
        .std()
        .reset_index(level=0, drop=True)
    )

    return out


def add_baseline_gdp(df: pd.DataFrame, baseline_year: int = 2000) -> pd.DataFrame:
    """
    Add baseline GDP per capita per country (value in baseline_year).
    This is used as a simple control variable in regression.
    """
    out = df.copy()

    baseline = out[out["year"] == baseline_year][["iso_code", "gdp_per_capita"]].copy()
    baseline = baseline.rename(columns={"gdp_per_capita": "baseline_gdp_pc"})

    out = out.merge(baseline, on="iso_code", how="left")
    return out


def add_emission_groups(df: pd.DataFrame, n_groups: int = 3) -> pd.DataFrame:
    """
    Assign emission group labels based on average CO2 per capita per country.
    If there are fewer unique countries than groups, assign a single group.
    """
    out = df.copy()

    country_avg = (
        out.groupby("iso_code", as_index=False)["co2_per_capita"]
        .mean()
        .rename(columns={"co2_per_capita": "avg_co2_per_capita"})
    )

    # If too few countries to form quantiles, assign all to 'mid'
    if country_avg.shape[0] < n_groups:
        country_avg["emission_group"] = "mid"
    else:
        labels = ["low", "mid", "high"] if n_groups == 3 else [f"g{i+1}" for i in range(n_groups)]
        country_avg["emission_group"] = pd.qcut(
            country_avg["avg_co2_per_capita"],
            q=n_groups,
            labels=labels,
            duplicates="drop",
        )

    out = out.merge(
        country_avg[["iso_code", "emission_group"]],
        on="iso_code",
        how="left"
    )
    return out


def summarise_country_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Produce one-row-per-country dataset for modelling.
    Includes:
    - avg_co2_per_capita
    - mean_gdp_growth
    - gdp_growth_volatility (std dev of growth over full period)
    - baseline_gdp_pc (first available baseline value)
    """
    required = {"iso_code", "country", "co2_per_capita", "gdp_pc_growth", "gdp_per_capita"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns for summary: {missing}")

    grp = df.groupby(["iso_code", "country"], as_index=False)

    summary = grp.agg(
        avg_co2_per_capita=("co2_per_capita", "mean"),
        mean_gdp_growth=("gdp_pc_growth", "mean"),
        gdp_growth_volatility=("gdp_pc_growth", "std"),
        avg_gdp_per_capita=("gdp_per_capita", "mean"),
    )

    if "baseline_gdp_pc" in df.columns:
        baseline = (
            df.groupby("iso_code", as_index=False)["baseline_gdp_pc"]
            .first()
        )
        summary = summary.merge(baseline, on="iso_code", how="left")

    return summary