import logging

import sys

from glycemiq_web.config import config_as_dict


class _LogManager:
    def __init__(self):
        self.config = config_as_dict('LOGGING')

        formatter = logging.Formatter(fmt=self.config['LOG_FORMAT'])

        self.handler = logging.StreamHandler(sys.stdout)  # TODO: make this come from config
        self.handler.setFormatter(formatter)

    def get_logger(self, name):
        logger = logging.getLogger(name)
        logger.addHandler(self.handler)
        logger.setLevel(getattr(logging, self.config['LOG_LEVEL']))

        return logger


logManager = _LogManager()
