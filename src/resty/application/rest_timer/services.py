import logging
import time
from datetime import datetime, timedelta
from typing import Union

from classic.components import component

from . import interfaces, enums


@component
class RestTimerUseCases:
    timer_repo: interfaces.ITimerRepo

    start_work_signal: interfaces.ISignal
    start_rest_signal: interfaces.ISignal

    def __attrs_post_init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def _get_end_rest_time(
            rest_time_seconds: Union[float, int] = 10
    ) -> datetime:
        end_rest_time = datetime.now() + timedelta(seconds=rest_time_seconds)
        return end_rest_time

    @staticmethod
    def _get_end_work_time(
            work_time_seconds: Union[float, int] = 5
    ) -> datetime:
        end_rest_time = datetime.now() + timedelta(seconds=work_time_seconds)
        return end_rest_time

    def start_timer(self):
        rest_timer = self.timer_repo.create_rest_timer(
            end_work_time=self._get_end_work_time(),
            status=enums.RestTimerStatuses.work
        )

        self.start_work_signal.emit()
        self.logger.debug(
            'Work is started, it will end at %s',
            rest_timer.end_work_time,
        )

        while True:
            rest_timer = self.timer_repo.get_rest_timer()

            time_now = datetime.now()

            if rest_timer.status == enums.RestTimerStatuses.work:
                if rest_timer.end_work_time <= time_now:
                    # запускаем отдых
                    self.start_rest_signal.emit()

                    # меняем статус таймера на "отдых"
                    rest_timer.status = enums.RestTimerStatuses.rest
                    # рассчитываем время окончания отдыха
                    rest_timer.end_rest_time = self._get_end_rest_time()
                    self.timer_repo.save_rest_timer(rest_timer=rest_timer)
                    self.logger.debug(
                        'Rest is started, it will end at %s',
                        rest_timer.end_work_time,
                    )

            elif rest_timer.status == enums.RestTimerStatuses.rest:
                if rest_timer.end_rest_time <= time_now:
                    # запускаем работу
                    self.start_work_signal.emit()

                    # меняем статус таймера на "работу"
                    rest_timer.status = enums.RestTimerStatuses.work
                    # рассчитываем время окончания работы
                    rest_timer.end_work_time = self._get_end_work_time()
                    self.timer_repo.save_rest_timer(rest_timer=rest_timer)
                    self.logger.debug(
                        'Work is started, it will end at %s',
                        rest_timer.end_work_time,
                    )

            time.sleep(1)
