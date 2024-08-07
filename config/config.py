import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = str(os.getenv("TOKEN"))
GROUPS_ID = [int(id) for id in os.getenv("GROUPS_ID").split(",")]


DATABASE_NAME = 'users.sqlite3'

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
