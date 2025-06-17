from attr import define

from resty.application.rest_timer import (
    IRestTimerRepo,
    RestTimer,
    RestTimerStatuses,
)


@define
class TimerRepo(IRestTimerRepo):
    _rest_timer: RestTimer = None

    def create(
        self,
        status: RestTimerStatuses,
    ) -> RestTimer:
        if self._rest_timer is None:
            self._rest_timer = RestTimer(status=status)

        return self._rest_timer

    def get(self) -> RestTimer:
        return self._rest_timer

    def save_and_flash(self, rest_timer: RestTimer):
        self._rest_timer = rest_timer
