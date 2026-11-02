
import os
import ssl
from pathlib import Path

import pymysql
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
CA_CERT = BASE_DIR / "certs" / "ca.pem"


def get_connection():
    contexto_ssl = ssl.create_default_context(
        cafile=str(CA_CERT)
    )

    return pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10,
        ssl=contexto_ssl
    )
