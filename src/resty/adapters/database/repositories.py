import copy

from PyQt6.QtCore import QMutex

from resty.application.rest_timer import (
    ITimerRepo,
    RestTimer,
    RestTimerStatuses,
)


class TimerRepo(ITimerRepo):
    _rest_timer: RestTimer = None

    def __init__(self):
        self.mutex = QMutex()

    def create_rest_timer(
        self,
        status: RestTimerStatuses,
    ) -> RestTimer:
        if self._rest_timer is None:
            self._rest_timer = RestTimer(status=status)

        return copy.deepcopy(self._rest_timer)

    def get_rest_timer(self) -> RestTimer:
        return copy.deepcopy(self._rest_timer)

    def save_rest_timer(self, rest_timer: RestTimer):
        self.mutex.lock()
        self._rest_timer = rest_timer
        self.mutex.unlock()
