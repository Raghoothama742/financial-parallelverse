import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "financial_parallelverse.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

API_PREFIX = "/api"
PROJECT_NAME = "Financial Parallelverse"
PROJECT_VERSION = "1.0.0"
CORS_ORIGINS = ["*"]
