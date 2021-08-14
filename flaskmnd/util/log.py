from flask import current_app
from flask.app import Flask
from flaskmnd.util import scope, filedir
from flask.logging import default_handler
import logging, sys
from logging.config import dictConfig
from logging.handlers import TimedRotatingFileHandler

def info(message: str):
    message = f"{scope.get_session_id()} : {message}"
    current_app.logger.info(message)

def debug(message: str):
    message = f"{scope.get_session_id()} : {message}"
    current_app.logger.debug(message)

def error(message: str):
    message = f"{scope.get_session_id()} : {message}"
    current_app.logger.error(message)

def info_stack(message, log_stack: list = None):
    if log_stack == None:
        log_stack = scope.get_log_stack()
    message = f"{scope.get_session_id()} : {log_stack} :{message}"
    current_app.logger.info(message)

def debug_stack(message, log_stack: list = None):
    if log_stack == None:
        log_stack = scope.get_log_stack()
    message = f"{scope.get_session_id()} : {log_stack} :{message}"
    current_app.logger.debug(message)

def error_stack(message):
    message = f"{scope.get_session_id()} : {scope.get_log_stack()} :{message}"
    current_app.logger.error(message)

def configure_logger(app: Flask):
    is_standalone = app.config["STANDALONE"]
    cus_fmtr = logging.Formatter(app.config["FORMAT_LOG"])
    level = {
            "INFO" : logging.INFO,
            "DEBUG" : logging.DEBUG,
            "WARN" : logging.WARN,
            "ERROR" : logging.ERROR
        }[app.config["LEVEL_LOG"]]
    
    app.logger.handlers.clear() # remove default handler

    #-------------------------------------------------------------- GUNI HANDLER
    if not is_standalone:
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers

    #-------------------------------------------------------------- FILE HANDLER
    file_log_handler = TimedRotatingFileHandler(
        filedir.path_from_project("log", "server.log"),
        when="midnight",
        backupCount=10
    )
    file_log_handler.setFormatter(cus_fmtr)
    file_log_handler.setLevel(level)
    app.logger.addHandler(file_log_handler)

    #------------------------------------------------------------ STREAM HANDLER
    if is_standalone:    
        stream_log_handler = logging.StreamHandler(sys.stdout)
        stream_log_handler.setFormatter(cus_fmtr)
        stream_log_handler.setLevel(level)
        app.logger.addHandler(stream_log_handler)

    #--------------------------------------------------------------- ROOT LOGGER
    app.logger.setLevel(level)

