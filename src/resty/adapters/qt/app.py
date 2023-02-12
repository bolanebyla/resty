from PyQt6.QtWidgets import QApplication, QWidget

import sys

from resty.application import rest_timer

from . import widgets


class App(QApplication):
    widgets = []

    def register_widget(self, widget: QWidget):
        self.widgets.append(widget)

    def run(self):
        self.exec()


def create_app(rest_timer_service: rest_timer.RestTimer):
    app = App(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    app.register_widget(widgets.MainWindow(rest_timer=rest_timer_service))

    return app
