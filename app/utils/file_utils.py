import uuid
from pathlib import Path


def generate_report_path(storage_dir: Path) -> Path:
    """
    Generate a unique path for the PDF report.
    """
    #uuid.uuid4().hex can produce like a81f92c3d4e54b8f9c...
    filename = f"eda_report_{uuid.uuid4().hex}.pdf"

    return storage_dir / filename