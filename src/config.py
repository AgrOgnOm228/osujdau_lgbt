from typing import Any, List

from pydantic import ValidationInfo, field_validator
from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore',
        env_file='.env'
    )
    BASE_PATH_BACKGROUND: str = ''
    BASE_PATH_CAT: str = 'static/cat_skin'
    SCENE_STR: str = ''

    SCENE_LIST: List[str] | None = None

    @field_validator('SCENE_LIST', mode='before')
    @classmethod
    def create_scene_list_from_scene_str(cls, v: Any, info: ValidationInfo) -> Any:
        if isinstance(v, list):
            return v

        listed = info.data.get('SCENE_STR').split(',')

        return listed


settings = Settings()

APP_VERSION = '0.1.0'
