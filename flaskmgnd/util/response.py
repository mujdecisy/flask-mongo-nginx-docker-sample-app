from flaskmgnd.util.pojo import Pojo
from flaskmgnd.util.exception import FlaskRestException

class Response(Pojo):
    status_code :int
    message :str
    data :dict

class ErrorResponse(Response):
    def from_exception(self, exc: FlaskRestException):
        self.status_code = exc.status_code
        self.message = exc.message

class SuccessResponse(Response):
    status_code = 200
    message = "Successful"