import logging
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format=("%(asctime)s | %(levelname)s | " "%(name)s | %(message)s"),
        handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8")],
        force=True,
    )

    # Reduce third-party SDK messages.
    for name in (
        "httpx",
        "httpcore",
        "google",
        "google_genai",
    ):
        logging.getLogger(name).setLevel(logging.WARNING)


setup_logging()

logger = logging.getLogger("rephrase_app")
