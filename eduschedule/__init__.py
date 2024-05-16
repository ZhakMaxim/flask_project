from flask import Flask

from .extensions import mongo

from .views import eduschedule_api_v1


def create_app(config_object='eduschedule.settings'):
    app = Flask(__name__)

    app.config.from_object(config_object)

    app.register_blueprint(eduschedule_api_v1)

    return app
