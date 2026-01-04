import pandas as pd

from src.feature_engineering import (
    add_gdp_growth,
    add_rolling_features,
    add_baseline_gdp,
    add_emission_groups,
    summarise_country_metrics,
)


def make_small_df():
    return pd.DataFrame(
        {
            "country": ["A"] * 6,
            "iso_code": ["AAA"] * 6,
            "year": [2000, 2001, 2002, 2003, 2004, 2005],
            "co2_per_capita": [1, 2, 3, 4, 5, 6],
            "gdp_per_capita": [100, 110, 121, 133.1, 146.41, 161.051],
        }
    )


def test_add_gdp_growth_creates_column_and_first_is_nan():
    df = make_small_df()
    out = add_gdp_growth(df)
    assert "gdp_pc_growth" in out.columns
    assert pd.isna(out.sort_values("year").iloc[0]["gdp_pc_growth"])


def test_add_rolling_features_creates_columns():
    df = add_gdp_growth(make_small_df())
    out = add_rolling_features(df, window=5)
    assert "co2_pc_rolling_5y" in out.columns
    assert "gdp_growth_volatility_5y" in out.columns


def test_add_baseline_gdp_sets_baseline_value():
    df = make_small_df()
    out = add_baseline_gdp(df, baseline_year=2000)
    assert "baseline_gdp_pc" in out.columns
    assert (out["baseline_gdp_pc"] == 100).all()


def test_add_emission_groups_creates_group_labels():
    df = make_small_df()
    out = add_emission_groups(df, n_groups=3)
    assert "emission_group" in out.columns
    assert out["emission_group"].notna().all()


def test_summarise_country_metrics_outputs_one_row():
    df = add_gdp_growth(make_small_df())
    df = add_baseline_gdp(df, baseline_year=2000)
    summary = summarise_country_metrics(df)
    assert len(summary) == 1
    assert "avg_co2_per_capita" in summary.columns
    assert "gdp_growth_volatility" in summary.columns