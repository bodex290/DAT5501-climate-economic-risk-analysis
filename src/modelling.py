def compute_country_level_dataset(df):
    """Create one-row-per-country modelling dataset."""
    # call summarise_country_metrics
    # drop missing
    # return df

def run_correlations(country_df):
    """Compute Pearson and Spearman correlations."""
    # select columns
    # compute correlations
    # return results df

def run_regression(country_df, y_col, x_cols):
    """Run linear regression with controls."""
    # build design matrix
    # fit OLS
    # return model + tidy results

def model_diagnostics(model):
    """Extract R^2, coefficients, residual stats."""
    # return dict or df