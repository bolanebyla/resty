from datetime import datetime
from typing import Optional, Union

import attr
from . import enums

SecondsType = Union[float, int]


@attr.dataclass
class RestTimerSettings:
    work_time_seconds: SecondsType = 10
    rest_time_seconds: SecondsType = 10


@attr.dataclass
class RestTimer:

    status: enums.RestTimerStatuses
    settings: RestTimerSettings = attr.field(factory=RestTimerSettings)
    end_rest_time: Optional[datetime] = None
    end_work_time: Optional[datetime] = None
