import logging
import time
from datetime import datetime, timedelta
from typing import Union

from classic.components import component

from . import interfaces, enums, entities


@component
class RestTimerUseCases:
    timer_repo: interfaces.ITimerRepo

    start_work_signal: interfaces.ISignal
    start_rest_signal: interfaces.ISignal

    def __attrs_post_init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def _get_end_rest_time(rest_time_seconds: entities.SecondsType) -> datetime:
        end_rest_time = datetime.now() + timedelta(seconds=rest_time_seconds)
        return end_rest_time

    @staticmethod
    def _get_end_work_time(work_time_seconds: entities.SecondsType) -> datetime:
        end_rest_time = datetime.now() + timedelta(seconds=work_time_seconds)
        return end_rest_time

    def _start_work(self, rest_timer: entities.RestTimer):
        """
        Запуск работы
        """
        # отправляем сигнал о начале работы
        self.start_work_signal.emit()

        # меняем статус таймера на "работу"
        rest_timer.status = enums.RestTimerStatuses.work
        # рассчитываем время окончания работы
        rest_timer.end_work_time = self._get_end_work_time(
            work_time_seconds=rest_timer.settings.work_time_seconds
        )
        self.timer_repo.save_rest_timer(rest_timer=rest_timer)
        self.logger.debug(
            'Work is started, it will end at %s',
            rest_timer.end_work_time,
        )

    def _start_rest(self, rest_timer: entities.RestTimer):
        """
        Запуск отдыха
        """
        # отправляем сигнал о начале отдыха
        self.start_rest_signal.emit()

        # меняем статус таймера на "отдых"
        rest_timer.status = enums.RestTimerStatuses.rest
        # рассчитываем время окончания отдыха
        rest_timer.end_rest_time = self._get_end_rest_time(
            rest_time_seconds=rest_timer.settings.rest_time_seconds,
        )
        self.timer_repo.save_rest_timer(rest_timer=rest_timer)
        self.logger.debug(
            'Rest is started, it will end at %s',
            rest_timer.end_rest_time,
        )

    def start_timer(self):
        # создаем таймер со статусом "работа"
        rest_timer = self.timer_repo.create_rest_timer(
            status=enums.RestTimerStatuses.work,
        )

        rest_timer.end_work_time = self._get_end_work_time(
            work_time_seconds=rest_timer.settings.work_time_seconds
        )
        self.timer_repo.save_rest_timer(rest_timer)

        # отправляем сигнал о начале работы
        self.start_work_signal.emit()
        self.logger.debug(
            'Work is started, it will end at %s',
            rest_timer.end_work_time,
        )

        while True:
            rest_timer = self.timer_repo.get_rest_timer()
            self.logger.debug('Timer status: %s', rest_timer.status.value)

            if rest_timer.status == enums.RestTimerStatuses.exit:
                return

            time_now = datetime.now()

            if rest_timer.status == enums.RestTimerStatuses.work:
                if rest_timer.end_work_time <= time_now:
                    # запускаем отдых
                    self._start_rest(rest_timer=rest_timer)

            elif rest_timer.status == enums.RestTimerStatuses.rest:
                if rest_timer.end_rest_time <= time_now:
                    # запускаем работу
                    self._start_work(rest_timer=rest_timer)

            time.sleep(1)

    def _move_rest(self, for_seconds: Union[float, int]):
        """
        Отложить отдых на время (сек) - запустить работу на определенное время
        """
        self.start_work_signal.emit()

        rest_timer = self.timer_repo.get_rest_timer()

        rest_timer.status = enums.RestTimerStatuses.work
        rest_timer.end_work_time = self._get_end_work_time(
            work_time_seconds=for_seconds
        )

        self.timer_repo.save_rest_timer(rest_timer)

    def move_rest_by_5_min(self):
        """
        Отложить отдых на 5 мин
        """
        self._move_rest(for_seconds=5 * 60)

    def move_rest_by_10_min(self):
        """
        Отложить отдых на 10 мин
        """
        self._move_rest(for_seconds=10 * 60)

    def finish_rest(self):
        """
        Завершить отдых и начать работу
        """
        rest_timer = self.timer_repo.get_rest_timer()
        self._start_work(rest_timer=rest_timer)

    def rest_now(self):
        """
        Запустить отдых
        """
        rest_timer = self.timer_repo.get_rest_timer()
        self._start_rest(rest_timer=rest_timer)

    def stop(self):
        """
        Остановить таймер
        """
        rest_timer = self.timer_repo.get_rest_timer()

        rest_timer.status = enums.RestTimerStatuses.stop
        rest_timer.end_work_time = None
        rest_timer.end_rest_time = None

        self.timer_repo.save_rest_timer(rest_timer)

    def start(self):
        """
        Начать работу
        """
        rest_timer = self.timer_repo.get_rest_timer()
        self._start_work(rest_timer=rest_timer)

    def exit(self):
        """
        Выключить таймер
        """
        rest_timer = self.timer_repo.get_rest_timer()
        rest_timer.status = enums.RestTimerStatuses.exit
        self.timer_repo.save_rest_timer(rest_timer)
