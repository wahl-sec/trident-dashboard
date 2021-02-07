#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Trident: Trident Module.
Handles the logic that fetches and populates Trident daemons.

@author: Jacob Wahlman
"""

from os import path
from random import choice
from functools import partial
from typing import AnyStr, NewType
JSON = NewType("JSON", None)

from flask import Blueprint, request, current_app, make_response 

from trident import ROOT_DIR
from trident.database.handler import retrieve_decorator, insert_decorator, delete_decorator, insert_record, retrieve_record

retrieve_trident_record = partial(retrieve_decorator, tablename="Daemon")
retrieve_connected_trident_record = partial(retrieve_decorator, tablename="ConnectedDaemon")
insert_trident_record = partial(insert_decorator, tablename="Daemon")
delete_trident_record = partial(delete_decorator, tablename="Daemon")
delete_connected_trident_record = partial(delete_decorator, tablename="ConnectedDaemon")
blueprint = Blueprint("trident", __name__, url_prefix="/trident")


@blueprint.route("/connect", methods=["POST"])
def connect() -> JSON:
    """ Connect an Trident daemon to the dashboard.
    The endpoint accepts information regarding the daemon like, amount of workers,
    information about all plugins in the daemon and more.
    The endpoint returns the unique identification on the dashboard.
    """
    data = request.get_json()
    if data is None:
        return make_response("Bad Request", 400)

    def generate_daemon_name():
        daemon_name = None
        while daemon_name is None or retrieve_record(tablename="Daemon", daemon=daemon_name).first():
            with open(path.join(ROOT_DIR, "data", "english-adjectives.txt"), "r") as adjectives:
                with open(path.join(ROOT_DIR, "data", "animals.txt"), "r") as animals:
                    daemon_name = "{}-{}".format(choice(adjectives.readlines()).strip(), choice(animals.readlines()).strip())

        return daemon_name

    daemon_name = generate_daemon_name() if data.get("daemon", None) is None else data.get("daemon")
    if data.get("daemon", None) is None:
        arguments = data.get("arguments", {})
        try:
            daemon_record = {
                "daemon": daemon_name,
                "host_addr": data.get("host_addr"),
                "worker_count": data.get("worker_count"),
                "arguments": {
                    "logging_level": arguments.get("logging_level", None),
                    "args": arguments.get("args", None)
                }
            }
            insert_record(tablename="Daemon", **daemon_record)
        except Exception as e:
            current_app.logger.debug(f"'/connect' - Failed to insert record to 'Daemon' with error: {e}")
            return make_response("Bad Request", 400)

        try:
            plugins = arguments.get("plugins", {})
            for plugin_name, plugin_config in plugins.items():
                plugin_record = {
                    "plugin_name": plugin_name,
                    "arguments": plugin_config.get("args", None),
                    "daemon": daemon_name
                }
                insert_record(tablename="Plugin", **plugin_record)
        except Exception as e:
            current_app.logger.debug(f"'/trident/connect' - Failed to insert record to 'Plugin' with error: {e}")
            return make_response("Bad Request", 400)

    if retrieve_record(tablename="ConnectedDaemon", daemon=daemon_name).first():
        return make_response("Bad Request", 400)

    try:
        daemon_record = {
            "daemon": daemon_name
        }
        insert_record(tablename="ConnectedDaemon", daemon=daemon_name)
    except Exception as e:
        current_app.logger.debug(f"'/connect' - Failed to insert record to 'ConnectedDaemon' with error: {e}")
        return make_response("Bad Request", 400)

    return make_response({"daemon": daemon_name}, 201)

@blueprint.route("/disconnect/<daemon>", methods=["DELETE"])
@delete_connected_trident_record
def disconnect(daemon) -> None:
    """ Disconnect a Trident daemon from the dashboard.
    The endpoint takes an unique identifier for the Trident daemon
    and marks it as disconnected.
    """
    pass

@blueprint.route("/connected", methods=["GET"])
@retrieve_connected_trident_record
def connected() -> JSON:
    """ Returns all daemons that are current connected to the dashboard. """
    pass

@blueprint.route("/remove/<daemon>", methods=["DELETE"])
@delete_trident_record
@delete_connected_trident_record
def remove(daemon) -> None:
    """ Removes a Trident daemon from the dashboard.
    The endpoint takes an unique identifier for the Trident daemon
    and removes it from the daemons.
    """
    pass

@blueprint.route("/<daemon>", methods=["GET"])
@retrieve_trident_record
def daemon(daemon) -> JSON:
    """ Get information about the Trident daemon,
    the information includes arguments provided to the daemon, name of plugins and more.
    """
    pass
