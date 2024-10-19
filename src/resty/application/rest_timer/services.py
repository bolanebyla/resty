import logging
from datetime import datetime, timedelta
from typing import Union

import attr
from dateutil.tz import tzlocal

from . import RestTimerNotFound, entities, enums, interfaces


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


@attr.frozen
class RestTimerService:
    timer_repo: interfaces.IRestTimerRepo
    event_update_time_msec: float
    full_half_hour_calculator: FullHalfHourCalculator

    logger = logging.getLogger('RestTimerService')

    @staticmethod
    def _get_end_event_time(time_seconds: entities.SecondsType) -> datetime:
        end_event_time = datetime.now() + timedelta(seconds=time_seconds)
        return end_event_time

    def start_work(self, rest_timer: entities.RestTimer):
        """
        Запуск работы
        """
        # меняем статус таймера на "работу"
        rest_timer.status = enums.RestTimerStatuses.work
        # рассчитываем время окончания работы
        rest_timer.end_event_time = self._get_end_event_time(
            time_seconds=rest_timer.settings.work_time_seconds
        )
        self.timer_repo.save_and_flash(rest_timer=rest_timer)
        self.logger.debug(
            'Work is started, it will end at %s',
            rest_timer.end_event_time,
        )

    def start_rest(self, rest_timer: entities.RestTimer):
        """
        Запуск отдыха
        """
        # меняем статус таймера на "отдых"
        rest_timer.status = enums.RestTimerStatuses.rest
        # рассчитываем время окончания отдыха
        rest_timer.end_event_time = self._get_end_event_time(
            time_seconds=rest_timer.settings.rest_time_seconds,
        )
        self.timer_repo.save_and_flash(rest_timer=rest_timer)
        self.logger.debug(
            'Rest is started, it will end at %s',
            rest_timer.end_event_time,
        )

    def create_rest_timer(self):
        """
        Создаёт таймер
        """
        # создаем таймер со статусом "работа"
        rest_timer = self.timer_repo.create(
            status=enums.RestTimerStatuses.work,
        )

        rest_timer.end_event_time = self._get_end_event_time(
            time_seconds=rest_timer.settings.work_time_seconds
        )
        self.timer_repo.save_and_flash(rest_timer)

        self.logger.debug(
            'Work is started, it will end at %s',
            rest_timer.end_event_time,
        )
        self.timer_repo.save_and_flash(rest_timer=rest_timer)

    def get_rest_timer(self) -> entities.RestTimer:
        """
        Получает таймер
        """
        rest_timer = self.timer_repo.get()

        if rest_timer is None:
            raise RestTimerNotFound()

        return rest_timer

    def update_rest_timer_state(self):
        """
        Обновить состояние таймера относительно текущего времени
        """
        rest_timer = self.get_rest_timer()

        time_now = datetime.now()

        self.logger.debug('rest_timer status: %s', rest_timer.status)
        if rest_timer.status == enums.RestTimerStatuses.work:
            if rest_timer.end_event_time <= time_now:
                # запускаем отдых
                self.rest_timer_service.start_rest(rest_timer=rest_timer)

        elif rest_timer.status == enums.RestTimerStatuses.rest:
            if rest_timer.end_event_time <= time_now:
                # запускаем работу
                self.rest_timer_service.start_work(rest_timer=rest_timer)

    def move_rest(self, for_seconds: Union[float, int]):
        """
        Отложить отдых на время (сек) - запустить работу на определенное время
        """
        rest_timer = self.get_rest_timer()

        rest_timer.status = enums.RestTimerStatuses.work
        rest_timer.end_event_time = self._get_end_event_time(
            time_seconds=for_seconds
        )

        self.timer_repo.save_and_flash(rest_timer)

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
        rest_timer = self.timer_repo.get()
        self.start_work(rest_timer=rest_timer)

    def rest_now(self):
        """
        Запустить отдых
        """
        rest_timer = self.timer_repo.get()
        self.start_rest(rest_timer=rest_timer)

    def stop(self):
        """
        Остановить таймер
        """
        rest_timer = self.timer_repo.get()

        rest_timer.status = enums.RestTimerStatuses.stop
        rest_timer.end_event_time = None

        self.timer_repo.save_and_flash(rest_timer)

    def start(self):
        """
        Начать работу
        """
        rest_timer = self.timer_repo.get()
        self.start_work(rest_timer=rest_timer)
