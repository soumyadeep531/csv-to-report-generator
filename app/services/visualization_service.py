import math
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def create_correlation_heatmap(
    corr: pd.DataFrame,
    title: str = "Correlation Heatmap"
):
    """
    Create a high-resolution correlation heatmap with increased height and clear formatting.
    """
    n_cols = len(corr)
    # Scale height comfortably so labels and squares are clear and not squished
    fig_height = max(8.5, min(14.0, n_cols * 0.45))
    fig_width = max(9.0, min(12.0, n_cols * 0.45))
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    sns.heatmap(
        corr,
        cmap="coolwarm",
        center=0,
        ax=ax,
        annot=n_cols <= 16,
        fmt=".2f" if n_cols <= 16 else "",
        annot_kws={"size": 7.5},
        cbar_kws={"shrink": 0.75, "aspect": 20},
        square=True,
        linewidths=0.5,
        linecolor="#f1f5f9"
    )
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    ax.tick_params(axis="y", rotation=0, labelsize=8)
    fig.tight_layout()
    return fig


def create_feature_importance_plot(
    importance_df: pd.DataFrame,
    top_n: int = 15
):
    """
    Convert feature importance table into a visual horizontal bar chart.
    """
    top_df = importance_df.head(top_n).sort_values("importance", ascending=True)

    fig, ax = plt.subplots(figsize=(9, 5.2))
    colors = plt.cm.viridis(np.linspace(0.3, 0.85, len(top_df)))

    bars = ax.barh(
        top_df["feature"],
        top_df["importance"],
        color=colors,
        edgecolor="#1e293b",
        height=0.65
    )

    # Numerical annotations on each bar
    max_val = max(top_df["importance"]) if not top_df.empty else 1.0
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + (max_val * 0.01),
            bar.get_y() + bar.get_height() / 2,
            f"{width:.4f}",
            va="center",
            ha="left",
            fontsize=8,
            fontweight="bold",
            color="#334155"
        )

    ax.set_xlabel("Relative Importance Score", fontsize=10, fontweight="bold")
    ax.set_title(f"Top {len(top_df)} Most Predictive Features (Random Forest)", fontsize=12, fontweight="bold", pad=10)
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.set_xlim(0, max_val * 1.15)
    fig.tight_layout()
    return fig


