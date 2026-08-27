import os
from pathlib import Path

# Load .env file into environment
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if _env_path.exists():
    with open(_env_path, "r", encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip().strip("'\""))


class Settings:
    APP_NAME: str = "autoeda-backend"
    APP_VERSION: str = "1.0.0"

    STORAGE_DIR: Path = (
        Path(__file__).resolve().parent.parent / "storage"
    )
    MAX_FILE_SIZE_MB: int = 10
    API_KEY: str

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

settings.STORAGE_DIR.mkdir(
    parents=True,
    exist_ok=True
)