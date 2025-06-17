import sys

from resty.adapters import database, log, qt
from resty.adapters.qt import UserActivityTracker
from resty.application import rest_timer
from resty.application.rest_timer.services import FullHalfHourCalculator


class Settings:
    qt = qt.Settings()


class Logger:
    log.configure()


class DB:
    timer_repo = database.TimerRepo()


class Application:
    full_half_hour_calculator = FullHalfHourCalculator()

    rest_timer_service = rest_timer.RestTimerService(
        event_update_time_msec=Settings.qt.EVENT_UPDATE_TIME_MSEC,
        timer_repo=DB.timer_repo,
        full_half_hour_calculator=full_half_hour_calculator,
    )


class Qt:
    user_activity_tracker = UserActivityTracker(
        event_update_time_msec=Settings.qt.EVENT_UPDATE_TIME_MSEC,
        rest_timer_service=Application.rest_timer_service,
    )


app = qt.create_app(
    event_update_time_msec=Settings.qt.EVENT_UPDATE_TIME_MSEC,
    rest_timer_service=Application.rest_timer_service,
    user_activity_tracker=Qt.user_activity_tracker,
)

if __name__ == '__main__':
    sys.exit(app.run())
