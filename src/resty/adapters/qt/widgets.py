import logging

from PyQt6 import uic
from PyQt6.QtCore import QThreadPool
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
            self.ui = uic.loadUi('resty/adapters/qt/ui/design.ui', self)

    def _init_tray(self):
        icon = QIcon('resty/adapters/qt/ui/icon.png')

        tray = QSystemTrayIcon(self)
        tray.setIcon(icon)
        tray.setVisible(True)

        menu = QMenu()

        rest_now_action = QAction('Rest now', self)
        # rest_now_action.triggered.connect(self.start_rest_timer)

        exit_action = QAction('Exit', self)

        menu.addAction(rest_now_action)
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
        self.hide()

    def start_rest(self):
        self.show()

    def move_rest_by_5_min(self):
        self.logger.debug('"move_rest_by_5_min" btn is pressed')

    def move_rest_by_10_min(self):
        self.logger.debug('"move_rest_by_10_min" btn is pressed')

    def finish_rest(self):
        self.logger.debug('"finish_rest" btn is pressed')
