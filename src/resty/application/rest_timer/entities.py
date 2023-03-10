from datetime import datetime
from typing import Optional, Union

import attr
from . import enums

SecondsType = Union[float, int]


@attr.dataclass
class RestTimerSettings:
    work_time_seconds: SecondsType = 60 * 5
    rest_time_seconds: SecondsType = 60 * 5


@attr.dataclass
class RestTimer:
    status: enums.RestTimerStatuses
    settings: RestTimerSettings = attr.field(factory=RestTimerSettings)
    end_event_time: Optional[datetime] = None
