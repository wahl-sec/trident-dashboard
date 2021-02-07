#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Trident: Dashboard Module.
Handles the logic for any representation in the dashboard.

@author: Jacob Wahlman
"""

from flask import Blueprint, render_template, request, current_app, make_response

from os import path
from typing import AnyStr, NewType
JSON = NewType("JSON", None)

from trident.database.handler import insert_record, retrieve_record
from trident import ROOT_DIR

blueprint = Blueprint("dashboard", __name__)


@blueprint.route("/", methods=["GET"])
def dashboard():
    """ Return the dashboard for the application.
    The dashboard is constructed using a template and gives an overview of Trident.
    """
    return render_template("dashboard.html")

@blueprint.route("/status", methods=["GET"])
def status() -> JSON:
    """ Get the current status of the dashboard like the amount of nodes connected,
    the URL of the dashboard and more information regarding the dashboard.
    """
    return make_response("", 200)