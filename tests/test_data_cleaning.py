import pandas as pd

from src.data_cleaning import (
    coerce_types,
    filter_time_range,
    drop_missing_core,
    retain_countries_with_min_years,
    merge_datasets,
)


def test_coerce_types_converts_year_to_int_and_metrics_to_numeric():
    df = pd.DataFrame(
        {
            "country": ["A"],
            "iso_code": ["AAA"],
            "year": ["2000"],
            "co2_per_capita": ["1.23"],
        }
    )
    out = coerce_types(df)
    assert out["year"].dtype.kind in {"i"}  # int
    assert out["co2_per_capita"].dtype.kind in {"f", "i"}  # numeric


def test_filter_time_range_filters_years_inclusive():
    df = pd.DataFrame(
        {
            "iso_code": ["AAA", "AAA", "AAA"],
            "year": [1999, 2000, 2001],
        }
    )
    out = filter_time_range(df, 2000, 2001)
    assert out["year"].min() == 2000
    assert out["year"].max() == 2001
    assert len(out) == 2


def test_drop_missing_core_drops_rows_with_missing_core_cols():
    df = pd.DataFrame(
        {
            "co2_per_capita": [1.0, None],
            "gdp_per_capita": [100.0, 200.0],
        }
    )
    out = drop_missing_core(df, ["co2_per_capita", "gdp_per_capita"])
    assert len(out) == 1


def test_retain_countries_with_min_years_keeps_only_valid():
    df = pd.DataFrame(
        {
            "iso_code": ["AAA"] * 3 + ["BBB"] * 1,
            "year": [2000, 2001, 2002, 2000],
        }
    )
    out = retain_countries_with_min_years(df, min_years=2)
    assert set(out["iso_code"].unique()) == {"AAA"}


def test_merge_datasets_inner_merge_on_iso_year():
    co2_df = pd.DataFrame(
        {
            "country": ["A", "A", "B"],
            "iso_code": ["AAA", "AAA", "BBB"],
            "year": [2000, 2001, 2000],
            "co2_per_capita": [1.0, 1.1, 2.0],
        }
    )
    gdp_df = pd.DataFrame(
        {
            "country": ["A", "B"],
            "iso_code": ["AAA", "BBB"],
            "year": [2000, 2000],
            "gdp_per_capita": [100.0, 200.0],
        }
    )
    merged = merge_datasets(co2_df, gdp_df)
    assert {"country", "iso_code", "year", "co2_per_capita", "gdp_per_capita"}.issubset(merged.columns)
    # only rows with matching iso_code+year remain (AAA-2000 and BBB-2000)
    assert len(merged) == 2