import logging

from settings.settings import settings


def create_request_log():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(settings.PATH_TO_REQUEST_LOG)
    file_handler.setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)

    return logger


def create_row_sql_log():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sql_logger = logging.getLogger('sqlalchemy.engine')
    file_handler = logging.FileHandler(settings.PATH_TO_DATABASE_LOG)
    sql_logger.addHandler(file_handler)
    return sql_logger


logger = create_request_log()
sql_logger = create_row_sql_log()