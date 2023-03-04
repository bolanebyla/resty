from PyQt6.QtWidgets import QApplication, QWidget

import sys

from resty.application import rest_timer

from . import widgets, signals


class App(QApplication):
    widgets = []

    def register_widget(self, widget: QWidget):
        self.widgets.append(widget)

    def run(self):
        self.exec()


def create_app(
        rest_timer_use_cases: rest_timer.RestTimerUseCases,
        start_work_signal: signals.StartWorkSignal,
        start_rest_signal: signals.StartRestSignal,
):
    app = App(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    app.register_widget(
        widgets.RestWindow(
            rest_timer_use_cases=rest_timer_use_cases,
            start_work_signal=start_work_signal,
            start_rest_signal=start_rest_signal,
        )
    )

    return app
