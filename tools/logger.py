import logging


def get_logger(name: str) -> logging.Logger:
    # Инициализация логгера с указанным именем
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
