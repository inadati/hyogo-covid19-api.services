import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
load_dotenv("../../.env")

FILE_NAME = "covid19.xlsx"
AWJ_DB_CONNECT_SETUP = os.environ.get("AWJ_DB_CONNECT_SETUP").strip("\"")