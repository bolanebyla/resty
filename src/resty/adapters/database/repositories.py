import copy
from threading import Lock

from resty.application.rest_timer import (
    IRestTimerRepo,
    RestTimer,
    RestTimerStatuses,
)


class TimerRepo(IRestTimerRepo):
    _rest_timer: RestTimer = None

    def __init__(self):
        self.mutex = Lock()

    def create(
        self,
        status: RestTimerStatuses,
    ) -> RestTimer:
        if self._rest_timer is None:
            self._rest_timer = RestTimer(status=status)

        return copy.deepcopy(self._rest_timer)

    def get(self) -> RestTimer:
        return copy.deepcopy(self._rest_timer)

    def save_and_flash(self, rest_timer: RestTimer):
        with self.mutex:
            self._rest_timer = rest_timer
