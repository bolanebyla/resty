import logging
import time
from datetime import datetime, timedelta
from typing import Union

import attr
from classic.components import component
from dateutil.tz import tzlocal

from . import entities, enums, errors, interfaces


@attr.frozen
class FullHalfHourCalculator:
    """
    Калькулятор для расчёта времени до наступления 30 минут или 00 на часах
    """

    def calculate_full_half_hour_time_sec(self) -> int:
        """
        Рассчитывает количество секунд до наступления 30 минут или 00 на часах
        относительно того к чему ближе

        Например:
            - если сейчас 15:20, то ближе 15:30, соответственно
            рассчитывается время как `15:30 - 15:20 = 600 сек`;
            - если сейчас 15:45, то ближе 16:00, соответственно
            рассчитывается время как `16:00 - 15:45 = 900 сек`
        """
        now = datetime.now(tz=tzlocal())

        if now.minute * 60 + now.second < 30 * 60:
            half_hour_time = 30 * 60 - (now.minute * 60 + now.second)
        else:
            half_hour_time = 60 * 60 - (now.minute * 60 + now.second)

        return half_hour_time


@component
class RestTimerService:
    timer_repo: interfaces.ITimerRepo

    start_work_signal: interfaces.ISignal
    start_rest_signal: interfaces.ISignal

    event_update_time_msec: float

    full_half_hour_calculator: FullHalfHourCalculator

    def __attrs_post_init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def _get_end_event_time(time_seconds: entities.SecondsType) -> datetime:
        end_event_time = datetime.now() + timedelta(seconds=time_seconds)
        return end_event_time

    def _start_work(self, rest_timer: entities.RestTimer):
        """
        Запуск работы
        """
        # отправляем сигнал о начале работы
        self.start_work_signal.emit()

        # меняем статус таймера на "работу"
        rest_timer.status = enums.RestTimerStatuses.work
        # рассчитываем время окончания работы
        rest_timer.end_event_time = self._get_end_event_time(
            time_seconds=rest_timer.settings.work_time_seconds
        )
        self.timer_repo.save_rest_timer(rest_timer=rest_timer)
        self.logger.debug(
            'Work is started, it will end at %s',
            rest_timer.end_event_time,
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
        rest_timer.end_event_time = self._get_end_event_time(
            time_seconds=rest_timer.settings.rest_time_seconds,
        )
        self.timer_repo.save_rest_timer(rest_timer=rest_timer)
        self.logger.debug(
            'Rest is started, it will end at %s',
            rest_timer.end_event_time,
        )

    def start_timer(self):
        # создаем таймер со статусом "работа"
        rest_timer = self.timer_repo.create_rest_timer(
            status=enums.RestTimerStatuses.work,
        )

        rest_timer.end_event_time = self._get_end_event_time(
            time_seconds=rest_timer.settings.work_time_seconds
        )
        self.timer_repo.save_rest_timer(rest_timer)

        # отправляем сигнал о начале работы
        self.start_work_signal.emit()
        self.logger.debug(
            'Work is started, it will end at %s',
            rest_timer.end_event_time,
        )

        while True:
            rest_timer = self.timer_repo.get_rest_timer()
            self.logger.debug('Timer status: %s', rest_timer.status.value)

            if rest_timer.status == enums.RestTimerStatuses.exit:
                return

            time_now = datetime.now()

            if rest_timer.status == enums.RestTimerStatuses.work:
                if rest_timer.end_event_time <= time_now:
                    # запускаем отдых
                    self._start_rest(rest_timer=rest_timer)

            elif rest_timer.status == enums.RestTimerStatuses.rest:
                if rest_timer.end_event_time <= time_now:
                    # запускаем работу
                    self._start_work(rest_timer=rest_timer)

            time.sleep(self.event_update_time_msec / 1000)

    def move_rest(self, for_seconds: Union[float, int]):
        """
        Отложить отдых на время (сек) - запустить работу на определенное время
        """
        self.start_work_signal.emit()

        rest_timer = self.timer_repo.get_rest_timer()

        rest_timer.status = enums.RestTimerStatuses.work
        rest_timer.end_event_time = self._get_end_event_time(
            time_seconds=for_seconds
        )

        self.timer_repo.save_rest_timer(rest_timer)

    def move_rest_by_5_min(self):
        """
        Отложить отдых на 5 мин
        """
        self.move_rest(for_seconds=5 * 60)

    def move_rest_by_10_min(self):
        """
        Отложить отдых на 10 мин
        """
        self.move_rest(for_seconds=10 * 60)

    def move_rest_to_full_half_hour(self):
        for_seconds = (
            self.full_half_hour_calculator.calculate_full_half_hour_time_sec()
        )
        self.move_rest(for_seconds=for_seconds)

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
        rest_timer.end_event_time = None

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

    def get_rest_timer(self) -> entities.RestTimer:
        """
        Получить RestTimer
        """
        rest_timer = self.timer_repo.get_rest_timer()

        if rest_timer is None:
            raise errors.RestTimerNotFound()

        return rest_timer
