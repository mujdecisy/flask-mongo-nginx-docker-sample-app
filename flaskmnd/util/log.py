from flask import current_app
from flaskmnd.util import scope
import os, logging, sys
from logging.handlers import TimedRotatingFileHandler


def debug(message: str):
    message = f"{scope.get_session_id()} : {message}"
    current_app.logger.debug(message)

def error(message: str):
    message = f"{scope.get_session_id()} : {message}"
    current_app.logger.error(message)

def debug_stack(message, log_stack: list = None):
    if log_stack == None:
        log_stack = scope.get_log_stack()
    message = f"{scope.get_session_id()} : {log_stack} :{message}"
    current_app.logger.debug(message)

def error_stack(message):
    message = f"{scope.get_session_id()} : {scope.get_log_stack()} :{message}"
    current_app.logger.error(message)


def configure():
    cus_fmtr = logging.Formatter(current_app.config.FORMAT_LOG)

    #-------------------------------------------------------------- FILE HANDLER
    file_log_handler = TimedRotatingFileHandler(
        file.path_from_project("log", "server.log"),
        when="midnight",
        backupCount=10
    )
    file_log_handler.setLevel(logging.DEBUG)
    file_log_handler.setFormatter(cus_fmtr)

    #------------------------------------------------------------ STREAM HANDLER
    stream_log_handler = logging.StreamHandler(sys.stdout)
    stream_log_handler.setFormatter(cus_fmtr)

    #--------------------------------------------------------------- ROOT LOGGER
    root_logger = logging.getLogger()
    root_logger.addHandler(stream_log_handler)
    root_logger.addHandler(file_log_handler)

    #-------------------------------------------------- DECREASE WERKZEUG LOGGER
    logging.getLogger("werkzeug").setLevel(logging.WARN)

