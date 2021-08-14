from flaskmgnd.mvc import models
from flaskmgnd.util import exception, response, log, data, scope

from base64 import b64encode
from flask import jsonify, request, current_app
import functools, traceback

def request_handler(func: callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        rsp: response.Response
        try:
            res = func(*args, **kwargs)
            if isinstance(res, dict) or isinstance(res, list):
                log.debug(f"response data generated as {str(res)}")
                rsp = response.SuccessResponse()
                rsp.data = res
            else:
                rsp = res
        except exception.FlaskRestException as ex1:
            log.error(traceback.format_exc())
            rsp = response.ErrorResponse()
            rsp.from_exception(ex1)
        except Exception as ex2:
            log.error(traceback.format_exc())
            ex2 = exception.UnhandledException(str(ex2))
            rsp = response.ErrorResponse()
            rsp.from_exception(ex2)

        if isinstance(rsp, response.Response):
            return jsonify(rsp.to_dict()), rsp.status_code
        else:
            return rsp, 200
    return wrapper

def basic_auth_handler(func: callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        username = current_app.config["BASIC_AUTH"]["username"]
        password = current_app.config["BASIC_AUTH"]["password"]

        auth = request.headers.get("Authorization")
        if auth == None:
            raise exception.Unauthorized()

        auth = auth.replace("Basic ", "")
        if auth == b64encode(bytes(f"{username}:{password}", "utf8")).decode("ascii"):
            res = func(*args, **kwargs)
            return res
        else:
            raise exception.Unauthorized()
    return wrapper


def token_auth_handler(func: callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if api_key == None:
            raise exception.Unauthorized()

        session_data = current_app.mng.select(models.Session.__name__, {"api_key": api_key})
        if len(session_data) > 0 :
            session_data = session_data[0]
            scope.add(scope.KEY_TOKEN_ATTRIBUTES, session_data)
            res = func(*args, **kwargs)
            scope.remove(scope.KEY_TOKEN_ATTRIBUTES)
            return res
        else:
            raise exception.Unauthorized()
    return wrapper