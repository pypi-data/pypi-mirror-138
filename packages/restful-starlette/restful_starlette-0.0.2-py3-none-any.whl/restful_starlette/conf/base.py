from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union, Type
from functools import lru_cache

from pydantic import BaseSettings, Field, PostgresDsn, IPvAnyAddress, BaseModel, AnyUrl
from pydantic.fields import ModelField
from pydantic.types import Path as PathType


class SystemSettings(BaseSettings):
    """
        System Settings
    """
    HOST: Optional[str] = '127.0.0.1'
    PORT: Optional[int] = 8001
    DEBUG: bool = True

    # BASE_DIR: Union[PathType, str, None]
    DOMAIN: Optional[str]
    FILE_SERVER: Optional[str] = Field(None, env="FILE_SERVER")


class GlobalSettings(BaseModel):
    """
        Global settings
    """
    SYSTEM_SETTINGS: SystemSettings

    @classmethod
    @lru_cache
    def get_global_settings(cls, env_path: Union[PathType, str, None] = '.env'):
        """
        get global settings and set into cache
        :param env_path:
        :return:
        """
        setting_models = cls.__fields__.copy()

        settings = {}
        for k, v in setting_models.items():
            if issubclass(type(v), ModelField):
                sub_setting_class = v.type_
                settings[k] = sub_setting_class(_env_file=str(env_path))

        return cls(**settings)

    @classmethod
    def generate_env_file(cls, path='./.env'):
        """
        生成配置文件
        :param path:
        :return:
        """
        envs = ''
        setting_models = cls.__fields__.copy()
        for k, v in setting_models.items():
            if issubclass(type(v), ModelField):
                sub_setting_class = v.type_
                envs += f"[{sub_setting_class.__name__}]\n"
                fields = sub_setting_class.__fields__.copy()
                for k, v in fields.items():
                    field_name = f'{sub_setting_class.Config.env_prefix}{k}'
                    envs += f"{field_name}={v.default}\n"
                envs += "\n"

        with open(file=path, mode='w') as f:
            f.writelines(envs)


# if __name__ == "__main__":
#     GlobalSettings.generate_env_file()
