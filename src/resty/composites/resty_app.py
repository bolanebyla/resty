from resty.adapters import qt, database
from resty.application import rest_timer


class DB:
    timer_repo = database.TimerRepo()


class Application:
    rest_timer = rest_timer.RestTimer(timer_repo=DB.timer_repo)


app = qt.create_app()
window = qt.MainWindow(rest_timer=Application.rest_timer)

if __name__ == '__main__':
    app.exec()
