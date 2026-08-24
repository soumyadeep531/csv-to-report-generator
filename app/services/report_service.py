import math
from pathlib import Path
from typing import Optional

import pandas as pd

from app.core.config import settings
from app.services.data_loader import detect_task_type, infer_column_types
from app.services.eda_service import (
    get_categorical_summary,
    get_correlation_matrix,
    get_dataset_overview,
    get_duplicate_distribution,
    get_missing_values_summary,
    get_numeric_summary,
    get_outlier_proportions,
)
from app.services.model_service import train_baseline_model
from app.services.pdf_service import build_pdf_report
from app.services.llm_service import generate_llm_summary
from app.services.visualization_service import (
    create_correlation_heatmap,
    create_duplicate_chart,
    create_feature_importance_plot,
    create_kde_pages,
    create_outlier_chart,
    create_pca_cluster_plot,
    create_target_distribution,
)
from app.utils.file_utils import generate_report_path


def run_pipeline(
    df: pd.DataFrame,
    target_column: Optional[str] = None,
    id_columns: Optional[list[str]] = None,
    drop_columns: Optional[list[str]] = None,
) -> dict:
    """
    Execute full EDA, PCA 2D Clustering, Visualizations, ML baseline, LLM summary, and PDF report.
    """
    if id_columns is None:
        id_columns = settings.ID_COLUMNS
    if drop_columns is None:
        drop_columns = settings.DROP_COLUMNS

    column_types = infer_column_types(df)
    numeric_cols = column_types["numeric"]
    categorical_cols = column_types["categorical"]
    id_like_cols = column_types["id_like"]

    # Target column resolution
    if not target_column:
        if settings.TARGET_COLUMN in df.columns:
            target_column = settings.TARGET_COLUMN
        elif categorical_cols:
            target_column = categorical_cols[0]
        else:
            target_column = df.columns[-1]

    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset")

    task_type = detect_task_type(df, target_column)

    # Filter numeric features (excluding target if numeric, id columns, and drop columns)
    feature_numeric_cols = [
        c for c in numeric_cols
        if c != target_column and c not in id_columns and c not in drop_columns
    ]

    # Compute EDA summaries
    overview = get_dataset_overview(df, target_column, task_type, id_like_cols)
    missing_summary = get_missing_values_summary(df)
    numeric_summary = get_numeric_summary(df, numeric_cols)
    categorical_summary = get_categorical_summary(df, categorical_cols)
    outlier_summary = get_outlier_proportions(df, feature_numeric_cols) if feature_numeric_cols else pd.DataFrame()
    duplicate_summary = get_duplicate_distribution(df)

    # Visualizations list
    figures = []

    # 1. Target Distribution
    try:
        if target_column in df.columns:
            figures.append(create_target_distribution(df, target_column, task_type))
    except Exception:
        pass

    # 2. PCA 2D Cluster Analysis (NEW)
    try:
        if len(feature_numeric_cols) >= 2:
            pca_fig = create_pca_cluster_plot(
                df=df,
                numeric_cols=feature_numeric_cols,
                target_column=target_column if task_type == "classification" else None
            )
            if pca_fig is not None:
                figures.append(pca_fig)
    except Exception:
        pass

    # 3. Correlation Heatmap (Increased Height & Annotated)
    try:
        if len(feature_numeric_cols) >= 2:
            corr = get_correlation_matrix(df, feature_numeric_cols[:20])
            figures.append(create_correlation_heatmap(corr))
    except Exception:
        pass

    # 4. Outlier Proportions (3-Sigma vs IQR)
    try:
        if not outlier_summary.empty:
            figures.append(create_outlier_chart(outlier_summary.head(15)))
    except Exception:
        pass

    # 5. Duplicate Value Distribution
    try:
        if not duplicate_summary.empty:
            figures.append(create_duplicate_chart(duplicate_summary.head(15)))
    except Exception:
        pass

    # 6. KDE Distribution Plots
    try:
        if feature_numeric_cols:
            kde_figs = create_kde_pages(df, feature_numeric_cols[:6], max_rows=settings.MAX_ROWS_FOR_KDE)
            figures.extend(kde_figs)
    except Exception:
        pass

    # Baseline Model Training (Classification)
    model_result = {}
    feature_importance_fig = None
    if task_type == "classification":
        try:
            model_result = train_baseline_model(
                df=df,
                target_column=target_column,
                id_columns=id_columns,
                drop_columns=drop_columns,
                test_size=settings.TEST_SIZE,
                random_state=settings.RANDOM_STATE,
            )
            if "feature_importance" in model_result and not model_result["feature_importance"].empty:
                feature_importance_fig = create_feature_importance_plot(
                    model_result["feature_importance"],
                    top_n=15
                )
        except Exception as e:
            model_result = {"error": str(e)}

    # Extract metrics for LLM summary
    metrics = {}
    if model_result and "evaluation" in model_result:
        metrics = model_result["evaluation"].get("metrics", {})

    # Generate LLM Executive Summary (NEW)
    llm_summary = generate_llm_summary(
        overview=overview,
        metrics=metrics,
        feature_importance_df=model_result.get("feature_importance") if isinstance(model_result, dict) else None,
        missing_df=missing_summary,
    )

    # Generate PDF report
    report_path = generate_report_path(settings.STORAGE_DIR)
    build_pdf_report(
        output_path=report_path,
        overview=overview,
        missing_summary=missing_summary,
        numeric_summary=numeric_summary,
        categorical_summary=categorical_summary,
        outlier_summary=outlier_summary,
        duplicate_summary=duplicate_summary,
        model_result=model_result,
        figures=figures,
        llm_summary=llm_summary,
        feature_importance_fig=feature_importance_fig,
    )

    return {
        "success": True,
        "filename": report_path.name,
        "report_url": f"/api/reports/{report_path.name}",
        "overview": overview,
        "metrics": metrics,
    }
