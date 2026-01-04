import pandas as pd

def coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure correct data types.
    """
    df = df.copy()
    df["year"] = df["year"].astype(int)

    for col in df.columns:
        if col not in ["iso_code", "country", "year"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def filter_time_range(df: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
    """
    Filter data to analysis time window.
    """
    return df[(df["year"] >= start_year) & (df["year"] <= end_year)]

def drop_missing_core(df: pd.DataFrame, core_cols: list) -> pd.DataFrame:
    """
    Drop rows missing essential variables.
    """
    return df.dropna(subset=core_cols)

def retain_countries_with_min_years(df: pd.DataFrame, min_years: int) -> pd.DataFrame:
    """
    Retain countries with suffficient time coverage.
    """
    counts = df.groupby("iso_code")["year"].nunique()
    valid_iso = counts[counts >= min_years].index
    return df[df["iso_code"].isin(valid_iso)]

def merge_datasets(co2_df: pd.DataFrame, gdp_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge CO₂ and GDP datasets on iso_code and year.
    """
    df = pd.merge(
        co2_df,
        gdp_df,
        on=["iso_code", "year"],
        how="inner",
        suffixes=("_co2", "_gdp")
    )

    # Keep a single country column
    if "country_co2" in df.columns:
        df = df.rename(columns={"country_co2": "country"})
        df = df.drop(columns=["country_gdp"], errors="ignore")

    return df