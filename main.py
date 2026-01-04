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

from src.exploratory_analysis import (
    plot_global_trends,
    plot_scatter_co2_vs_gdp,
    plot_volatility_by_emission_group,
    plot_country_trajectories
)

from src.modelling import (
    compute_country_level_dataset,
    run_correlations,
    run_regression,
    summarise_model,
)

from src.modelling_visualisations import (
    plot_scatter_with_fit,
    plot_residuals_vs_fitted,
    plot_coefficients,
)

EDA_DIR = "outputs/figures"
FIG_DIR = "outputs/figures"

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
    # df.to_csv("data/processed/panel_features.csv", index=False)

    # Country-level summary for modelling
    country_summary = summarise_country_metrics(df)
    country_summary.to_csv("data/processed/country_summary.csv", index=False)

    # Exploratory Data Analysis
    plot_global_trends(df, EDA_DIR)
    plot_scatter_co2_vs_gdp(df, EDA_DIR)
    plot_volatility_by_emission_group(df, EDA_DIR)
    plot_country_trajectories(df, ["USA", "CHN"], EDA_DIR)

    print(df[["country","iso_code","year","gdp_pc_growth","co2_pc_rolling_5y","gdp_growth_volatility_5y","baseline_gdp_pc","emission_group"]].head(12))
    print(country_summary.head())

    # Country-level dataset for modelling
    country_df = compute_country_level_dataset(df)
    country_df.to_csv("data/processed/country_level_model_dataset.csv", index=False)

    # Correlation analysis
    corr_df = run_correlations(country_df)
    corr_df.to_csv("outputs/tables/correlations.csv", index=False)

    # Regression 1: volatility
    vol_model = run_regression(
        country_df,
        y_col="gdp_growth_volatility",
        x_cols=["avg_co2_per_capita", "baseline_gdp_pc"],   
    )
    vol_summary = summarise_model(vol_model)
    vol_summary.to_csv("outputs/tables/regression_volatility_summary.csv", index=False)

    # Regression 2: mean growth
    growth_model = run_regression(
        country_df,
        y_col="mean_gdp_growth",
        x_cols=["avg_co2_per_capita", "baseline_gdp_pc"],
    )
    growth_summary = summarise_model(growth_model)
    growth_summary.to_csv("outputs/tables/regression_growth_summary.csv", index=False)

    # print(vol_summary)
    # print(growth_summary)

    df.to_csv("data/processed/panel.csv", index=False)

    # 1) Scatter + fit: CO2 vs volatility (controls held at mean)
    plot_scatter_with_fit(
        country_df,
        x="avg_co2_per_capita",
        y="gdp_growth_volatility",
        model=vol_model,
        output_path=f"{FIG_DIR}/model_scatter_co2_vs_volatility.png",
        title="CO₂ Exposure vs GDP Growth Volatility (Country-level)",
        x_label="Average CO₂ per capita (tonnes per person)",
        y_label="GDP growth volatility (std dev of growth rate)",
    )

# 2) Residual diagnostics (optional but strong)
    plot_residuals_vs_fitted(
        vol_model,
        output_path=f"{FIG_DIR}/model_residuals_volatility.png",
        title="Residuals vs Fitted Values (Volatility Model)",
    )

# 3) Coefficient plot for volatility model
    plot_coefficients(
        vol_summary,
        output_path=f"{FIG_DIR}/model_coefficients_volatility.png",
        title="Regression Coefficients (Volatility Model)",
    )

# (Optional) also visualise the growth model coefficients
    plot_coefficients(
        growth_summary,
        output_path=f"{FIG_DIR}/model_coefficients_growth.png",
        title="Regression Coefficients (Growth Model)",
    )

if __name__ == "__main__":
    main()