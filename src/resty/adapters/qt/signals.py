from PyQt6.QtCore import pyqtSignal, QObject


class StartWorkSignal(QObject):
    signal: pyqtSignal = pyqtSignal()

    def emit(self):
        self.signal.emit()


class StartRestSignal(QObject):
    signal: pyqtSignal = pyqtSignal()

    def emit(self):
        self.signal.emit()
