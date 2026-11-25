import os

import dotenv

dotenv.load_dotenv(override=True)

SQLITE_PATH = os.getenv("SQLITE_PATH", "sqlite.db")
REPOSITORY_URL = os.getenv("REPOSITORY_URL", "https://github.com/imbastos/gunther")