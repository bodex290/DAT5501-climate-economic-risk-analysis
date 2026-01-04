from src.data_loading import load_co2_data, load_gdp_data
from src.data_cleaning import (
    coerce_types,
    filter_time_range,
    drop_missing_core,
    retain_countries_with_min_years,
    merge_datasets
)

from src.feature_engineering import (
    add_gdp_growth,
    add_rolling_features,
    add_baseline_gdp,
    add_emission_groups,
    summarise_country_metrics,
)


START_YEAR = 2000
END_YEAR = 2023
MIN_YEARS = 20

def main():
    co2 = load_co2_data("data/raw/owid_co2.csv")
    gdp = load_gdp_data("data/raw/owid_gdp_per_capita.csv")

    co2 = coerce_types(co2)
    gdp = coerce_types(gdp)

    co2 = filter_time_range(co2, START_YEAR, END_YEAR)
    gdp = filter_time_range(gdp, START_YEAR, END_YEAR)

    df = merge_datasets(co2, gdp)
    df = drop_missing_core(df, ["co2_per_capita", "gdp_per_capita"])
    df = retain_countries_with_min_years(df, MIN_YEARS)

    # Feature engineering
    df = add_gdp_growth(df)
    df = add_rolling_features(df, window=5)
    df = add_baseline_gdp(df, baseline_year=2000)
    df = add_emission_groups(df, n_groups=3)

    # Save feature table
    df.to_csv("data/processed/panel_features.csv", index=False)

    # Country-level summary for modelling
    country_summary = summarise_country_metrics(df)
    country_summary.to_csv("data/processed/country_summary.csv", index=False)

    print(df[["country","iso_code","year","gdp_pc_growth","co2_pc_rolling_5y","gdp_growth_volatility_5y","baseline_gdp_pc","emission_group"]].head(12))
    print(country_summary.head())

    # df.to_csv("data/processed/panel.csv", index=False)

if __name__ == "__main__":
    main()