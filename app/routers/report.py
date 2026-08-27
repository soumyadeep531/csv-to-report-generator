from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from app.core.config import settings
from app.services.data_loader import load_csv
from app.services.report_service import run_pipeline
from fastapi import Depends
from app.core.security import verify_api_key
from fastapi import Request
from app.core.limiter import limiter


router = APIRouter(prefix="/api", tags=["Reports & EDA"])


@router.post("/generate-report",dependencies=[Depends(verify_api_key)])
@limiter.limit("5/minute")
def generate_report(
    request : Request,
    file: UploadFile = File(...),
    target_column: Optional[str] = Form(None),
    id_columns: Optional[str] = Form(None),
    drop_columns: Optional[str] = Form(None),
):
    """
    Upload a CSV file and generate a full EDA & ML PDF Report.
    """
    df = load_csv(file)

    parsed_id_cols = [c.strip() for c in id_columns.split(",")] if id_columns else settings.ID_COLUMNS
    parsed_drop_cols = [c.strip() for c in drop_columns.split(",")] if drop_columns else settings.DROP_COLUMNS

    try:
        result = run_pipeline(
            df=df,
            target_column=target_column,
            id_columns=parsed_id_cols,
            drop_columns=parsed_drop_cols,
        )
        return JSONResponse(content=result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/sample-report",
            dependencies=[Depends(verify_api_key)])
def generate_sample_report():
    """
    Generate report using the bundled Cancer_Data.csv.
    """
    sample_csv = Path(__file__).resolve().parent.parent.parent / "Cancer_Data.csv"
    if not sample_csv.exists():
        raise HTTPException(status_code=404, detail="Cancer_Data.csv not found")

    df = pd.read_csv(sample_csv)
    result = run_pipeline(
        df=df,
        target_column=settings.TARGET_COLUMN,
        id_columns=settings.ID_COLUMNS,
        drop_columns=settings.DROP_COLUMNS,
    )
    return JSONResponse(content=result)


@router.get("/reports/{filename}",dependencies=[Depends(verify_api_key)])
def download_report(filename: str):
    """
    Download a generated PDF report.
    """
    file_path = settings.STORAGE_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")

    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/pdf",
    )


