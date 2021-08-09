class FlaskRestException(Exception):
    status_code :int
    message :str

#------------------------------------------------------------ --- 400 EXCEPTIONS
class BadRequest(FlaskRestException):
    def __init__(self, msg: str = ""):
        self.status_code = 400
        self.message :str = f"BadRequest : {msg}"
        super().__init__(self.message)

class Unauthorized(FlaskRestException):
    def __init__(self, msg: str = ""):
        self.status_code = 401
        self.message :str = f"Unauthorized : {msg}"
        super().__init__(self.message)

class NotFound(FlaskRestException):
    def __init__(self, msg: str = ""):
        self.status_code = 404
        self.message :str = f"NotFound : {msg}"
        super().__init__(self.message)


#---------------------------------------------------------------- 500 EXCEPTIONS
class InternalServerError(FlaskRestException):
    def __init__(self, msg: str = ""):
        self.status_code = 500
        self.message :str = f"InternalServerError : {msg}"
        super().__init__(self.message)

class UnhandledException(InternalServerError):
    def __init__(self, msg: str = ""):
        self.message :str = f"UnhandledException : {msg}"
        super().__init__(self.message)
    

#---------------------------------------------------------------- APP EXCEPTIONS
class ConfigurationError(Exception):
    def __init__(self, msg: str = ""):
        self.message :str = f"Configuration Missing or Wrong : {msg}"
        super().__init__(self.message)