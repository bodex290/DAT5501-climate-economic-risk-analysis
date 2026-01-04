import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm

def compute_country_level_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create one-row-per-country dataset for modelling.
    """
    required = {
        "iso_code",
        "country",
        "co2_per_capita",
        "gdp_pc_growth",
        "gdp_per_capita",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    country_df = (
        df.groupby(["iso_code", "country"], as_index=False)
        .agg(
            avg_co2_per_capita=("co2_per_capita", "mean"),
            mean_gdp_growth=("gdp_pc_growth", "mean"),
            gdp_growth_volatility=("gdp_pc_growth", "std"),
            avg_gdp_per_capita=("gdp_per_capita", "mean"),
            baseline_gdp_pc=("baseline_gdp_pc", "first"),
        )
    )

    return country_df.dropna()

def run_correlations(country_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Pearson and Spearman correlations between CO2 exposure
    and economic stability metrics.
    """
    results = []

    pairs = [
        ("avg_co2_per_capita", "mean_gdp_growth"),
        ("avg_co2_per_capita", "gdp_growth_volatility"),
    ]

    for x, y in pairs:
        pearson_r, pearson_p = stats.pearsonr(country_df[x], country_df[y])
        spearman_r, spearman_p = stats.spearmanr(country_df[x], country_df[y])

        results.append(
            {
                "x": x,
                "y": y,
                "pearson_r": pearson_r,
                "pearson_p": pearson_p,
                "spearman_r": spearman_r,
                "spearman_p": spearman_p,
            }
        )

    return pd.DataFrame(results)

def run_regression(country_df: pd.DataFrame, y_col: str, x_cols: list):
    """
    Run OLS regression with specified dependent and independent variables.
    """
    X = country_df[x_cols]
    X = sm.add_constant(X)
    y = country_df[y_col]

    model = sm.OLS(y, X, missing="drop").fit()
    return model

def summarise_model(model) -> pd.DataFrame:
    """
    Extract tidy regression summary for reporting.
    """
    summary = pd.DataFrame(
        {
            "coefficient": model.params,
            "std_error": model.bse,
            "p_value": model.pvalues,
        }
    )
    summary["r_squared"] = model.rsquared
    return summary.reset_index().rename(columns={"index": "variable"})