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
from flaskgmnd.util.exception import NotFound

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
## **5 . Logger Configuration**
## **6 . Session Handling**
## **7 . DaMongo**
## **8 . Pojo**