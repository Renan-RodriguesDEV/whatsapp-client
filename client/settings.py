import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DIR_PROFILE = Path(os.getenv("DATA_DIR", "./session")).absolute()
DOWNLOADS_PATH = Path(os.getenv("DOWN_PATH", "./downloads")).absolute()
WHATSAPP_URL = "https://web.whatsapp.com/"
TIMEOUT = int(os.getenv("TIMEOUT", "120000"))
