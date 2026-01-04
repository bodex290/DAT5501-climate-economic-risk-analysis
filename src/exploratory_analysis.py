import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def plot_global_trends(df: pd.DataFrame, output_dir: str):
    """
    Plot global median CO2 per capita and GDP per capita over time.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = (
        df.groupby("year")
        .agg(
            median_co2=("co2_per_capita", "median"),
            median_gdp=("gdp_per_capita", "median"),
        )
        .reset_index()
    )

    # CO2 trend
    plt.figure()
    plt.plot(summary["year"], summary["median_co2"])
    plt.xlabel("Year")
    plt.ylabel("CO₂ emissions per capita (tonnes per person)")
    plt.title("Global Median CO₂ Emissions per Capita Over Time")
    plt.tight_layout()
    plt.savefig(output_dir / "global_co2_trend.png")
    plt.close()

    # GDP trend
    plt.figure()
    plt.plot(summary["year"], summary["median_gdp"])
    plt.xlabel("Year")
    plt.ylabel("GDP per capita (constant international $)")
    plt.title("Global Median GDP per Capita Over Time")
    plt.tight_layout()
    plt.savefig(output_dir / "global_gdp_trend.png")
    plt.close()

def plot_scatter_co2_vs_gdp(df: pd.DataFrame, output_dir: str):
    """
    Scatter plot of CO2 per capita vs GDP per capita.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    sample = df.dropna(subset=["co2_per_capita", "gdp_per_capita"])

    plt.figure()
    plt.scatter(sample["co2_per_capita"], sample["gdp_per_capita"], alpha=0.3)
    plt.xlabel("CO₂ emissions per capita (tonnes per person)")
    plt.ylabel("GDP per capita (constant international $)")
    plt.title("CO₂ Emissions vs GDP per Capita")
    plt.tight_layout()
    plt.savefig(output_dir / "co2_vs_gdp_scatter.png")
    plt.close()

def plot_volatility_by_emission_group(df: pd.DataFrame, output_dir: str):
    """
    Compare GDP growth volatility across emission groups.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = df.dropna(subset=["gdp_growth_volatility_5y", "emission_group"])

    groups = ["low", "mid", "high"]
    values = [
        data.loc[data["emission_group"] == g, "gdp_growth_volatility_5y"]
        for g in groups
        if g in data["emission_group"].unique()
    ]

    plt.figure()
    plt.boxplot(values, labels=[g for g in groups if g in data["emission_group"].unique()])
    plt.xlabel("Emission Group")
    plt.ylabel("GDP Growth Volatility (5-year rolling std)")
    plt.title("GDP Growth Volatility by CO₂ Emission Group")
    plt.tight_layout()
    plt.savefig(output_dir / "volatility_by_emission_group.png")
    plt.close()

def plot_country_trajectories(df: pd.DataFrame, iso_codes: list, output_dir: str):
    """
    Plot CO2 and GDP per capita trajectories for selected countries.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for iso in iso_codes:
        subset = df[df["iso_code"] == iso]

        if subset.empty:
            continue

        plt.figure()
        plt.plot(subset["year"], subset["co2_per_capita"], label="CO₂ per capita (tonnes per person)")
        plt.plot(subset["year"], subset["gdp_per_capita"], label="GDP per capita (constant international $)")
        plt.xlabel("Year")
        plt.title(f"{subset.iloc[0]['country']}: CO₂ and GDP Trends")
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_dir / f"{iso}_trajectory.png")
        plt.close()