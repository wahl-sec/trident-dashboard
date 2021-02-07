#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import environ, path
from logging import DEBUG, INFO
ROOT_DIR = path.dirname(path.abspath(__file__))

from flask import Flask

from trident.database.models import database
import trident.backend.result
import trident.backend.plugin
import trident.backend.trident
import trident.backend.dashboard


def create_app(config=None) -> Flask:
    """ Create and configure the Flask application. """
    debug = True if environ.get("FLASK_ENV", "production") == "development" else False
    app = Flask(__name__, instance_relative_config=True, template_folder="templates")
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    app.logger.setLevel(DEBUG if debug else INFO)

    if config is not None:
        app.config.update(config)

    database.init_app(app)
    with app.app_context():
        database.create_all()

    app.register_blueprint(trident.backend.result.blueprint)
    app.register_blueprint(trident.backend.plugin.blueprint)
    app.register_blueprint(trident.backend.trident.blueprint)
    app.register_blueprint(trident.backend.dashboard.blueprint)
    
    return app

app = create_app()