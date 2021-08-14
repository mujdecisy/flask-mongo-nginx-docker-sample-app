## **1 . Generic Request Handling**
You can handle requests without considering error cases or json translation or sending files. `request_handler` decorator makes things easy.

```python
from flaskmgnd.util import decorator
from flask import Blueprint

bp = Blueprint('bp', __name__)

@bp.route("/foo")
@decorator.request_handler
def foo():
    return {"message": "hello from foo"}
```

## **2 . Authentication Schemas**
You can use **basic authentication** by configuring `instance/config.yml > BASIC_AUTH` parameters. And you can add `basic_auth_handler` decorator to your controller methods.

And also you can add **token based authentication** over http-headers > x-api-key by adding `token_auth_handler` decorator to your controller methods.

The token auth system is ready for management by `/api/user/session` endpoint over `flaskmgnd/mvc/controllers/user_session`.

```python
from flaskmgnd.util import decorator
from flask import Blueprint

bp = Blueprint('bp', __name__)

@bp.route("/foo")
@decorator.request_handler
@decorator.basic_auth_handler
def foo():
    return {"message": "foo is protected by basic auth"}

@bp.route("/bar")
@decorator.request_handler
@decorator.token_auth_handler
def bar():
    return {"message": "bar is protected by token auth"}
```

## **3 . Exception Flow**
You can fire `FlaskRestException` from anywhere and create inherited particular exceptions you need. Built-in exceptions:
- BadRequest
- Unauthorized
- NotFound
- InternalServerError
- UnhandledException

These exceptions are catched by the `request_handler` and transformed to the formal HTTP response.

```python
from flaskmgnd.util.exception import NotFound

fruit_stock = {
    "apple": 23,
    "pear": 42
}

def retrieve_stock(fruit):
    stock = fruit_stock.get(fruit)
    if stock == None:
        raise NotFound(f"There is no fruit like {fruit}")
    return stock
```

## **4 . Swagger Documentation**
You can manage your swagger documentation directly with built-in security schemas on `flaskmgnd/static/swagger.yml`. You can reach and use the swagger doc at `http://<ip|localhost>:<port>/util/swagger` easily.

## **5 . Logger Configuration**
Logs are configured for all run cases (flask run, gunicorn, docker) and can be tracked at `log/server.log`. The `TimedRotatingFileHandler` organises log files daily.

You can use flaskmgnd.util.log module from any class you need. You can configure the logger level at `/instance/config.yml > LEVEL_LOG`, and change log format at `/instance/config.yml > FORMAT_LOG`.

```python
from flaskmgnd.util import log

def foo():
    log.debug("this is a debug log")
    log.info("this is an info log")
    log.error("this is an error log")
```

## **7 . DaMongo**
You can use mongo db over `flaskmgnd.util.damongo.DaMongo` which is attached to the flask app generated at `flaskmgnd.daflask`. DaMongo will allow you to insert, update, delete and find transactions MongoDB.

It makes id transformations of objects to make easy to work on dictionary data. It is also positioned at the Flask object along application scope to avoid the wasted connection time for every request.

```python
from flask import current_app
from flaskmgnd.util import damongo, exception

def retrieve_fruit(name):
    mongo: damongo.DaMongo = current_app.mng
    res = mongo.select("fruit", {"name": name}, with_id=True)
    if len(res) < 1:
        raise exception.NotFound(f"There is no fruit founded with name : {name}")
    return res
```

## **8 . Pojo**
You can use `flaskmgnd.util.pojo.Pojo` on models, views and DTOS for high complex dictionary mapping operations. Pojo can translates objects to dicts recursively and vice versa.

```python
from flaskmgnd.util.pojo import Pojo

class B(Pojo):
    ba: str
    bb: int
    def __init__(self, ba: str, bb: int, data:str = None, fromclass = None) -> None:
        self.ba, self.bb = ba, bb
        return super().__init__(data, fromclass)
                
class A(Pojo):
    a: str
    b: int
    c: float
    d: B
    def __init__(self, a:str, b:int, c:float, d:B, data:str = None, fromclass = None) -> None:
        self.a, self.b, self.c, self.d = a, b, c, d
        return super().__init__(data, fromclass)

b = B("b str", 0)
a = A("a str", 1, 2.5, self.b)

print(a.to_dict())

'''
{
    "a" : "a str",
    "b" : 1,
    "c" : 2.5,
    "d" : {
        "ba" : "b str",
        "bb" : 0
    }
}
'''
```