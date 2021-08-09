from flaskmnd.daflask import DaFlask
from flaskmnd.mvc import models, views
from flaskmnd.util import data, exception, scope
from flask import current_app

from datetime import datetime as dt, timedelta as td

def insert_object(objname: str, body):
    possible_objects = [models.User]
    if body.get("_id"):
        del body["_id"]

    is_a_real_object = False
    for e in possible_objects:
        if objname == e.__name__:
            o = e(body, e)
            o.check_self()
            current_app.mng.insert(objname, [o.to_dict()])
            is_a_real_object = True
            break
    
    if not is_a_real_object:
        raise exception.NotFound("wrong url")
    return {}


def select_object(objname:str, query:dict):
    possible_objects = [models.User]
    is_a_real_object = False
    res = {}
    for e in possible_objects:
        if objname == e.__name__:
            res = current_app.mng.select(objname, query, with_id=True)
            is_a_real_object = True
            break
    
    if not is_a_real_object:
        raise exception.NotFound("wrong url")

    return res

def delete_object(objname: str, query:dict):
    possible_objects = [models.User]
    is_a_real_object = False
    res = {}
    for e in possible_objects:
        if objname == e.__name__:
            res = [current_app.mng.delete(objname, query)]
            is_a_real_object = True
            break
    
    if not is_a_real_object:
        raise exception.NotFound("wrong url")

    return res


def login_user(username: str, password:str):
    if username == None or password == None:
        raise exception.BadRequest("missing parameters in body [username, password]")
    
    res = current_app.mng.select("User", {"username": username, "password": password}, with_id = True)

    if len(res) < 1:
        raise exception.Unauthorized("wrong credentials")
    
    user = models.User(res[0])

    now = dt.now()
    api_key = scope.generate_sha( now.isoformat() + username + password, add_random=5 )
    
    session = models.Session()
    session.api_key = api_key
    session.user_id = user._id
    session.created_at = now.isoformat()
    now += td(minutes=current_app.config["SESSION_EXPIRE"])
    session.ends_at = now.isoformat()

    current_app.mng.insert(models.Session.__name__, [session.to_dict()])

    return {"api_key": api_key}


def logout_user(api_key:str):
    if api_key == None:
        raise exception.BadRequest("missing parameters in url [api_key]")
    current_app.mng.delete(models.Session.__name__, {"api_key": api_key})
    return {}


def send_message(receiver_username:str, context:str):
    mng: data.DaMongo = current_app.mng

    session_data = models.Session(scope.get(scope.KEY_TOKEN_ATTRIBUTES))
    sender_id = session_data.user_id

    res = mng.select(models.User.__name__, {"username": receiver_username}, with_id=True)
    print(res)

    if len(res) < 1:
        raise exception.NotFound(f"user not found with username > {receiver_username}")

    message = models.Message()
    message.receiver = res[0]["_id"]
    message.sender = sender_id
    message.context = context
    message.send_at = dt.now().isoformat()
    message.read_already = False

    current_app.mng.insert(models.Message.__name__, [message.to_dict()])
    return {}

def read_messages():
    mng: data.DaMongo = current_app.mng

    session_data = models.Session(scope.get(scope.KEY_TOKEN_ATTRIBUTES))
    user_id = session_data.user_id
    res = mng.select(models.Message.__name__, {"receiver": user_id, "read_already": False}, with_id=True)
    query = {"_id": {"$in" : [e["_id"] for e in res]}}
    mng.update(models.Message.__name__, query, {"read_already": True})
    senders = mng.select(models.User.__name__, {
        "_id" : {
            "$in": list(map(lambda x: x["sender"], res)) 
            }
        }, 
        with_id=True
    )

    senders = {e["_id"]: e["username"] for e in senders}

    for i in range(len(res)):
        res[i]["sender"] = senders[res[i]["sender"]]
        res[i] = views.Message(res[i], fromclass=views.Message).to_dict()

    return res