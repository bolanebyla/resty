import logging
import time
from datetime import datetime, timedelta
from threading import Lock, Thread
from typing import Callable

import keyboard
import pyautogui
from classic.components import component

from resty.application.rest_timer import RestTimerService, RestTimerStatuses


@component
class UserActivityTracker:
    """
    Отслеживает активность пользователя за компьютером:
    использует компьютер или отошел
    """
    mouse_movement_tracking_time_sec: float
    user_activity_tracking_time_sec: float

    rest_timer_service: RestTimerService

    def __attrs_post_init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        # время последнего действия пользователя
        # (нажатия на клавиатуру или движение мышью)
        self._last_user_action_time = datetime.now()

        self.last_user_action_time_mutex = Lock()

        # устанавливаем колбэк обновления времени
        # последней активности пользователя
        # при нажатии на любую клавишу клавиатуры
        keyboard.on_press(lambda _: self._update_last_activity_user_time())

        # поток для трекинга движений мыши
        tracking_mouse_movement_thread = Thread(
            target=self._tracking_mouse_movement,
            daemon=True,
        )
        tracking_mouse_movement_thread.start()

    def _tracking_mouse_movement(self):
        """
        Наблюдает за позицией мыши
        и обновляет время последней активность пользователя при движении
        """
        _last_mouse_position = None
        while True:
            mouse_position = pyautogui.position()
            if mouse_position != _last_mouse_position:
                _last_mouse_position = mouse_position
                self._update_last_activity_user_time()

            time.sleep(self.mouse_movement_tracking_time_sec)

    def _update_last_activity_user_time(self):
        """
        Обновляет время последней активность пользователя
        """
        with self.last_user_action_time_mutex:
            self._last_user_action_time = datetime.now()

    def start_tracking_user_activity(
        self, on_user_not_active_status: Callable,
        on_user_activity_start: Callable
    ):
        """
        Запускает отслеживание активности пользователя
        и вызывает соответствующие колбэки в зависимости от статуса активности

        :param on_user_not_active_status: колбэк, который вызовется,
                если пользователь не активен какое-то время
        :param on_user_activity_start: колбэк, который вызовется,
                если пользователь стал снова активным
        """
        is_user_not_active = False
        while True:
            rest_timer = self.rest_timer_service.get_rest_timer()
            now = datetime.now()

            # если пользователь во время статуса работы стал не активным
            if rest_timer.status == RestTimerStatuses.work:
                if (now - self._last_user_action_time >= timedelta(
                        seconds=rest_timer.settings.rest_time_seconds)):
                    on_user_not_active_status()
                    is_user_not_active = True

            # если пользователь снова стал активным
            elif is_user_not_active:
                if (now - self._last_user_action_time <= timedelta(
                        seconds=self.user_activity_tracking_time_sec)):
                    on_user_activity_start()
                    is_user_not_active = False

            time.sleep(self.user_activity_tracking_time_sec)
