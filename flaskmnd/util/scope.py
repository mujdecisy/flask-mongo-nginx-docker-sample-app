import os, hashlib
from flask import session
from datetime import datetime
from random import randint

PID = os.getpid()

KEY_ID = "id"
KEY_LOG_STACK = "logstack"
KEY_LOG_STACK_PARAMETERS = "logstack_parameters"
KEY_TOKEN_ATTRIBUTES = "token_attributes"

PARAM_KEY_TIME_START = "time_start"
PARAM_KEY_TIME_END = "time_end"
PARAM_KEY_STACK_DUR = "stack_duration"

def get_session_id() -> str:
    _id = session.get(KEY_ID)
    if _id != None:
        return _id
    
    unique_timestamp = str(datetime.now().timestamp()).replace(".","")[4:11]
    _id = f"{PID}-{unique_timestamp}"
    session[KEY_ID] = _id
    return _id

def push_log_stack(tag :str):
    log_stack = session.get(KEY_LOG_STACK, [])
    log_stack.append(tag)
    session[KEY_LOG_STACK] = log_stack

    log_stack_parameters = session.get(KEY_LOG_STACK_PARAMETERS, {})
    log_stack_parameters[tag] = {
        PARAM_KEY_TIME_START : datetime.now().timestamp()
    }
    session[KEY_LOG_STACK_PARAMETERS] = log_stack_parameters
    
def pop_log_stack() -> tuple:
    tag = None
    log_stack = session.get(KEY_LOG_STACK, [])
    if len(log_stack) > 0:
        tag = log_stack[-1]
        del log_stack[-1]
    session[KEY_LOG_STACK] = log_stack

    params = {}
    log_stack_parameters = session.get(KEY_LOG_STACK_PARAMETERS, {})
    if tag in log_stack_parameters.keys():
        params = log_stack_parameters[tag]
        del log_stack_parameters[tag]
    session[KEY_LOG_STACK_PARAMETERS] = log_stack_parameters

    params[PARAM_KEY_TIME_END] = datetime.now().timestamp()
    duration = params[PARAM_KEY_TIME_END]-params[PARAM_KEY_TIME_START]
    params[PARAM_KEY_STACK_DUR] = round(duration, 5)
    return tag, params, get_log_stack(log_stack + [tag])

def get_log_stack(log_stack: list = None) -> str:
    if log_stack == None:
        log_stack = session.get(KEY_LOG_STACK, [])
    return ">".join([" "]+log_stack)

def get_log_stack_parameter(tag :str) -> dict:
    log_stack_parameters = session.get(KEY_LOG_STACK_PARAMETERS, {})
    return log_stack_parameters.get(tag)

def update_log_stack_parameter(tag :str, key:str, val: object):
    log_stack_parameters = session.get(KEY_LOG_STACK_PARAMETERS, {})
    params = log_stack_parameters.get(tag)
    if params != None:
        params[key] = val
        log_stack_parameters[tag] = params
        session[KEY_LOG_STACK_PARAMETERS] = log_stack_parameters

def generate_sha(text:str, add_random=0) -> str:
    if add_random > 0:
        text += str(randint(10**add_random, 10**(add_random+1)-1))
    ho = hashlib.sha256(bytearray(text, "utf8"))
    ho = ho.hexdigest()
    return ho

def add(key:str, value: object) -> None:
    session[key] = value

def get(key:str) -> object:
    value = session.get(key)
    return value

def remove(key: str) -> None:
    if session.get(key) != None:
        del session[key]