import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QWidget
from qt_material import apply_stylesheet

from resty.application import rest_timer

from . import widgets
from .user_activity import UserActivityTracker

BASE_DIR: Path = Path(__file__).parent


class App(QApplication):
    widgets = []

    def register_widget(self, widget: QWidget):
        self.widgets.append(widget)

    def run(self):
        self.exec()


def create_app(
    event_update_time_msec: float,
    rest_timer_service: rest_timer.RestTimerService,
    user_activity_tracker: UserActivityTracker
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
            event_update_time_msec=event_update_time_msec,
            primary_screen=app.primaryScreen(),
            rest_timer_service=rest_timer_service,
            user_activity_tracker=user_activity_tracker,
        )
    )

    return app
