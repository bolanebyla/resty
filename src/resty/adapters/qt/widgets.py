import logging
import math
import sys
from datetime import datetime
from pathlib import Path
from random import choice

from classic.components import component
from PyQt6 import QtGui, uic
from PyQt6.QtCore import Qt, QThreadPool, QTimer
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QMenu, QSystemTrayIcon

from resty.adapters.qt.handlers import Worker
from resty.application.rest_timer import (
    RestTimerNotFound,
    RestTimerService,
    RestTimerStatuses,
)

from . import signals

BASE_DIR: Path = Path(__file__).parent

# TODO: перенести в слой приложения и создать сущность
rest_message_texts = [
    'Прежде чем осуждать кого-то, возьми его обувь и пройди его путь, '
    'попробуй его слезы, почувствуй его боли. Наткнись на каждый камень, '
    'о который он споткнулся. И только после этого говори ему, '
    'что ты знаешь, как правильно жить. Далай-Лама',
    'Есть вещи на которые ты можешь повлиять. '
    'Есть вещи, на которые ты повлиять не в силах. '
    'Сконцентрируйся на первых и оставь вторые. Стоицизм',
    'Все, что есть в этом мире, ты получаешь во временное пользование. '
    'Либо эта вещь или человек пропадут из твоей жизни, либо ты уйдешь сам. '
    'Не держись за предметы, всё, '
    'что у тебя есть, это твое достоинство. Стоицизм',
    'Человека определяют не атрибуты, а поступки. Стоицизм',
    'Иногда самые отвратительные проблемы разбивает в прах '
    'маленькая порция юмора. Далай-Лама'
]


