from typing import Optional

from pydantic import BaseSettings, Field


class DBSettings(BaseSettings):
    """
        Database Settings
    """

    TYPE: Optional[str] = Field(default='mysql', title="DB Type")
    HOST: Optional[str] = Field(default='127.0.0.1', title="DB Host")
    PORT: Optional[str] = Field(default='3306', title="DB Port")
    DATABASE: Optional[str] = Field(default='test', title="DB Database")
    USER: Optional[str] = Field(default='root', title="DB User")
    PASSWORD: Optional[str] = Field(default='root', title="DB Password")

    @property
    def dsn(self):
        return f"{self.TYPE.lower()}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"


class MySQLSettings(DBSettings):
    """
        MySQL Settings
    """

    class Config:
        env_prefix = 'MYSQL_'
        case_sensitive = True