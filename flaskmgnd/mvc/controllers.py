from flask import Blueprint, request
from flaskmgnd.util import decorator
from flaskmgnd.mvc import services


controller_blueprints = Blueprint('controller_blueprints', __name__)

@controller_blueprints.route("/api/admin/<objname>", methods=["GET", "POST", "DELETE"])
@decorator.request_handler
@decorator.basic_auth_handler
def administration(objname:str):
    if request.method == "POST":
        body = request.get_json()
        res = services.insert_object(objname, body)
    elif request.method == "GET":
        res = services.select_object(objname, {})
    elif request.method == "DELETE":
        params = dict(request.args)
        res = services.delete_object(objname, params)
    return res

@controller_blueprints.route("/api/user/session", methods=["POST", "DELETE"])
@decorator.request_handler
def user_session():
    if request.method == "POST":
        body = request.get_json()
        res = services.login_user(body.get("username"), body.get("password"))
    elif request.method == "DELETE":
        params = dict(request.args)
        services.logout_user(params.get("api_key"))
        res = {}
    return res

@controller_blueprints.route("/api/user/message", methods=["POST", "GET"])
@decorator.request_handler
@decorator.token_auth_handler
def user_message():
    if request.method == "POST":
        body = request.get_json()
        services.send_message(body["receiver_id"], body["context"])
        res = {}
    elif request.method == "GET":
        res = services.read_messages()
    return res