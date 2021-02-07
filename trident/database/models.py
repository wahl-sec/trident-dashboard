#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Trident: Database Models Module.
Database models for Trident dashboard.

@author: Jacob Wahlman
"""

from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class Daemon(database.Model):
    """ Database model for Trident Daemons. """
    __tablename__ = "daemon"

    daemon = database.Column(database.String(20), primary_key=True)
    host_addr = database.Column(database.String(15), nullable=False)
    worker_count = database.Column(database.Integer, nullable=False)
    arguments = database.Column(database.JSON)

    daemon_plugin_rel = database.relationship("Plugin", backref="plugin_daemon", lazy=True)
    daemon_result_rel = database.relationship("Result", backref="result_daemon", lazy=True)

    def __repr__(self):
        return f"{self.daemon}@{self.host_addr}"
    
    @property
    def serialize(self):
        """ Return a serialized Daemon instance.
        If it is not serializable then a ValueError is raised.
        If it is serializable then the returned value is a dictionary.
        """
        try:
            return {
                "daemon": self.daemon,
                "host_addr": self.host_addr,
                "worker_count": self.worker_count,
                "arguments": self.arguments
            }
        except Exception as e:
            raise ValueError(f"Failed to serialize 'Daemon' model instance.")


class ConnectedDaemon(database.Model):
    """ Database model for connected Trident Daemons. """
    __tablename__ = "connected_daemons"

    daemon = database.Column(database.String(20), database.ForeignKey("daemon.daemon"), primary_key=True)

    def __repr__(self):
        return f"{self.daemon.daemon}@{self.daemon.host_addr}"

    @property
    def serialize(self):
        """ Return a serialized ConnectedDaemon instance.
        If it is not serializable then a ValueError is raised.
        If it is serializable then the returned value is a dictionary.
        """
        try:
            return {
                "daemon": self.daemon
            }
        except Exception as e:
            raise ValueError(f"Failed to serialize 'ConnectedDaemon' model instance.")


class Plugin(database.Model):
    """ Database model for Trident Plugins. """
    __tablename__ = "plugin"

    plugin = database.Column(database.Integer, primary_key=True)
    plugin_name = database.Column(database.String(20), nullable=False)
    arguments = database.Column(database.JSON)
    daemon = database.Column(database.String(20), database.ForeignKey("daemon.daemon"))

    plugin_result_rel = database.relationship("Result", backref="result_plugin", lazy=True)

    def __repr__(self):
        return f"({self.plugin}) {self.plugin_name}@{self.daemon}"

    @property
    def serialize(self):
        """ Return a serialized Plugin instance.
        If it is not serializable then a ValueError is raised.
        If it is serializable then the returned value is a dictionary.
        """
        try:
            return {
                "plugin": self.plugin,
                "plugin_name": self.plugin_name,
                "arguments": self.arguments,
                "daemon": self.daemon
            }
        except Exception as e:
            raise ValueError(f"Failed to serialize 'Plugin' model instance.")


class Result(database.Model):
    """ Database model for Trident Results. """
    __tablename__ = "result"

    index = database.Column(database.Integer, primary_key=True)
    plugin_name = database.Column(database.String(20), database.ForeignKey("plugin.plugin_name"), primary_key=True)
    result = database.Column(database.JSON, nullable=False)
    daemon = database.Column(database.String(20), database.ForeignKey("daemon.daemon"), nullable=False)

    def __repr__(self):
        return f"({self.index}) {self.plugin_name}@{self.daemon}"

    @property
    def serialize(self):
        """ Return a serialized Result instance.
        If it is not serializable then a ValueError is raised.
        If it is serializable then the returned value is a dictionary.
        """
        try:
            return {
                "index": self.index,
                "result": self.result,
                "plugin": self.plugin_name,
                "daemon": self.daemon
            }
        except Exception as e:
            raise ValueError(f"Failed to serialize 'Plugin' model instance.")

    def insert_result(self, index, value):
        """ Insert a value in the result dictionary. """
        self.result[index] = value
