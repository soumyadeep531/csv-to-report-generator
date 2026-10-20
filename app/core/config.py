import os
import tempfile
from pathlib import Path

# Ensure Matplotlib uses a writable directory in serverless environments (prevents read-only FS errors)
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "matplotlib"))

# Load .env file into environment
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if _env_path.exists():
    with open(_env_path, "r", encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip().strip("'\""))


def _resolve_storage_dir() -> Path:
    # On Vercel, AWS Lambda, or other serverless platforms, always use writable /tmp
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        storage = Path(tempfile.gettempdir()) / "storage"
    else:
        storage = Path(__file__).resolve().parent.parent / "storage"

    try:
        storage.mkdir(parents=True, exist_ok=True)
        return storage
    except (OSError, PermissionError):
        # Fallback to system temp directory if local path is on a read-only filesystem
        storage = Path(tempfile.gettempdir()) / "storage"
        storage.mkdir(parents=True, exist_ok=True)
        return storage


class Settings:
    APP_NAME: str = "autoeda-backend"
    APP_VERSION: str = "1.0.0"

    STORAGE_DIR: Path = _resolve_storage_dir()

    # Cancer_Data.csv settings
    TARGET_COLUMN: str = "diagnosis"
    ID_COLUMNS: list[str] = ["id"]
    DROP_COLUMNS: list[str] = ["Unnamed: 32"]

    # EDA settings
    MAX_ROWS_FOR_KDE: int = 5000
    KDE_PLOTS_PER_PAGE: int = 6
    STATS_COLUMNS_PER_PAGE: int = 5

    # Machine learning settings
    RANDOM_STATE: int = 42
    TEST_SIZE: float = 0.20


settings = Settings()