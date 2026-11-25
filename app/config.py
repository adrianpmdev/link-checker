"""
Config

Central application settings. Values can be overridden with environment
variables so the same code runs locally and in any deployment.

@author adrianpmdev
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = Path(os.getenv("DB_PATH", BASE_DIR / "data" / "link_checker.db"))
SEED_SAMPLE_DATA = os.getenv("SEED_SAMPLE_DATA", "true").lower() == "true"
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "60"))
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))
USER_AGENT = "LinkChecker/1.0"
