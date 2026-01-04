def coerce_types(df):
    """Ensure numeric columns are numeric and year is int."""
    # astype conversions
    # coerce errors to NaN

def filter_time_range(df, start_year: int, end_year: int):
    """Restrict data to analysis window."""
    # df[(year >= start) & (year <= end)]

def drop_missing_core(df, core_cols: list):
    """Drop rows missing essential variables."""
    # df.dropna(subset=core_cols)

def retain_countries_with_min_years(df, min_years: int):
    """Keep countries with sufficient time coverage."""
    # groupby iso_code -> count years
    # filter eligible countries

def merge_datasets(co2_df, gdp_df):
    """Merge CO2 and GDP on iso_code + year."""
    # merge inner
    # resolve country column
    # return merged df