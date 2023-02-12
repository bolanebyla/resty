from PyQt6 import uic
from PyQt6.QtCore import QThreadPool
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu

from resty.adapters.qt.handlers import Worker

from resty.application.rest_timer import services


class MainWindow(QMainWindow):
    ui = None

    def __init__(self, rest_timer: services.RestTimer):
        super().__init__()

        self.rest_timer = rest_timer

        self._init_ui()
        self._init_tray()
        self._register_signals()

        self.threadpool = QThreadPool()

        self._start_work_timer()

    def _init_ui(self):
        try:
            from .ui import design

            self.ui = design.Ui_MainWindow()
            self.ui.setupUi(self)
        except ImportError:
            self.ui = uic.loadUi('resty/adapters/qt/ui/design.ui', self)

    def _init_tray(self):
        icon = QIcon('resty/adapters/qt/ui/icon.png')

        # Create the tray
        tray = QSystemTrayIcon(self)
        tray.setIcon(icon)
        tray.setVisible(True)

        menu = QMenu()
        action = QAction('A menu item', self)
        menu.addAction(action)

        tray.setContextMenu(menu)
        tray.show()

    def _register_signals(self):
        self.ui.btn_move_rest_by_5_min.clicked.connect(self.move_rest_by_5_min)
        self.ui.btn_move_rest_by_10_min.clicked.connect(self.move_rest_by_10_min)
        self.ui.btn_finish_rest.clicked.connect(self.finish_rest)

    def _start_work_timer(self, time_seconds=7):

        worker = Worker(self.rest_timer.start_work_timer, time_seconds)
        worker.signals.finished.connect(self._start_rest_timer)

        self.threadpool.start(worker)

        self.hide()

    def _start_rest_timer(self, time_seconds=7):
        worker = Worker(self.rest_timer.start_rest_timer, time_seconds)
        worker.signals.result.connect(self._start_work_timer)

        self.threadpool.start(worker)

        self.show()

    def move_rest_by_5_min(self):
        self._start_work_timer(time_seconds=5)

    def move_rest_by_10_min(self):
        self._start_work_timer(time_seconds=10)

    def finish_rest(self):
        self._start_work_timer()
