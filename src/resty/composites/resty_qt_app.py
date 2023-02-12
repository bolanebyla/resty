from resty.adapters import qt, database, log
from resty.application import rest_timer


class Logger:
    log.configure()


class DB:
    timer_repo = database.TimerRepo()


class Application:
    rest_timer = rest_timer.RestTimer(timer_repo=DB.timer_repo)


app = qt.create_app(rest_timer_service=Application.rest_timer)

if __name__ == '__main__':
    app.run()
