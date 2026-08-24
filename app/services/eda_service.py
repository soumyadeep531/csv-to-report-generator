import pandas as pd


def get_dataset_overview(
    df: pd.DataFrame,
    target_column: str,
    task_type: str,
    id_like_cols: list
) -> dict:
    """
    Return basic information about the dataset.
    """

    return {
        "rows": len(df),
        "columns": df.shape[1],
        "task_type": task_type,
        "target_column": target_column,
        "overall_missing_pct": round(
            df.isna().mean().mean() * 100,
            2
        ),
        "id_like_columns_removed": len(id_like_cols),
    }


def get_missing_values_summary(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate missing value count and percentage
    for every column.
    """

    missing = df.isna().sum()

    percentage = (
        missing / len(df) * 100
    ).round(2)

    result = pd.DataFrame({
        "missing_count": missing,
        "missing_percent": percentage
    })

    return result.sort_values(
        "missing_count",
        ascending=False
    )


def get_numeric_summary(
    df: pd.DataFrame,
    numeric_cols: list
) -> pd.DataFrame:
    """
    Generate descriptive statistics for numeric columns.
    """

    stats = df[numeric_cols].describe().T

    stats["missing"] = (
        df[numeric_cols]
        .isna()
        .sum()
    )

    return stats


def get_categorical_summary(
    df: pd.DataFrame,
    categorical_cols: list
) -> pd.DataFrame:
    """
    Generate descriptive statistics for categorical columns.
    """

    if not categorical_cols:
        return pd.DataFrame()

    return df[categorical_cols].describe().T


def get_correlation_matrix(
    df: pd.DataFrame,
    numeric_cols: list
) -> pd.DataFrame:
    """
    Calculate correlation between numeric columns.
    """

    return df[numeric_cols].corr()


def get_outlier_proportions(
    df: pd.DataFrame,
    numeric_cols: list
) -> pd.DataFrame:
    """
    Calculate outlier percentages using:
    1. 3-sigma rule
    2. 1.5 x IQR rule
    """

    rows = []

    for col in numeric_cols:

        series = df[col].dropna()

        # -----------------------------
        # 3-sigma method
        # -----------------------------

        mean = series.mean()
        std = series.std()

        sigma_outliers = (
            (series - mean).abs() > 3 * std
        ).mean() * 100

        # -----------------------------
        # IQR method
        # -----------------------------

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        iqr_outliers = (
            (series < lower) |
            (series > upper)
        ).mean() * 100

        rows.append({
            "column": col,
            "sigma_pct": sigma_outliers,
            "iqr_pct": iqr_outliers
        })

    return pd.DataFrame(rows).sort_values(
        "iqr_pct"
    )


def get_duplicate_distribution(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Count duplicated values in every column.
    """

    rows = []

    for col in df.columns:

        duplicate_count = (
            df[col]
            .duplicated(keep=False)
            .sum()
        )

        rows.append({
            "column": col,
            "duplicate_count": duplicate_count
        })

    return pd.DataFrame(rows).sort_values(
        "duplicate_count",
        ascending=False
    )