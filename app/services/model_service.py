import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve,
)


def prepare_classification_data(
    df: pd.DataFrame,
    target_column: str,
    id_columns: list,
    drop_columns: list,
    test_size: float = 0.20,
    random_state: int = 42,
):
    """
    Prepare data for classification.

    Removes ID/unwanted columns, handles missing values,
    encodes the target, and creates train/test sets.
    """

    data = df.copy()

    # Remove unwanted columns
    columns_to_remove = [
        col
        for col in id_columns + drop_columns
        if col in data.columns
    ]

    data = data.drop(
        columns=columns_to_remove,
        errors="ignore"
    )

    # Make sure target exists
    if target_column not in data.columns:
        raise ValueError(
            f"Target column '{target_column}' not found"
        )

    # Separate features and target
    X = data.drop(
        columns=[target_column]
    )

    y = data[target_column]

    # Keep only numeric features
    X = X.select_dtypes(
        include=["number"]
    )

    # Handle missing values
    X = X.fillna(
        X.median(numeric_only=True)
    )

    # Encode target
    label_encoder = LabelEncoder()

    y_encoded = label_encoder.fit_transform(y)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=test_size,
        random_state=random_state,
        stratify=y_encoded,
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        label_encoder,
        X.columns.tolist(),
    )


def train_random_forest(
    X_train,
    y_train,
    random_state: int = 42,
):
    """
    Train a baseline Random Forest classifier.
    """

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=random_state,
        class_weight="balanced",
        n_jobs=1,
    )

    model.fit(
        X_train,
        y_train
    )

    return model


def evaluate_classification_model(
    model,
    X_test,
    y_test,
):
    """
    Calculate classification metrics.
    """

    y_pred = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(
            y_test,
            y_pred
        ),
        "precision": precision_score(
            y_test,
            y_pred,
            zero_division=0
        ),
        "recall": recall_score(
            y_test,
            y_pred,
            zero_division=0
        ),
        "f1": f1_score(
            y_test,
            y_pred,
            zero_division=0
        ),
    }

    return {
        "metrics": metrics,
        "predictions": y_pred,
        "classification_report": classification_report(
            y_test,
            y_pred,
            zero_division=0
        ),
        "confusion_matrix": confusion_matrix(
            y_test,
            y_pred
        ),
    }


def calculate_roc_auc(
    model,
    X_test,
    y_test,
):
    """
    Calculate ROC curve and AUC.
    """

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    auc_score = roc_auc_score(
        y_test,
        probabilities
    )

    fpr, tpr, thresholds = roc_curve(
        y_test,
        probabilities
    )

    return {
        "auc": auc_score,
        "fpr": fpr,
        "tpr": tpr,
        "thresholds": thresholds,
        "probabilities": probabilities,
    }


def get_feature_importance(
    model,
    feature_names: list,
) -> pd.DataFrame:
    """
    Return Random Forest feature importance.
    """

    importance = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_,
    })

    return importance.sort_values(
        "importance",
        ascending=False
    ).reset_index(drop=True)


def train_baseline_model(
    df: pd.DataFrame,
    target_column: str,
    id_columns: list,
    drop_columns: list,
    test_size: float = 0.20,
    random_state: int = 42,
):
    """
    Complete baseline Random Forest pipeline.
    """

    (
        X_train,
        X_test,
        y_train,
        y_test,
        label_encoder,
        feature_names,
    ) = prepare_classification_data(
        df=df,
        target_column=target_column,
        id_columns=id_columns,
        drop_columns=drop_columns,
        test_size=test_size,
        random_state=random_state,
    )

    model = train_random_forest(
        X_train,
        y_train,
        random_state=random_state,
    )

    evaluation = evaluate_classification_model(
        model,
        X_test,
        y_test,
    )

    roc_data = calculate_roc_auc(
        model,
        X_test,
        y_test,
    )

    feature_importance = get_feature_importance(
        model,
        feature_names,
    )

    return {
        "model": model,
        "label_encoder": label_encoder,
        "feature_names": feature_names,
        "evaluation": evaluation,
        "roc": roc_data,
        "feature_importance": feature_importance,
    }