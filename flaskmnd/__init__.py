import yaml

from flaskmnd.daflask import DaFlask
from flaskmnd.util.data import DaMongo
from flaskmnd.util.blueprint import util_blueprints
from flaskmnd.mvc.controllers import controller_blueprints

def create_app(test_config=None):
    app = DaFlask(__name__, instance_relative_config=True)
    
    load_config(app, test_config)

    if app.config["STANDALONE"]:
        connect_mongo(app)

    app.register_blueprint(util_blueprints)
    app.register_blueprint(controller_blueprints)
    
    return app


def load_config(app, test_config):
    if test_config is None:
        app.config.from_file('config.yml', load=yaml.safe_load)
    else:
        app.config.from_mapping(test_config)


def connect_mongo(app):
    app.mng = DaMongo(app.config["MONGO"])