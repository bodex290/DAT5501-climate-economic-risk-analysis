def add_gdp_growth(df):
    """Compute year-on-year GDP per capita growth by country."""
    # sort by iso_code, year
    # pct_change grouped by iso_code
    # return df

def add_rolling_stats(df, windows=(5, 10)):
    """Add rolling means and rolling volatility."""
    # for each window:
    # rolling mean of co2_per_capita
    # rolling std of gdp growth
    # return df

def add_baseline_gdp(df, baseline_year: int):
    """Add baseline GDP per capita per country."""
    # for each iso_code: gdp in baseline year
    # merge back as baseline_gdp_pc
    # return df

def add_emission_groups(df, n_groups=3):
    """Assign low/mid/high emission groups by avg CO2."""
    # compute per-country avg co2
    # qcut into tertiles
    # merge labels back
    # return df

def summarise_country_metrics(df):
    """Produce country-level summary for modelling."""
    # groupby iso_code
    # avg co2, mean growth, growth volatility
    # include baseline gdp
    # return summary df