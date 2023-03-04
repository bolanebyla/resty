import copy
from datetime import datetime
from typing import Optional

from PyQt6.QtCore import QMutex

from resty.application.rest_timer import (
    ITimerRepo,
    RestTimer,
    RestTimerStatuses, entities,
)


class TimerRepo(ITimerRepo):
    _rest_timer: RestTimer = None

    def __init__(self):
        self.mutex = QMutex()

    def create_rest_timer(
            self,
            status: RestTimerStatuses,
            end_rest_time: Optional[datetime] = None,
            end_work_time: Optional[datetime] = None,
    ) -> RestTimer:
        if self._rest_timer is None:
            self._rest_timer = RestTimer(
                end_rest_time=end_rest_time,
                end_work_time=end_work_time,
                status=status,
            )

        return copy.deepcopy(self._rest_timer)

    def get_rest_timer(self) -> RestTimer:
        return copy.deepcopy(self._rest_timer)

    def save_rest_timer(self, rest_timer: entities.RestTimer):
        self.mutex.lock()
        self._rest_timer = rest_timer
        self.mutex.unlock()
