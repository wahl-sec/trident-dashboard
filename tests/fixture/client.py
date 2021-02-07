#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Trident: Test Fixture Module.
Contains all the fixtures for all the tests.

@author: Jacob Wahlman
"""

import pytest

from os import close, unlink
from tempfile import mkstemp

from trident import create_app
from trident.database.models import database

tired_panda = {
    "host_addr": "192.168.1.1",
    "worker_count": 5,
    "arguments": {
        "logging_level": "DEBUG",
        "plugins": {
            "find-file": {
                "path": "plugins.find_file",
                "plugin_args": {
                    "files": ["file1.html", "file2.css"]
                },
                "args": {
                    "store": {
                        "path": "stores"
                    }
                }
            },
            "scan-hosts-file": {
                "path": "plugins.scan_file"
            }
        }
    }
}

round_giraffe = {
    "host_addr": "192.168.1.2",
    "worker_count": 2,
    "arguments": {
        "logging_level": "INFO",
        "plugins": {
            "improved-find-file": {
                "path": "plugins.improved_find_file",
                "plugin_args": {
                    "files": ["file1.html", "file2.css"]
                },
                "args": {
                    "store": {
                        "path": "stores"
                    }
                }
            }
        }
    }
}

cool_kitten = {
    "worker_count": 2,
    "arguments": {
        "logging_level": "INFO",
        "plugins": {
            "improved-find-file": {
                "path": "plugins.improved_find_file",
                "plugin_args": {
                    "files": ["file1.html", "file2.css"]
                },
                "args": {
                    "store": {
                        "path": "stores"
                    }
                }
            }
        }
    }
}

find_file_result = {
    "result": {
        0: None,
        1: None,
        2: "file2.html"
    }
}

improved_find_file_result = {
    "result": {
        0: None,
        1: "file1.html",
        2: "file2.html"
    }
}

@pytest.fixture
def client():
    database, path = mkstemp()
    return create_app({
        "TESTING": True,
        "DATABASE": path
    }).test_client()