#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Trident: Result Module.
Handles the logic that fetches and populates the results generated by Trident plugins.

@author: Jacob Wahlman
"""

from functools import partial
from typing import AnyStr, NewType
JSON = NewType("JSON", None)

from flask import Blueprint, request, make_response, current_app

from trident.database.handler import retrieve_decorator, insert_decorator, delete_decorator, insert_record, retrieve_record

retrieve_results_record = partial(retrieve_decorator, tablename="Result")
insert_results_record = partial(insert_decorator, tablename="Result")
delete_results_record = partial(delete_decorator, tablename="Result")
blueprint = Blueprint("result", __name__, url_prefix="/result")


@blueprint.route("/<daemon>", methods=["GET"])
@retrieve_results_record
def results(daemon) -> JSON:
    """ Get all results for all plugins stored in the database relating to a given Trident daemon.
    If the daemon does not exist then the returned value is empty and 404 is returned.
    If the request is successful then 200 is returned with the content in JSON format.
    """
    pass

@blueprint.route("/<daemon>/<plugin_name>", methods=["GET"])
@retrieve_results_record
def results_plugin(daemon, plugin_name) -> JSON:
    """ Get all results for a specific plugin stored in the database relating to a given Trident daemon.
    If the daemon and/or the plugin does not exist then the returned value is empty and 404 is returned.
    If the request is successful then 200 is returned with the content in JSON format.
    """
    pass

@blueprint.route("/<daemon>/<plugin_name>/<index>", methods=["GET"])
@retrieve_results_record
def results_plugin_index(daemon, plugin_name, index) -> JSON:
    """ Get all results for a specific plugin at a given run index stored in the database relating to a given Trident daemon.
    If the daemon and/or the plugin does not exist then the returned value is empty and 404 is returned, same for the index.
    If the request is successful then 200 is returned with the content in JSON format.
    """
    pass

@blueprint.route("/<daemon>/<plugin_name>/<index>", methods=["POST"])
def post_results_plugin_index(daemon, plugin_name, index) -> None:
    """ Post a new result for a specific plugin at a given run index stored in the database relating to a given Trident daemon.
    If the daemon and/or the plugin does not exist then 404 is returned.
    If the run index already exists then the results for that index will be overwritten.
    If the request is successful then 204 is returned.
    """
    data = request.get_json()
    if data is None or not retrieve_record(tablename="Daemon", daemon=daemon).first():
        return make_response("Bad Request", 400)

    try:
        result_record = {
            "index": index,
            "result": data.get("result"),
            "plugin_name": plugin_name,
            "daemon": daemon
        }
        insert_record(tablename="Result", **result_record)
    except Exception as e:
        current_app.logger.debug(f"'/result/<daemon>/<plugin_name>/<index>' - Failed to insert record to 'Result' with error: {e}")
        return make_response("Bad Request", 400)

    return make_response("", 201)

@blueprint.route("/<daemon>", methods=["DELETE"])
@delete_results_record
def delete_results(daemon) -> None:
    """ Delete all results for all plugins stored in the database relating to a given Trident daemon.
    If the daemon does not exist then the returned value is empty and 404 is returned.
    If the request is successful then 202 is returned.
    """
    pass

@blueprint.route("/<daemon>/<plugin_name>", methods=["DELETE"])
@delete_results_record
def delete_results_plugin(daemon, plugin_name) -> None:
    """ Delete all results for a specific plugin stored in the database relating to a given Trident daemon.
    If the daemon and/or the plugin does not exist then the returned value is empty and 404 is returned.
    If the request is successful then 202 is returned.
    """
    pass

@blueprint.route("/<daemon>/<plugin_name>/<index>", methods=["DELETE"])
@delete_results_record
def delete_results_plugin_index(daemon, plugin_name, index) -> None:
    """ Delete all results for a specific plugin at a given run index stored in the database relating to a given Trident daemon.
    If the daemon and/or the plugin does not exist then the returned value is empty and 404 is returned, same for the index.
    If the request is successful then 202.
    """
    pass