import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QWidget
from qt_material import apply_stylesheet

from resty.application import rest_timer

from . import signals, widgets

BASE_DIR: Path = Path(__file__).parent


class App(QApplication):
    widgets = []

    def register_widget(self, widget: QWidget):
        self.widgets.append(widget)

    def run(self):
        self.exec()


def create_app(
    rest_timer_service: rest_timer.RestTimerService,
    start_work_signal: signals.StartWorkSignal,
    start_rest_signal: signals.StartRestSignal,
):
    app = App(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    # setup stylesheet
    apply_stylesheet(
        app,
        theme='light_blue_500.xml',
        invert_secondary=True,
        css_file=str(BASE_DIR / 'resources' / 'style.css'),
    )

    app.register_widget(
        widgets.RestWindow(
            primary_screen=app.primaryScreen(),
            rest_timer_service=rest_timer_service,
            start_work_signal=start_work_signal,
            start_rest_signal=start_rest_signal,
        )
    )

    return app
