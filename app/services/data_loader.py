import pandas as pd
from fastapi import UploadFile, HTTPException


def load_csv(file: UploadFile) -> pd.DataFrame:
    """
    Read an uploaded CSV file into a pandas DataFrame.
    """

    # Check file extension
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only .csv files are supported"
        )

    try:
        # Read CSV into DataFrame
        df = pd.read_csv(file.file)

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Could not parse CSV: {exc}"
        )

    # Make sure CSV is not empty
    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="Uploaded CSV is empty"
        )

    return df


def infer_column_types(df: pd.DataFrame) -> dict:
    """
    Split columns into numeric, categorical, and ID-like columns.
    """

    numeric_cols = []
    categorical_cols = []
    id_like_cols = []

    n_rows = len(df)

    for col in df.columns:

        # ID-like column:
        # every non-null value is unique
        if (
            df[col].nunique(dropna=True) == n_rows
            and df[col].dtype != "float64"
        ):
            id_like_cols.append(col)

        # Numeric column
        elif pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)

        # Everything else is categorical
        else:
            categorical_cols.append(col)

    return {
        "numeric": numeric_cols,
        "categorical": categorical_cols,
        "id_like": id_like_cols,
    }


def detect_task_type(
    df: pd.DataFrame,
    target_column: str
) -> str:
    """
    Automatically detect classification or regression.
    """
    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' not found"
        )
        
    series = df[target_column]

    # Object/string target or small number of unique values
    # usually means classification.
    if series.dtype == "object" or series.nunique() <= 10:
        return "classification"

    return "regression"