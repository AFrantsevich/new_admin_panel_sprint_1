import os

from dotenv import load_dotenv
from split_settings.tools import include, optional

load_dotenv()

DEBUG = os.environ.get("DEBUG", False) == "True"
ALLOWED_HOSTS = []


base_settings = [
    "components/common.py",
    "components/database.py",
    optional("environments/local.py"),
]

include(*base_settings)
