import pandas as pd
import pytest

from src.data_loading import (
    standardise_owid_columns,
    validate_required_columns,
    drop_non_country_rows,
    load_co2_data,
    load_gdp_data,
)


def test_standardise_owid_columns_renames_expected_headers():
    df = pd.DataFrame(
        {
            "Entity": ["A"],
            "Code": ["AAA"],
            "Year": [2000],
            "SomeValue": [1.0],
        }
    )
    out = standardise_owid_columns(df)
    assert {"country", "iso_code", "year"}.issubset(out.columns)


def test_validate_required_columns_raises_on_missing():
    df = pd.DataFrame({"a": [1]})
    with pytest.raises(ValueError):
        validate_required_columns(df, ["a", "missing_col"])


def test_drop_non_country_rows_removes_missing_iso_code():
    df = pd.DataFrame(
        {
            "country": ["World", "Afghanistan"],
            "iso_code": [None, "AFG"],
            "year": [2000, 2000],
        }
    )
    out = drop_non_country_rows(df)
    assert out["iso_code"].isna().sum() == 0
    assert len(out) == 1
    assert out.iloc[0]["iso_code"] == "AFG"


def test_load_co2_data_outputs_standard_schema():
    df = load_co2_data("data/raw/owid_co2.csv")
    assert list(df.columns) == ["country", "iso_code", "year", "co2_per_capita"]
    assert df["iso_code"].notna().all()
    assert df["year"].notna().all()


def test_load_gdp_data_outputs_standard_schema():
    df = load_gdp_data("data/raw/owid_gdp_per_capita.csv")
    assert list(df.columns) == ["country", "iso_code", "year", "gdp_per_capita"]
    assert df["iso_code"].notna().all()
    assert df["year"].notna().all()