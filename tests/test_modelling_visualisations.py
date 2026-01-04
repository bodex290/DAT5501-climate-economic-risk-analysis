from pathlib import Path
import pandas as pd

from src.modelling import run_regression
from src.modelling_visualisations import plot_residuals_vs_fitted


def test_plot_residuals_creates_file(tmp_path: Path):
    # tiny dataset for model
    df = pd.DataFrame(
        {
            "avg_co2_per_capita": [1.0, 2.0, 3.0],
            "baseline_gdp_pc": [100, 150, 200],
            "gdp_growth_volatility": [0.02, 0.03, 0.05],
        }
    )
    model = run_regression(df, y_col="gdp_growth_volatility", x_cols=["avg_co2_per_capita", "baseline_gdp_pc"])
    out = tmp_path / "resid.png"
    plot_residuals_vs_fitted(model, str(out), "Residuals Test")
    assert out.exists()