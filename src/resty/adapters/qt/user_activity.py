import logging
from datetime import datetime, timedelta
from typing import Callable

import keyboard
import pyautogui
from attr import define

from resty.application.rest_timer import RestTimerService, RestTimerStatuses


@define
class UserActivityTracker:
    """
    Отслеживает активность пользователя за компьютером:
    использует компьютер или отошел
    """
    logger = logging.getLogger('UserActivityTracker')

    event_update_time_msec: float

    rest_timer_service: RestTimerService

    # время последней активности пользователя
    _last_user_action_time: datetime = None
    # пользователь не активен
    _is_user_not_active: bool = False
    # последнее положение мыши
    _last_mouse_position: pyautogui.Point = None

    def __attrs_post_init__(self):

        # время последнего действия пользователя
        # (нажатия на клавиатуру или движение мышью)
        self._last_user_action_time = datetime.now()

        # устанавливаем колбэк обновления времени
        # последней активности пользователя
        # при нажатии на любую клавишу клавиатуры
        keyboard.on_press(lambda _: self._update_last_activity_user_time())

    def _update_last_activity_user_time(self):
        """
        Обновляет время последней активность пользователя
        """
        self._last_user_action_time = datetime.now()

    def processing_user_activity_events(
        self,
        on_user_not_active_status: Callable,
        on_user_activity_start: Callable,
    ):
        """
        Выполняет колбэки в зависимости от активности пользователя

        :param on_user_not_active_status: колбэк, который вызовется,
                если пользователь не активен какое-то время

        :param on_user_activity_start: колбэк, который вызовется,
                если пользователь стал снова активным
        """
        rest_timer = self.rest_timer_service.get_rest_timer()
        now = datetime.now()

        # если пользователь во время статуса работы стал не активным
        if rest_timer.status == RestTimerStatuses.work:
            rest_time = timedelta(seconds=rest_timer.settings.rest_time_seconds)
            if now - self._last_user_action_time >= rest_time:
                on_user_not_active_status()
                self._is_user_not_active = True

        # если пользователь снова стал активным
        elif self._is_user_not_active:
            diff = timedelta(milliseconds=self.event_update_time_msec * 10)
            if now - self._last_user_action_time <= diff:
                on_user_activity_start()
                self._is_user_not_active = False

    def track_user_activity(self):
        """
        Проверить активность пользователя
        """
        # проверяем, изменилось ли положение мыши
        mouse_position = pyautogui.position()
        if mouse_position != self._last_mouse_position:
            self._last_mouse_position = mouse_position
            self._update_last_activity_user_time()