@component
class RestWindow(QMainWindow):
    ui = None

    primary_screen: QtGui.QScreen

    rest_timer_service: RestTimerService

    start_work_signal: signals.StartWorkSignal
    start_rest_signal: signals.StartRestSignal

    event_update_time_msec: float

    def __attrs_post_init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

        self.threadpool = QThreadPool()

        self.on_create()

    def on_create(self):
        self.logger.info('Creating %s...', self.__class__.__name__)
        self._init_ui()
        self._init_tray()
        self._register_signals()

        # запускаем поток сервиса с таймером
        worker = Worker(self.rest_timer_service.start_timer)
        self.threadpool.start(worker)
        self.logger.info('Rest timer is started')

        # обновляем tooltip со статусом таймера
        self.show_rest_timer_status_tooltip()

    def _init_ui(self):
        try:
            from .ui.rest_window import rest_window

            self.ui = rest_window.Ui_RestWindow()
            self.ui.setupUi(self)
        except ImportError as e:
            self.logger.warning('Can\'t import python ui: %s', e)
            self.ui = uic.loadUi(
                'resty/adapters/qt/ui/rest_window/rest_window.ui', self
            )

        # устанавливаем флаги формы
        self.setWindowFlags(
            Qt.WindowType.Tool    # скрываем иконку с панели задач
            | Qt.WindowType.WindowStaysOnTopHint    # открывать поверх всех окон
            | Qt.WindowType.FramelessWindowHint    # убираем рамку вокруг формы
        )

        # включаем перенос строк
        self.ui.lbl_rest_message_text.setWordWrap(True)

        # таймер для прогрес бара отдыха
        self.rest_progress_timer = QTimer(self)
        self.rest_progress_timer.timeout.connect(self.update_rest_progress_bar)
        self.rest_progress_timer.timeout.connect(
            self.update_remaining_rest_time
        )

        # форма должна быть по центру экрана
        self._move_window_center()

        # форма должна появляться всегда на главном мониторе
        self.setScreen(self.primary_screen)

    def _move_window_center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _init_tray(self):
        icon = QIcon(
            str(BASE_DIR / 'resources' / 'images' / 'icons' / 'tray_icon.svg')
        )
        assert not icon.isNull()

        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(icon)
        self.tray.setVisible(True)

        menu = QMenu()

        rest_now_action = QAction('Отдых', self)
        rest_now_action.triggered.connect(self.rest_now)

        start_action = QAction('Перезапустить', self)
        start_action.triggered.connect(self.start_rest_timer)

        stop_action = QAction('Остановить таймер', self)
        stop_action.triggered.connect(self.stop_rest_timer)

        exit_action = QAction('Выход', self)
        exit_action.triggered.connect(self.exit)

        menu.addAction(rest_now_action)
        menu.addAction(start_action)
        menu.addAction(stop_action)
        menu.addAction(exit_action)

        self.tray.setContextMenu(menu)
        self.tray.show()

        tray_timer = QTimer(self)
        # обновляем время до перерыва
        tray_timer.timeout.connect(self.show_rest_timer_status_tooltip)
        tray_timer.start(self.event_update_time_msec)

    def _register_signals(self):
        self.start_work_signal.signal.connect(self.start_work)
        self.start_rest_signal.signal.connect(self.start_rest)

        self.ui.btn_move_rest_by_5_min.clicked.connect(self.move_rest_by_5_min)
        self.ui.btn_move_rest_by_10_min.clicked.connect(
            self.move_rest_by_10_min
        )
        self.ui.btn_finish_rest.clicked.connect(self.finish_rest)

    def start_work(self):
        self.logger.debug('Start work signal')
        self.hide()
        self.rest_progress_timer.stop()

    def start_rest(self):
        self.logger.debug('Start rest signal')
        self.ui.lbl_rest_message_text.setText(choice(rest_message_texts))
        self.ui.rest_progress_bar.setValue(100)
        self.rest_progress_timer.start(self.event_update_time_msec)
        self.show()

    def move_rest_by_5_min(self):
        self.logger.debug('"move_rest_by_5_min" btn is pressed')
        self.rest_timer_service.move_rest_by_5_min()

    def move_rest_by_10_min(self):
        self.logger.debug('"move_rest_by_10_min" btn is pressed')
        self.rest_timer_service.move_rest_by_10_min()

    def finish_rest(self):
        self.logger.debug('"finish_rest" btn is pressed')
        self.rest_timer_service.finish_rest()

    def rest_now(self):
        self.logger.debug('"rest_now" btn is pressed')
        self.rest_timer_service.rest_now()

    def stop_rest_timer(self):
        """
        Остановить таймер
        """
        self.logger.debug('"stop" btn is pressed')
        self.hide()
        self.rest_timer_service.stop()

    def start_rest_timer(self):
        """
        Запустить таймер
        """
        self.logger.debug('"start" btn is pressed')
        self.rest_timer_service.start()

    def exit(self):
        """
        Выйти из приложения (закрыть)
        """
        self.logger.debug('"exit" btn is pressed')
        self.rest_timer_service.exit()
        self.close()
        sys.exit()

    def show_rest_timer_status_tooltip(self):
        """
        Вывести подсказку с состоянием таймера
        """
        try:
            rest_timer = self.rest_timer_service.get_rest_timer()
        except RestTimerNotFound:
            rest_timer = None

        tool_tip_title = 'Resty'
        tool_tip_message = ''

        if rest_timer is not None:
            # если сейчас работа, выводим время до перерыва
            if rest_timer.status == RestTimerStatuses.work:
                # определяем сколько времени осталось до следующего перерыва
                next_break_time = rest_timer.end_event_time - datetime.now()

                # переводим оставшееся время в минуты
                # (округляем в большую сторону)
                next_break_time_minutes = math.ceil(
                    next_break_time.total_seconds() / 60
                )
                tool_tip_message = (
                    f'{next_break_time_minutes} '
                    f'мин до следующего перерыва'
                )

            elif rest_timer.status == RestTimerStatuses.rest:
                tool_tip_message = 'Отдых...'

            elif rest_timer.status == RestTimerStatuses.stop:
                tool_tip_message = 'Остановлен'

        tool_tip_text = f'{tool_tip_title}\n{tool_tip_message}'

        self.tray.setToolTip(tool_tip_text)

    def update_rest_progress_bar(self):
        """
        Обновляет значение прогресс-бара перерыва (от 100% к 0)
        """
        try:
            rest_timer = self.rest_timer_service.get_rest_timer()
        except RestTimerNotFound as e:
            self.logger.warning(e.message)
            return

        rest_time_seconds = rest_timer.settings.rest_time_seconds
        remaining_rest_time = rest_timer.get_remaining_time_before_event()

        progress = remaining_rest_time.total_seconds() / rest_time_seconds * 100

        self.ui.rest_progress_bar.setValue(progress)

    def update_remaining_rest_time(self):
        """
        Обновляет таймер оставшегося времени перерыва
        """
        try:
            rest_timer = self.rest_timer_service.get_rest_timer()
        except RestTimerNotFound as e:
            self.logger.warning(e.message)
            return

        remaining_rest_time = rest_timer.get_remaining_time_before_event()
        mm, ss = divmod(remaining_rest_time.seconds, 60)

        if mm <= 60:
            self.ui.lbl_remaining_rest_time.setText(f'{mm} мин {ss} сек')
        else:
            self.ui.lbl_remaining_rest_time.setText('')
