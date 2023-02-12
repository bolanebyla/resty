import time

from . import interfaces, errors


class RestTimer:
    def __init__(self, timer_repo: interfaces.ITimerRepo):
        self.timer_repo = timer_repo

    def start_work_timer(self, time_seconds=10):
        if time_seconds is None:
            time_seconds = 10

        self.timer_repo.set_rest_end()
        self.timer_repo.set_work_start()

        counter = 0
        while counter < time_seconds:
            time.sleep(1)
            counter += 1

            work_started = self.timer_repo.is_work_started()
            if not work_started:
                raise errors.TimerCanceled()

        self.timer_repo.set_work_end()

    def start_rest_timer(self, time_seconds=10):
        if time_seconds is None:
            time_seconds = 10

        self.timer_repo.set_work_end()
        self.timer_repo.set_rest_start()

        counter = 0
        while counter < time_seconds:
            time.sleep(1)
            counter += 1

            rest_started = self.timer_repo.is_rest_started()
            if not rest_started:
                raise errors.TimerCanceled()

        self.timer_repo.set_rest_end()
