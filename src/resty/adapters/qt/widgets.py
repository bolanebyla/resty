import logging
import sys

from PyQt6 import uic
from PyQt6.QtCore import QThreadPool, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu
from classic.components import component

from resty.adapters.qt.handlers import Worker

from resty.application.rest_timer import RestTimerUseCases

from . import signals


@component
class RestWindow(QMainWindow):
    ui = None

    rest_timer_use_cases: RestTimerUseCases

    start_work_signal: signals.StartWorkSignal
    start_rest_signal: signals.StartRestSignal

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
        worker = Worker(self.rest_timer_use_cases.start_timer)
        self.threadpool.start(worker)

    def _init_ui(self):
        try:
            from .ui import design

            self.ui = design.Ui_MainWindow()
            self.ui.setupUi(self)
        except ImportError:
            self.ui = uic.loadUi(
                'resty/adapters/qt/ui/rest_window/rest_window.ui', self
            )

        # устанавливаем флаги формы
        self.setWindowFlags(
            Qt.WindowType.Tool  # скрываем иконку с панели задач
            | Qt.WindowType.WindowStaysOnTopHint  # открывать поверх всех окон
            | Qt.WindowType.FramelessWindowHint  # убираем рамку вокруг формы
        )

    def _init_tray(self):
        icon = QIcon('resty/adapters/qt/ui/icon.png')

        tray = QSystemTrayIcon(self)
        tray.setIcon(icon)
        tray.setVisible(True)

        menu = QMenu()

        rest_now_action = QAction('Rest now', self)
        rest_now_action.triggered.connect(self.rest_now)

        start_action = QAction('Start', self)
        start_action.triggered.connect(self.start)

        stop_action = QAction('Stop', self)
        stop_action.triggered.connect(self.stop)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.exit)

        menu.addAction(rest_now_action)
        menu.addAction(start_action)
        menu.addAction(stop_action)
        menu.addAction(exit_action)

        tray.setContextMenu(menu)
        tray.show()

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

    def start_rest(self):
        self.logger.debug('Start rest signal')
        self.show()

    def move_rest_by_5_min(self):
        self.logger.debug('"move_rest_by_5_min" btn is pressed')
        self.rest_timer_use_cases.move_rest_by_5_min()

    def move_rest_by_10_min(self):
        self.logger.debug('"move_rest_by_10_min" btn is pressed')
        self.rest_timer_use_cases.move_rest_by_10_min()

    def finish_rest(self):
        self.logger.debug('"finish_rest" btn is pressed')
        self.rest_timer_use_cases.finish_rest()

    def rest_now(self):
        self.logger.debug('"rest_now" btn is pressed')
        self.rest_timer_use_cases.rest_now()

    def stop(self):
        self.logger.debug('"stop" btn is pressed')
        self.hide()
        self.rest_timer_use_cases.stop()

    def start(self):
        self.logger.debug('"start" btn is pressed')
        self.rest_timer_use_cases.start()

    def exit(self):
        self.logger.debug('"exit" btn is pressed')
        self.rest_timer_use_cases.exit()
        self.close()
        sys.exit()
