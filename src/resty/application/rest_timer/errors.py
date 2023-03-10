from classic.app import AppError


class RestTimerNotFound(AppError):
    msg_template = 'Rest timer not found'
    code = 'rest_timer.rest_timer_not_fFound'
