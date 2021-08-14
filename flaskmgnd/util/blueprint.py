from flask import Blueprint, request, send_file, render_template
from flaskmgnd.util import scope, log, decorator, filedir, exception
import os, json


util_blueprints = Blueprint('util_blueprints', __name__)

@util_blueprints.before_request
def before_request():
    url = request.path
    scope.push_log_stack(url)
    log.debug_stack("request recieved")

@util_blueprints.after_request
def after_request(resp):
    tag, log_stack_data, log_stack = scope.pop_log_stack()
    duration = log_stack_data.get(scope.PARAM_KEY_STACK_DUR)
    log.debug_stack(f"response released with code {resp.status_code} in {duration} sec.", log_stack)
    resp.headers["Total-Duration-MilliSecond"] = duration
    return resp


@util_blueprints.route("/util/health", methods=["GET"])
@decorator.request_handler
def health():
    return {"status": "UP"}

@util_blueprints.route("/util/staticfile/<path>")
@decorator.request_handler
def staticfile(path: str):
    path = f"static/{path}"
    folders_and_files = path.split("/")
    static_path = filedir.path_from_source(*folders_and_files)
    if not os.path.exists(static_path):
        raise exception.NotFound(f"there is no file like {path}")
    return send_file(static_path)


@util_blueprints.route("/util/swagger")
def swagger():
    default_config = {
        "app_name": "Swagger UI",
        "dom_id": "#swagger-ui",
        "url": "/util/staticfile/swagger.yml",
        "layout": "StandaloneLayout",
        "deepLinking": True,
    }

    fields = {
        "app_name": "",
        "config_json": json.dumps(default_config)
        }
    return render_template("swagger.html", **fields)