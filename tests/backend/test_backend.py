#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Trident: Test Backend Module.
Tests the logic for the Trident Dashboard backend.

@author: Jacob Wahlman
"""

import pytest

from tests.fixture.client import client, tired_panda, round_giraffe, find_file_result, improved_find_file_result, cool_kitten


def test_dashboard_smoke(client):
    """ Smoke test to ensure the dashboard endpoint is up. """
    assert client.get("/").status_code == 200

def test_status_dashboard(client):
    """ Test get the status of the dashboard. """
    response = client.get("/status")
    assert response.status_code == 200

def test_connect_daemon(client):
    """ Test connect a Trident daemon to the dashboard. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    response = client.get("/trident/{}".format(response.get_json()["daemon"]))
    assert response.status_code == 200

def test_connect_invalid_daemon(client):
    """ Test connect an invalid daemon to the dashboard. """
    response = client.get("/trident/cool-kitten")
    assert response.status_code == 404

    response = client.post("/trident/connect", json=cool_kitten)
    assert response.status_code == 400
    assert response.get_json() is None

def test_daemon_connected(client):
    """ Test if a daemon is connected to the dashboard. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    daemon_name = response.get_json()["daemon"]
    response, = client.get("/trident/connected").get_json()
    assert response["daemon"] ==  daemon_name

def test_disconnect_daemon(client):
    """ Test disconnect a daemon from the dashboard. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201
    
    daemon_name = response.get_json()["daemon"]
    response, = client.get("/trident/connected").get_json()
    assert response["daemon"] ==  daemon_name

    response = client.delete("/trident/disconnect/{}".format(daemon_name))
    assert response.status_code == 202

    response = client.get("/trident/connected")
    assert response.status_code == 404

    response = client.get("/trident/{}".format(daemon_name))
    assert response.status_code == 200

def test_disconnect_non_connected_daemon(client):
    """ Test disconnect a daemon from the dashboard. """
    response = client.delete("/trident/disconnect/tired-panda")
    assert response.status_code == 202

def test_remove_daemon(client):
    """ Test remove a Trident daemon from the dashboard. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201
    daemon = response.get_json()["daemon"]

    response = client.get("/trident/{}".format(daemon))
    assert response.status_code == 200

    response = client.delete("/trident/remove/{}".format(daemon))
    assert response.status_code == 202

    response = client.get("/trident/{}".format(daemon))
    assert response.status_code == 404

def test_remove_non_connected_daemon(client):
    """ Test remove a daemon that is not connected to the dashboard. """
    response = client.delete("/trident/remove/tired-panda")
    assert response.status_code == 202

def test_retrieve_daemon(client):
    """ Test get information about an connected client. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    response = client.get("/trident/{}".format(response.get_json()["daemon"]))
    assert response.status_code == 200

def test_retrieve_non_connected_daemon(client):
    """ Test retrieve information about a non-connected daemon. """
    response = client.get("/trident/tired-panda")
    assert response.status_code == 404

def test_repeated_connect_daemon(client):
    """ Test repeatedly connecting the same daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    daemon = tired_panda.copy()
    daemon["daemon"] = response.get_json()["daemon"]
    response = client.post("/trident/connect", json=daemon)
    assert response.status_code == 400

def test_retrieve_plugins(client):
    """ Test retrieve all plugins for a given daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201
    
    plugins = client.get("/plugin/{}".format(response.get_json()["daemon"])).get_json()
    assert {plugin.get("plugin_name") for plugin in plugins} == {"find-file", "scan-hosts-file"}
    assert len(plugins) == 2

def test_retrieve_plugin(client):
    """ Test retrieve a specific plugin for a given daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    plugin, = client.get("/plugin/{}/find-file".format(response.get_json()["daemon"])).get_json()
    assert plugin.get("plugin_name") == "find-file"

def test_retrieve_non_existant_plugin(client):
    """ Test retrieve a specific plugin that does not exist for a given daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    response = client.get("/plugin/tired-panda/plugin-name")
    assert response.status_code == 404

def test_insert_result(client):
    """ Test insert a new result for the specific plugin for a given daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    response = client.post("/result/{}/find-file/0".format(response.get_json()["daemon"]), json=find_file_result)
    assert response.status_code == 201

def test_insert_result_in_non_connected_daemon(client):
    """ Test insert a new result in a non-connected daemon. """
    response = client.post("/result/tired-panda/find-file/0", json=find_file_result)
    assert response.status_code == 400

def test_retrieve_results(client):
    """ Test retrieve all results for the specific plugin for a given daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    daemon = response.get_json()["daemon"]
    response = client.post("/result/{}/find-file/0".format(daemon), json=find_file_result)
    assert response.status_code == 201

    response, = client.get("/result/{}".format(daemon)).get_json()
    assert response["result"]["2"] == "file2.html"

