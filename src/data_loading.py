import pandas as pd
from pathlib import Path

def load_csv(path: str) -> pd.DataFrame:
    """Load CSV file and return DataFrame.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)


def validate_required_columns(df: pd.DataFrame, required_cols: list):
    """Assert required columns exist; raise informative error if not.
    """
    # check set inclusion
    # raise ValueError if missing

    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
def standardise_owid_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardise common OWID export headers:
    Entity -> country
    Code   -> iso_code
    Year   -> year
    """
    df = df.copy()

    # Rename if present (OWID exports)
    rename_map = {
        "Entity": "country",
        "Code": "iso_code",
        "Year": "year",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    return df

def drop_non_country_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Many OWID exports include aggregates where iso_code is missing.
    Keep only rows that have an iso_code.
    """
    df = df.copy()
    df["iso_code"] = df["iso_code"].astype("string")
    return df[df["iso_code"].notna()]

def filter_owid_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove OWID aggregates (World, regions).
    """
    # drop rows where iso_code startswith 'OWID_'
    return df[~df['iso_code'].str.startswith('OWID_')]

def load_co2_data(path: str) -> pd.DataFrame:
    df = load_csv(path)
    df = standardise_owid_columns(df)

    # Map the indicator column to our internal name
    # Your file uses: "Annual CO₂ emissions (per capita)"
    co2_col = "Annual CO₂ emissions (per capita)"
    validate_required_columns(df, ["country", "iso_code", "year", co2_col])

    df = df.rename(columns={co2_col: "co2_per_capita"})
    df = drop_non_country_rows(df)

    return df[["country", "iso_code", "year", "co2_per_capita"]]

def load_gdp_data(path: str) -> pd.DataFrame:
    df = load_csv(path)
    df = standardise_owid_columns(df)

    gdp_col = "GDP per capita"
    validate_required_columns(df, ["country", "iso_code", "year", gdp_col])

    df = df.rename(columns={gdp_col: "gdp_per_capita"})
    df = drop_non_country_rows(df)

    return df[["country", "iso_code", "year", "gdp_per_capita"]]