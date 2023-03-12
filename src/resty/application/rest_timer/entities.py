from datetime import datetime, timedelta
from typing import Optional, Union

import attr

from . import enums

SecondsType = Union[float, int]


@attr.dataclass
class RestTimerSettings:
    work_time_seconds: SecondsType = 40 * 60
    rest_time_seconds: SecondsType = 10 * 60


@attr.dataclass
class RestTimer:
    status: enums.RestTimerStatuses
    settings: RestTimerSettings = attr.field(factory=RestTimerSettings)
    end_event_time: Optional[datetime] = None

    def get_remaining_time_before_event(self) -> timedelta:
        """
        Получение оставшегося времени до события
        """
        remaining_event_time = (self.end_event_time - datetime.now())

        return remaining_event_time
