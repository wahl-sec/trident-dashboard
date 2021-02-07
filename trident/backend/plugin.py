#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Trident: Plugin Module.
Handles the logic that fetches and publish information about plugins related to Trident Daemons.

@author: Jacob Wahlman
"""

from functools import partial
from typing import AnyStr, NewType
JSON = NewType("JSON", None)

from flask import Blueprint

from trident.database.handler import retrieve_decorator, insert_decorator

retrieve_plugins_record = partial(retrieve_decorator, tablename="Plugin")
blueprint = Blueprint("plugin", __name__, url_prefix="/plugin")


@blueprint.route("/<daemon>", methods=["GET"])
@retrieve_plugins_record
def plugins(daemon) -> JSON:
    """ Get all plugins stored in the database relating to a given Trident daemon.
    If the daemon does not exist then the returned value is empty and 404 is returned.
    If the request is successful then 200 is returned with the content in JSON format.
    """
    pass

@blueprint.route("/<daemon>/<plugin_name>", methods=["GET"])
@retrieve_plugins_record
def plugins_plugin(daemon, plugin_name) -> JSON:
    """ Get a specific plugin stored in the database relating to a given Trident daemon.
    If the daemon and/or plugin does not exist then the returned value is empty and 404 is returned.
    If the request is successful then 200 is returned with the content in JSON format.
    """
    pass
