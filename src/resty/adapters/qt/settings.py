from pydantic import BaseSettings


class Settings(BaseSettings):
    EVENT_UPDATE_TIME_MSEC: float = 100
