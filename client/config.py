import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PATH_USER_DATA = Path(os.getenv("PATH_USER_DATA"))
PATH_DOWNLOADS = Path(os.getenv("PATH_DOWNLOADS"))
URL_WHATSAPP = os.getenv("URL_WHATSAPP")
TIMEOUT = int(os.getenv("TIMEOUT", "120000"))
