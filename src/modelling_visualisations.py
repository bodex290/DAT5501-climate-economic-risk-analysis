from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_scatter_with_fit(country_df: pd.DataFrame, x: str, y: str, model, output_path: str, title: str,
                          x_label: str, y_label: str) -> None:
    """
    Scatter plot of x vs y with fitted regression line from a statsmodels OLS model.
    """
    outpath = Path(output_path)
    outpath.parent.mkdir(parents=True, exist_ok=True)

    # Clean
    df = country_df[[x, y]].dropna()

    # Scatter
    plt.figure()
    plt.scatter(df[x], df[y], alpha=0.5)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # Fit line (hold other predictors constant at their mean)
    x_min, x_max = df[x].min(), df[x].max()
    x_vals = pd.Series([x_min, x_max])

    # Build design rows for prediction based on model exog names
    exog_names = list(model.model.exog_names)  # e.g. ['const','avg_co2_per_capita','baseline_gdp_pc']
    pred_rows = []
    for xv in x_vals:
        row = {}
        for name in exog_names:
            if name == "const":
                row[name] = 1.0
            elif name == x:
                row[name] = float(xv)
            else:
                # set controls to mean values
                if name in country_df.columns:
                    row[name] = float(country_df[name].mean())
        pred_rows.append(row)

    pred_df = pd.DataFrame(pred_rows)[exog_names]
    y_pred = model.predict(pred_df)

    plt.plot(x_vals, y_pred)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_residuals_vs_fitted(model, output_path: str, title: str) -> None:
    """
    Residuals vs fitted plot for quick model diagnostics.
    """
    outpath = Path(output_path)
    outpath.parent.mkdir(parents=True, exist_ok=True)

    fitted = model.fittedvalues
    resid = model.resid

    plt.figure()
    plt.scatter(fitted, resid, alpha=0.5)
    plt.axhline(0)
    plt.xlabel("Fitted values")
    plt.ylabel("Residuals")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_coefficients(summary_df: pd.DataFrame, output_path: str, title: str) -> None:
    """
    Plot regression coefficients with simple error bars (±1 std error).
    Expects output from summarise_model() with columns:
    variable, coefficient, std_error
    """
    outpath = Path(output_path)
    outpath.parent.mkdir(parents=True, exist_ok=True)

    df = summary_df.copy()
    # Drop intercept for a cleaner plot (optional)
    df = df[df["variable"] != "const"]

    plt.figure()
    plt.errorbar(df["variable"], df["coefficient"], yerr=df["std_error"], fmt="o")
    plt.axhline(0)
    plt.xlabel("Predictor")
    plt.ylabel("Coefficient (±1 SE)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()