from datetime import datetime
from typing import Optional

import attr
from . import enums


@attr.dataclass
class RestTimer:
    status: enums.RestTimerStatuses
    end_rest_time:  Optional[datetime] = None
    end_work_time: Optional[datetime] = None
