from pydantic import BaseSettings


class Settings(BaseSettings):
    EVENT_UPDATE_TIME_MSEC: float = 100
    USER_ACTIVITY_TRACKING_TIME_SEC: float = 0.1
    MOUSE_MOVEMENT_TRACKING_TIME_SEC: float = 0.1