def create_pca_cluster_plot(
    df: pd.DataFrame,
    numeric_cols: list,
    target_column: Optional[str] = None,
    n_clusters: int = 3
):
    """
    Perform PCA dimensionality reduction (2 components) and create a 2D cluster scatter plot.
    """
    if len(numeric_cols) < 2:
        return None

    features = [c for c in numeric_cols if c != target_column]
    data_clean = df[features].dropna()

    if len(data_clean) < 5:
        return None

    # Standardize data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data_clean)

    # 2D PCA
    pca = PCA(n_components=2, random_state=42)
    pca_coords = pca.fit_transform(scaled_data)
    var_exp = pca.explained_variance_ratio_ * 100

    pca_df = pd.DataFrame(pca_coords, columns=["PC1", "PC2"], index=data_clean.index)

    fig, ax = plt.subplots(figsize=(9, 5.2))

    # Color by target if available, otherwise KMeans clusters
    if target_column and target_column in df.columns:
        target_series = df.loc[data_clean.index, target_column]
        sns.scatterplot(
            data=pca_df,
            x="PC1",
            y="PC2",
            hue=target_series,
            palette="Set2",
            alpha=0.85,
            s=55,
            edgecolor="w",
            ax=ax
        )
        ax.set_title(f"PCA 2D Projection (Color-Coded by '{target_column}')", fontsize=12, fontweight="bold")
    else:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(scaled_data)
        scatter = ax.scatter(
            pca_df["PC1"],
            pca_df["PC2"],
            c=clusters,
            cmap="tab10",
            alpha=0.85,
            s=55,
            edgecolors="w"
        )
        ax.set_title(f"PCA 2D Cluster Analysis (K-Means k={n_clusters})", fontsize=12, fontweight="bold")

    ax.set_xlabel(f"Principal Component 1 ({var_exp[0]:.1f}% Explained Variance)", fontsize=10, fontweight="bold")
    ax.set_ylabel(f"Principal Component 2 ({var_exp[1]:.1f}% Explained Variance)", fontsize=10, fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    return fig


def create_target_distribution(
    df: pd.DataFrame,
    target_column: str,
    task_type: str
):
    """
    Create a distribution plot for the target column.
    """
    fig, ax = plt.subplots(figsize=(8, 4.5))

    if task_type == "classification":
        counts = df[target_column].value_counts()
        counts.plot(kind="bar", ax=ax, color="#6366f1", edgecolor="black")
        ax.set_xlabel(target_column, fontsize=10, fontweight="bold")
        ax.set_ylabel("Count", fontsize=10, fontweight="bold")
    else:
        df[target_column].plot(kind="hist", bins=30, ax=ax, color="#6366f1", edgecolor="black")
        ax.set_xlabel(target_column, fontsize=10, fontweight="bold")
        ax.set_ylabel("Frequency", fontsize=10, fontweight="bold")

    ax.set_title(f"Target Distribution: {target_column}", fontsize=12, fontweight="bold")
    fig.tight_layout()
    return fig


def create_kde_pages(
    df: pd.DataFrame,
    numeric_cols: list,
    max_rows: int = 5000,
    per_page: int = 6
):
    """
    Create pages containing KDE plots.
    """
    if not numeric_cols:
        return []

    sample = df[numeric_cols].dropna()
    if len(sample) > max_rows:
        sample = sample.sample(max_rows, random_state=42)

    figures = []
    for start in range(0, len(numeric_cols), per_page):
        cols = numeric_cols[start:start + per_page]
        rows = math.ceil(len(cols) / 2)

        fig, axes = plt.subplots(rows, 2, figsize=(9.5, 3.2 * rows))
        axes = np.atleast_1d(axes).flatten()

        for ax, col in zip(axes, cols):
            sns.kdeplot(data=sample, x=col, fill=True, ax=ax, color="#06b6d4")
            ax.set_title(f"KDE: {col}", fontsize=9.5)

        for ax in axes[len(cols):]:
            ax.set_visible(False)

        fig.tight_layout()
        figures.append(fig)

    return figures


def create_outlier_chart(
    outlier_df: pd.DataFrame
):
    """
    Create a chart comparing outlier percentages.
    """
    fig, ax = plt.subplots(figsize=(9.5, 4.8))

    x = np.arange(len(outlier_df))
    width = 0.35

    ax.bar(x - width / 2, outlier_df["sigma_pct"], width, label="3-Sigma", color="#f43f5e")
    ax.bar(x + width / 2, outlier_df["iqr_pct"], width, label="IQR", color="#f59e0b")

    ax.set_xticks(x)
    ax.set_xticklabels(outlier_df["column"], rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Outlier Percentage (%)", fontsize=9.5, fontweight="bold")
    ax.set_title("Outlier Proportions by Method (3-Sigma vs IQR)", fontsize=12, fontweight="bold")
    ax.legend()
    fig.tight_layout()
    return fig


def create_duplicate_chart(
    duplicate_df: pd.DataFrame
):
    """
    Create a chart showing duplicate values for each column.
    """
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    ax.bar(duplicate_df["column"], duplicate_df["duplicate_count"], color="#8b5cf6")
    ax.set_title("Duplicate Value Distribution", fontsize=12, fontweight="bold")
    ax.set_xlabel("Column", fontsize=9.5, fontweight="bold")
    ax.set_ylabel("Duplicate Count", fontsize=9.5, fontweight="bold")
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    fig.tight_layout()
    return fig