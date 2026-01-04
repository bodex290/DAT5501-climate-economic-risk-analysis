def load_csv(path: str):
    """Load CSV and return DataFrame."""
    # read csv
    # return df

def validate_required_columns(df, required_cols: list):
    """Assert required columns exist; raise informative error if not."""
    # check set inclusion
    # raise ValueError if missing

def filter_owid_aggregates(df):
    """Remove OWID aggregates (World, regions)."""
    # drop rows where iso_code startswith 'OWID_'
    # return df

def load_co2_data(path: str):
    """Load and minimally prepare CO2 dataset."""
    # df = load_csv
    # validate columns: iso_code, country, year, co2_per_capita
    # filter aggregates
    # select columns
    # return df

def load_gdp_data(path: str):
    """Load and minimally prepare GDP dataset."""
    # df = load_csv
    # validate columns: iso_code, country, year, gdp_per_capita
    # filter aggregates
    # select columns
    # return df