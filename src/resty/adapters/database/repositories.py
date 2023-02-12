from PyQt6.QtCore import QMutex

from resty.application.rest_timer import interfaces


class TimerRepo(interfaces.ITimerRepo):
    work_started = True
    rest_started = False

    def __init__(self):
        self.mutex = QMutex()

    def set_work_start(self):
        self.mutex.lock()
        self.work_started = True
        self.mutex.unlock()

    def set_rest_start(self):
        self.mutex.lock()
        self.rest_started = True
        self.mutex.unlock()

    def set_work_end(self):
        self.mutex.lock()
        self.work_started = False
        self.mutex.unlock()

    def set_rest_end(self):
        self.mutex.lock()
        self.rest_started = False
        self.mutex.unlock()

    def is_rest_started(self):
        return self.rest_started

    def is_work_started(self):
        return self.work_started
