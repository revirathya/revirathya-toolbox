from logging import Formatter, Logger, StreamHandler


class LogAdapter:
    __logger: Logger

    def __init__(self, name: str, log_level: str):
        self.__logger = Logger(name, log_level.upper())
        self.__setup_logger()


    # Public
    def debug(self, msg: str):
        self.__logger.debug(msg)

    def info(self, msg: str):
        self.__logger.info(msg)

    def warning(self, msg: str):
        self.__logger.warning(msg)

    def error(self, msg: str):
        self.__logger.error(msg)
    
    def critical(self, msg: str):
        self.__logger.critical(msg)


    # Private
    def __setup_logger(self):
        handler = StreamHandler()
        handler.setFormatter(
            fmt = Formatter(
                fmt = "[%(asctime)s] (%(name)s) %(levelname)s - %(message)s",
                datefmt = "%Y-%m-%d %H:%M:%S"
            )
        )

        self.__logger.addHandler(handler)
