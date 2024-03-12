from dataclasses import dataclass, asdict
from os import path, environ
from app.common.consts import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

base_dir = path.dirname(path.dirname(path.abspath(__file__)))

@dataclass
class Config:
    BASE_DIR = base_dir

    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True

@dataclass
class LocalConf(Config):
    PROJ_RELOAD: bool = True
    DB_URL: str = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def conf():
    config = dict(local = LocalConf())
    return config.get(environ.get("API_ENV", "local"))