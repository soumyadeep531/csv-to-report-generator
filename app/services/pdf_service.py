from datetime import datetime
from pathlib import Path
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
    KeepTogether,
)


def dataframe_to_table(
    df: pd.DataFrame,
    max_rows: int = 15,
    header_color: str = "#334155",
    alt_color: str = "#f8fafc",
    grid_color: str = "#cbd5e1",
    header_text_color: str = "#ffffff",
):
    """
    Convert a DataFrame into a vibrant, styled ReportLab table.
    """
    if df.empty:
        return Table([["No data available"]])

    display_df = df.head(max_rows).copy()
    display_df = display_df.round(4).astype(str)

    data = [list(display_df.columns)] + display_df.values.tolist()

    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_color)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor(header_text_color)),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(grid_color)),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("FONTSIZE", (0, 1), (-1, -1), 7.5),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor(alt_color)]),
        ])
    )
    return table


def figure_to_image(
    fig,
    output_dir: Path,
    filename: str
):
    """
    Save a Matplotlib Figure as a temporary PNG and return its path.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    image_path = output_dir / filename
    fig.savefig(image_path, dpi=150, bbox_inches="tight")
    return image_path


def build_pdf_report(
    output_path: Path,
    overview: dict,
    missing_summary: pd.DataFrame,
    numeric_summary: pd.DataFrame,
    categorical_summary: pd.DataFrame,
    outlier_summary: pd.DataFrame,
    duplicate_summary: pd.DataFrame,
    model_result: dict,
    figures: list,
    llm_summary: str = "",
    feature_importance_fig=None,
):
    """
    Build the complete AutoEDA PDF report with Colorful Tables, Exact Timestamps, PCA, and Full-Page LLM Summary.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = output_path.parent / "_report_images"
    temp_dir.mkdir(parents=True, exist_ok=True)

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=32,
        leftMargin=32,
        topMargin=32,
        bottomMargin=32,
    )

    styles = getSampleStyleSheet()

    # Exact Generation Timestamp
    now = datetime.now()
    timestamp_str = now.strftime("%A, %B %d, %Y • %I:%M:%S %p")

    # Custom Typography & Styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1e1b4b"),
        fontName="Helvetica-Bold",
        alignment=0,
    )

    meta_style = ParagraphStyle(
        "MetaBadge",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#4338ca"),
        fontName="Helvetica-Bold",
    )

    sub_style = ParagraphStyle(
        "CustomSub",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748b"),
    )

    heading_style = ParagraphStyle(
        "CustomHeading2",
        parent=styles["Heading2"],
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#0f172a"),
        fontName="Helvetica-Bold",
        spaceBefore=10,
        spaceAfter=6,
    )

    normal_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
    )

    # Full-page Executive Summary typography
    summary_box_style = ParagraphStyle(
        "FullPageSummaryBox",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=16,
        textColor=colors.HexColor("#0f172a"),
    )

    summary_header_style = ParagraphStyle(
        "SummaryHeader",
        parent=styles["Normal"],
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#312e81"),
        fontName="Helvetica-Bold",
    )

    story = []

    # -------------------------------------------------
    # Title Header with Exact Date & Time
    # -------------------------------------------------
    story.append(Paragraph("AutoEDA & Predictive Intelligence Report", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Automated Exploratory Data Analysis, Machine Learning Baseline & Strategic AI Insights", sub_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"📅 Generated on: <b>{timestamp_str}</b>", meta_style))
    story.append(Spacer(1, 14))

    # -------------------------------------------------
    # 1. Dataset Overview (Indigo & Slate Theme)
    # -------------------------------------------------
    story.append(Paragraph("1. Dataset Overview", heading_style))
    overview_data = [
        ["Property", "Value"],
        ["Rows", f"{overview.get('rows', ''):,}" if isinstance(overview.get('rows'), int) else str(overview.get('rows', ''))],
        ["Columns", str(overview.get("columns", ""))],
        ["Task Type", str(overview.get("task_type", "")).capitalize()],
        ["Target Column", str(overview.get("target_column", ""))],
        ["Overall Missing %", f"{overview.get('overall_missing_pct', '')}%"],
        ["ID-like Columns Removed", str(overview.get("id_like_columns_removed", ""))],
        ["Report Timestamp", timestamp_str],
    ]

    overview_table = Table(overview_data, repeatRows=1, colWidths=[180, 350])
    overview_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4338ca")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#c7d2fe")),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef2ff")]),
        ])
    )
    story.append(overview_table)
    story.append(Spacer(1, 14))

    # -------------------------------------------------
    # 2. Missing Values (Sky / Ocean Blue Theme)
    # -------------------------------------------------
    story.append(Paragraph("2. Missing Values Summary", heading_style))
    story.append(Paragraph("Missing-value counts and percentages per attribute:", normal_style))
    story.append(Spacer(1, 6))
    story.append(dataframe_to_table(
        missing_summary.reset_index(),
        max_rows=16,
        header_color="#0284c7",
        alt_color="#f0f9ff",
        grid_color="#bae6fd"
    ))
    story.append(PageBreak())

    # -------------------------------------------------
    # 3. Numeric Summary (Teal / Emerald Theme)
    # -------------------------------------------------
    story.append(Paragraph("3. Numeric Summary Statistics", heading_style))
    story.append(dataframe_to_table(
        numeric_summary.reset_index(),
        max_rows=16,
        header_color="#0f766e",
        alt_color="#f0fdfa",
        grid_color="#99f6e4"
    ))
    story.append(Spacer(1, 14))

    # -------------------------------------------------
    # 4. Categorical Summary (Violet Theme)
    # -------------------------------------------------
    story.append(Paragraph("4. Categorical Summary", heading_style))
    if categorical_summary.empty:
        story.append(Paragraph("No categorical columns detected in this dataset.", normal_style))
    else:
        story.append(dataframe_to_table(
            categorical_summary.reset_index(),
            header_color="#7c3aed",
            alt_color="#faf5ff",
            grid_color="#ddd6fe"
        ))
    story.append(PageBreak())

    # -------------------------------------------------
    # 5. Outliers & Duplicates (Crimson & Purple Theme)
    # -------------------------------------------------
    story.append(Paragraph("5. Outlier Analysis (3-Sigma vs IQR)", heading_style))
    if not outlier_summary.empty:
        story.append(dataframe_to_table(
            outlier_summary,
            max_rows=12,
            header_color="#e11d48",
            alt_color="#fff1f2",
            grid_color="#fecdd3"
        ))
    else:
        story.append(Paragraph("No numeric features available for outlier calculation.", normal_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("6. Duplicate Value Distribution", heading_style))
    if not duplicate_summary.empty:
        story.append(dataframe_to_table(
            duplicate_summary,
            max_rows=12,
            header_color="#9333ea",
            alt_color="#faf5ff",
            grid_color="#e9d5ff"
        ))
    else:
        story.append(Paragraph("No duplicate records found.", normal_style))
    story.append(PageBreak())

    # -------------------------------------------------
    # 7. Machine Learning Baseline (Royal Blue Theme)
    # -------------------------------------------------
    story.append(Paragraph("7. Baseline Random Forest Classifier", heading_style))
    if model_result and "evaluation" in model_result:
        metrics = model_result["evaluation"]["metrics"]
        metric_data = [
            ["Evaluation Metric", "Score / Value"],
            ["Model Accuracy", f"{metrics['accuracy'] * 100:.2f}%"],
            ["Precision (Weighted)", f"{metrics['precision'] * 100:.2f}%"],
            ["Recall (Sensitivity)", f"{metrics['recall'] * 100:.2f}%"],
            ["Harmonic F1-Score", f"{metrics['f1'] * 100:.2f}%"],
            ["ROC Area Under Curve (AUC)", f"{model_result['roc']['auc']:.4f}" if 'roc' in model_result else "N/A"],
        ]
        metric_table = Table(metric_data, repeatRows=1, colWidths=[200, 330])
        metric_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bfdbfe")),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eff6ff")]),
            ])
        )
        story.append(metric_table)
        story.append(Spacer(1, 12))

        story.append(Paragraph("Classification Report Detail", heading_style))
        report_text = (
            model_result["evaluation"]["classification_report"]
            .replace("\n", "<br/>")
            .replace(" ", "&nbsp;")
        )
        story.append(Paragraph(f"<font face='Courier' size=7 color='#1e293b'>{report_text}</font>", normal_style))
    else:
        story.append(Paragraph("Model baseline was not run or task is regression.", normal_style))
    story.append(PageBreak())

    # -------------------------------------------------
    # 8. Feature Importance (VISUAL PICTURE)
    # -------------------------------------------------
    story.append(Paragraph("8. Feature Importance (Visual Analysis)", heading_style))
    story.append(Spacer(1, 6))
    if feature_importance_fig is not None:
        feat_img_path = figure_to_image(feature_importance_fig, temp_dir, "feature_importance.png")
        story.append(Image(str(feat_img_path), width=6.8 * inch, height=4.6 * inch))
    elif model_result and "feature_importance" in model_result:
        story.append(dataframe_to_table(
            model_result["feature_importance"].head(15),
            header_color="#059669",
            alt_color="#ecfdf5",
            grid_color="#a7f3d0"
        ))
    else:
        story.append(Paragraph("No feature importance data available.", normal_style))
    
    story.append(PageBreak())

    # -------------------------------------------------
    # 9. Key Exploratory Visualizations
    # -------------------------------------------------
    story.append(Paragraph("9. Key Exploratory Visualizations", heading_style))
    for index, fig in enumerate(figures):
        image_path = figure_to_image(fig, temp_dir, f"figure_{index}.png")
        story.append(Image(str(image_path), width=6.8 * inch, height=5.2 * inch))
        story.append(Spacer(1, 10))
        story.append(PageBreak())

    # -------------------------------------------------
    # 10. AI Executive Summary (FULL DEDICATED PAGE)
    # -------------------------------------------------
    if llm_summary:
        story.append(Paragraph("10. AI-Generated Executive Summary & Strategic Insights", summary_header_style))
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"Autonomous Analysis Synthesized on <b>{timestamp_str}</b>", meta_style))
        story.append(Spacer(1, 12))

        summary_table_data = [[
            Paragraph(llm_summary, summary_box_style)
        ]]
        summary_table = Table(summary_table_data, colWidths=[530])
        summary_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ("BOX", (0, 0), (-1, -1), 2.0, colors.HexColor("#4f46e5")),
                ("TOPPADDING", (0, 0), (-1, -1), 18),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
                ("LEFTPADDING", (0, 0), (-1, -1), 20),
                ("RIGHTPADDING", (0, 0), (-1, -1), 20),
            ])
        )
        story.append(summary_table)

    # Build PDF
    document.build(story)
    return output_path