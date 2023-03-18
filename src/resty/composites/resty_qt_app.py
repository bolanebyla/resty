import sys

from resty.adapters import database, log, qt
from resty.application import rest_timer


class Settings:
    qt = qt.Settings()


class Logger:
    log.configure()


class DB:
    timer_repo = database.TimerRepo()


class Signals:
    start_work_signal = qt.StartWorkSignal()
    start_rest_signal = qt.StartRestSignal()


class Application:
    rest_timer_service = rest_timer.RestTimerService(
        event_update_time_msec=Settings.qt.EVENT_UPDATE_TIME_MSEC,
        timer_repo=DB.timer_repo,
        start_work_signal=Signals.start_work_signal,
        start_rest_signal=Signals.start_rest_signal,
    )


app = qt.create_app(
    event_update_time_msec=Settings.qt.EVENT_UPDATE_TIME_MSEC,
    rest_timer_service=Application.rest_timer_service,
    start_work_signal=Signals.start_work_signal,
    start_rest_signal=Signals.start_rest_signal,
)

if __name__ == '__main__':
    sys.exit(app.run())
