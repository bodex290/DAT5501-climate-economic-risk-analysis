from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    data_raw: Path
    data_processed: Path
    outputs: Path
    figures: Path
    tables: Path


def get_project_paths(root: Optional[str | Path] = None) -> ProjectPaths:
    """
    Resolve and return key project directories.
    Defaults to repo root (assumes this file lives in src/).
    """
    if root is None:
        # src/utils.py -> src -> project root
        root_path = Path(__file__).resolve().parents[1]
    else:
        root_path = Path(root).resolve()

    data_raw = root_path / "data" / "raw"
    data_processed = root_path / "data" / "processed"
    outputs = root_path / "outputs"
    figures = outputs / "figures"
    tables = outputs / "tables"

    # Ensure folders exist (safe: mkdir with parents=True)
    for p in [data_raw, data_processed, figures, tables]:
        p.mkdir(parents=True, exist_ok=True)

    return ProjectPaths(
        root=root_path,
        data_raw=data_raw,
        data_processed=data_processed,
        outputs=outputs,
        figures=figures,
        tables=tables,
    )


def validate_required_columns(df: pd.DataFrame, required: Iterable[str], df_name: str = "DataFrame") -> None:
    """
    Raise ValueError if required columns are missing.
    """
    required = set(required)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{df_name} is missing required columns: {sorted(missing)}")


def safe_to_csv(df: pd.DataFrame, path: str | Path, index: bool = False) -> Path:
    """
    Save DataFrame to CSV, ensuring parent directory exists.
    Returns the resolved path.
    """
    path = Path(path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index)
    return path


def safe_read_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """
    Read CSV with slightly safer defaults.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    return pd.read_csv(path, **kwargs)


def describe_missingness(df: pd.DataFrame) -> pd.DataFrame:
    """
    Quick missingness summary: count + percent per column.
    Useful for exploration and data quality notes.
    """
    missing_count = df.isna().sum()
    missing_pct = (missing_count / len(df) * 100).round(2)
    out = pd.DataFrame({"missing_count": missing_count, "missing_pct": missing_pct})
    return out.sort_values("missing_pct", ascending=False)


def log_basic_info(df: pd.DataFrame, name: str = "df") -> None:
    """
    Print basic info in a consistent format (lightweight logging).
    """
    print(f"\n[{name}] shape={df.shape}")
    print(f"[{name}] columns={list(df.columns)}")
    print(f"[{name}] head:\n{df.head(3)}")