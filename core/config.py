import os
import sys
from dotenv import load_dotenv

file_path = './.env'

# Check if .env file exists

if os.path.exists(file_path):
    load_dotenv(file_path)
    print(".env file loaded")
else:
    print(f'.env file {file_path} not found')
    sys.exit()

class Settings:
    PROJECT_NAME: str = "Simple Twitter"
    API_V1_STR: str = "/api/v1"
    PROJECT_VERSION: str = "1.0.0"
    USE_SQLITE_DB: str = os.getenv("USE_SQLITE_DB")
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER", "localhost")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", 3306)
    MYSQL_DB: str = os.getenv("MYSQL_DB", "tdd")
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins


settings = Settings()
