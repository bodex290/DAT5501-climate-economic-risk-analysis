from src.data_loading import load_co2_data, load_gdp_data
from src.data_cleaning import (
    coerce_types,
    filter_time_range,
    drop_missing_core,
    retain_countries_with_min_years,
    merge_datasets
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

    print(df.shape)
    print(df.head())

    df.to_csv("data/processed/panel.csv", index=False)

if __name__ == "__main__":
    main()