def test_retrieve_results_from_non_connected_daemon(client):
    """ Test retrieve all results for the specific plugin for a non-connected daemon. """
    response = client.get("/result/tired-panda")
    assert response.status_code == 404

def test_retrieve_results_from_no_results_daemon(client):
    """ Test retrieve all results for the specific plugin for a given daemon with no results. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    daemon = response.get_json()["daemon"]
    response = client.get("/result/{}".format(daemon))
    assert response.status_code == 404

def test_retrieve_result(client):
    """ Test retrieve results for a specific plugin for a given daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    daemon = response.get_json()["daemon"]
    response = client.post("/result/{}/find-file/0".format(daemon), json=find_file_result)
    assert response.status_code == 201

    response = client.post("/result/{}/scan-hosts-file/0".format(daemon), json=find_file_result)
    assert response.status_code == 201

    response, = client.get("/result/{}/find-file".format(daemon)).get_json()
    assert response["plugin"] == "find-file"

def test_retrieve_result_non_existant_plugin(client):
    """ Test retrieve results for a specific plugin for a given daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    daemon = response.get_json()["daemon"]
    response = client.get("/result/{}/improved-find-file".format(daemon))
    assert response.status_code == 404

def test_retrieve_result_index(client):
    """ Test retrieve results at a given index for a specific plugin for a given daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    daemon = response.get_json()["daemon"]
    response = client.post("/result/{}/find-file/0".format(daemon), json=find_file_result)
    assert response.status_code == 201

    response = client.post("/result/{}/find-file/1".format(daemon), json=improved_find_file_result)
    assert response.status_code == 201

    response, = client.get("/result/{}/find-file/1".format(daemon)).get_json()
    assert response["result"]["1"] == "file1.html"

    response, = client.get("/result/{}/find-file/0".format(daemon)).get_json()
    assert response["result"]["1"] == None

def test_retrieve_result_non_existant_index(client):
    """ Test retrieve results at a given index that does not exist for a specific plugin for a given daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    daemon = response.get_json()["daemon"]
    response = client.post("/result/{}/find-file/0".format(daemon), json=find_file_result)
    assert response.status_code == 201

    response = client.get("/result/{}/find-file/1".format(daemon))
    assert response.status_code == 404

def test_delete_results(client):
    """ Test delete all results for a given daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    daemon = response.get_json()["daemon"]
    response = client.post("/result/{}/find-file/0".format(daemon), json=find_file_result)
    assert response.status_code == 201

    response = client.post("/result/{}/find-file/1".format(daemon), json=improved_find_file_result)
    assert response.status_code == 201

    response = client.delete("/result/{}".format(daemon))
    assert response.status_code == 202

    response = client.get("/result/{}".format(daemon))
    assert response.status_code == 404

def test_delete_results_non_existant_daemon(client):
    """ Test delete all results for a given non-existant daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    daemon = response.get_json()["daemon"]
    response = client.post("/result/{}/find-file/0".format(daemon), json=find_file_result)
    assert response.status_code == 201

    response = client.post("/result/{}/find-file/1".format(daemon), json=improved_find_file_result)
    assert response.status_code == 201

    response = client.delete("/result/{}".format(daemon + "-test"))
    assert response.status_code == 202

def test_delete_results_plugin(client):
    """ Test delete all results for a specific plugin for a given daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    daemon = response.get_json()["daemon"]
    response = client.post("/result/{}/find-file/0".format(daemon), json=find_file_result)
    assert response.status_code == 201

    response = client.post("/result/{}/find-file/1".format(daemon), json=improved_find_file_result)
    assert response.status_code == 201

    response = client.post("/result/{}/scan-hosts-file/0".format(daemon), json=improved_find_file_result)
    assert response.status_code == 201

    response = client.delete("/result/{}/find-file".format(daemon))
    assert response.status_code == 202

    response = client.get("/result/{}/find-file".format(daemon))
    assert response.status_code == 404

    response = client.get("/result/{}/scan-hosts-file".format(daemon))
    assert response.status_code == 200

def test_delete_results_plugin_index(client):
    """ Test delete the results at a specific index for a specific plugin for a given daemon. """
    response = client.post("/trident/connect", json=tired_panda)
    assert response.status_code == 201

    daemon = response.get_json()["daemon"]
    response = client.post("/result/{}/find-file/0".format(daemon), json=find_file_result)
    assert response.status_code == 201

    response = client.post("/result/{}/find-file/1".format(daemon), json=improved_find_file_result)
    assert response.status_code == 201

    response = client.delete("/result/{}/find-file/0".format(daemon))
    assert response.status_code == 202

    response = client.get("/result/{}/find-file/0".format(daemon))
    assert response.status_code == 404

    response = client.get("/result/{}/find-file/1".format(daemon))
    assert response.status_code == 200
