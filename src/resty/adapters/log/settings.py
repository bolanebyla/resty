from pydantic import BaseSettings


class Settings(BaseSettings):
    LOGGING_LEVEL: str = 'INFO'
    LOGGING_JSON: bool = True

    @property
    def LOGGING_CONFIG(self):
        fmt = '%(asctime)s.%(msecs)03d [%(levelname)s]|[%(name)s]: %(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'

        config = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'default': {
                    'format': fmt,
                    'datefmt': datefmt,
                },
                'json': {
                    'format': fmt,
                    'datefmt': datefmt,
                    'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
                },
            },
            'handlers': {
                'default': {
                    'level': self.LOGGING_LEVEL,
                    'formatter': 'json' if self.LOGGING_JSON else 'default',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['default'],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False
                },
            }
        }

        return config
