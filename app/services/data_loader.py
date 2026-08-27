import pandas as pd
from fastapi import UploadFile, HTTPException
from app.core.config import settings

MAX_FILE_SIZE_MB = 10


def load_csv(file: UploadFile) -> pd.DataFrame:

    # Check file extension
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only .csv files are supported"
        )

    # 2. check content type
    if file.content_type not in(
        "text/csv",
        "application/vnd.ms-excel",
        "application/csv",
        "text/plain",
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid content type for csv upload"
        )
        
        
    file.file.seek(0,2)
    size_mb=file.file.tell()/ (1024 * 1024)
    file.file.seek(0)
    
    if size_mb>MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds {MAX_FILE_SIZE_MB} MB Limit"
        )
        
    df = pd.read_csv(file.file)
        
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