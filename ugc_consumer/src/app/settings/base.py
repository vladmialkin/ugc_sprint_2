from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


class Base(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR.joinpath('.env'),
        case_sensitive=True,
        extra='allow'
    )
