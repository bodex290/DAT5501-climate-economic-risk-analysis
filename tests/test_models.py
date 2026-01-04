import pandas as pd

from src.modelling import (
    compute_country_level_dataset,
    run_correlations,
    run_regression,
    summarise_model,
)


def make_panel_df():
    """
    Build a small panel dataset with two countries over multiple years.
    Includes baseline_gdp_pc column to match pipeline.
    """
    return pd.DataFrame(
        {
            "iso_code": ["AAA"] * 6 + ["BBB"] * 6,
            "country": ["A"] * 6 + ["B"] * 6,
            "year": [2000, 2001, 2002, 2003, 2004, 2005] * 2,
            "co2_per_capita": [1, 1.2, 1.3, 1.4, 1.5, 1.6] + [3, 3.1, 3.2, 3.4, 3.5, 3.6],
            "gdp_per_capita": [100, 105, 110, 108, 115, 120] + [200, 198, 205, 210, 208, 215],
            # Pretend baseline is year 2000 GDP repeated per country
            "baseline_gdp_pc": [100] * 6 + [200] * 6,
        }
    )


def test_compute_country_level_dataset_outputs_expected_columns():
    df = make_panel_df()

    # Add a simple growth column like the pipeline does
    df = df.sort_values(["iso_code", "year"])
    df["gdp_pc_growth"] = df.groupby("iso_code")["gdp_per_capita"].pct_change()

    country_df = compute_country_level_dataset(df)

    expected_cols = {
        "iso_code",
        "country",
        "avg_co2_per_capita",
        "mean_gdp_growth",
        "gdp_growth_volatility",
        "avg_gdp_per_capita",
        "baseline_gdp_pc",
    }
    assert expected_cols.issubset(set(country_df.columns))
    assert len(country_df) == 2


def test_run_correlations_returns_expected_rows():
    df = make_panel_df()
    df = df.sort_values(["iso_code", "year"])
    df["gdp_pc_growth"] = df.groupby("iso_code")["gdp_per_capita"].pct_change()

    country_df = compute_country_level_dataset(df)
    corr = run_correlations(country_df)

    # We compute 2 x-y pairs
    assert len(corr) == 2
    assert {"pearson_r", "pearson_p", "spearman_r", "spearman_p"}.issubset(set(corr.columns))


def test_run_regression_and_summary_work():
    df = make_panel_df()
    df = df.sort_values(["iso_code", "year"])
    df["gdp_pc_growth"] = df.groupby("iso_code")["gdp_per_capita"].pct_change()

    country_df = compute_country_level_dataset(df)

    model = run_regression(
        country_df,
        y_col="gdp_growth_volatility",
        x_cols=["avg_co2_per_capita", "baseline_gdp_pc"],
    )

    summary = summarise_model(model)
    assert "variable" in summary.columns
    assert "coefficient" in summary.columns
    assert "p_value" in summary.columns
    # Should include const and both predictors
    assert set(summary["variable"]).issuperset({"const", "avg_co2_per_capita", "baseline_gdp_pc"})