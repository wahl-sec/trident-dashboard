#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Trident: Handler Module.
Handles all logic and interaction with the database.

@author: Jacob Wahlman
"""

from functools import wraps
from inspect import signature

from flask import make_response, jsonify, current_app
from sqlalchemy.exc import OperationalError

from trident.database.models import *


def retrieve_record(tablename, **kwargs):
    """ Given a tablename query the table given the kwargs provided into that table. """
    if tablename not in globals():
        raise AttributeError(f"Table: '{tablename}' does not exist")

    table = globals()[tablename]
    try:
        return table.query.filter_by(**kwargs)
    except Exception as e:
        current_app.logger.exception(f"Failed to retrieve record(s) from the database table: '{tablename}'")
        raise e

def insert_record(tablename, **kwargs):
    """ Given a tablename insert all the kwargs provided into that table. """
    if tablename not in globals():
        raise AttributeError(f"Table: '{tablename}' does not exist")

    table = globals()[tablename]
    try:
        database.session.add(table(**kwargs))
        database.session.commit()
    except Exception as e:
        database.session.rollback()
        current_app.logger.exception(f"Failed to store record in database table: '{tablename}'")
        raise e

def delete_record(tablename, **kwargs):
    """ Given a tablename delete the record that matches the kwargs provided. """
    if tablename not in globals():
        raise AttributeError(f"Table: '{tablename}' does not exist")

    table = globals()[tablename]
    try:
        records = retrieve_record(tablename=tablename, **kwargs).all()
        for record in records:
            database.session.delete(record)
        database.session.commit()
    except Exception as e:
        database.session.rollback()
        current_app.logger.exception(f"Failed to delete record from database table: '{tablename}'")
        raise e
    
def retrieve_decorator(func, tablename):
    """ Used by 'GET' endpoints to retrieve records from the backend database tables.
    If any errors occur then the decorator will return '500'
    If the query did not result in any records then the decorator will return '404'
    If the query is successful then the decorator will return '200' 
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            records = retrieve_record(tablename=tablename, **kwargs).all()
        except Exception as e:
            current_app.logger.exception(f"Failed to fetch the records for table: '{tablename}' with parameters: '{kwargs}'")
            return make_response("Internal Server Error", 500)

        if not records:
            current_app.logger.error(f"No records for table: '{tablename}' with parameters: '{kwargs}'")
            return make_response("Not Found", 404)

        try:
            f_records = jsonify([record.serialize for record in records])
        except Exception as e:
            current_app.logger.exception(f"Failed to format the records for table: '{tablename}' with parameters: '{kwargs}' as JSON")
            return make_response("Internal Server Error", 500)

        return make_response(f_records, 200)

    return decorator

def insert_decorator(func, tablename):
    """ Used by 'POST' endpoints to insert records to the backend database tables.
    If any errors occur then the decorator will return '500'
    If the request lacks required parameters then the decorator will return '400' 
    If the query is successful then the decorator will return '201'
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            if data is None:
                insert_record(tablename=tablename, **kwargs)
            else:
                insert_record(tablename=tablename, **data)
        except OperationalError as e:
            current_app.logger.exception(f"Operational occured when inserting record into the table: '{tablename}' with parameters: '{kwargs}'")
            return make_response("Bad Request", 400)
        except Exception as e:
            current_app.logger.exception(f"Failed to insert record into the table: '{tablename}' with parameters: '{kwargs}'")
            return make_response("Internal Server Error", 500)

        return make_response("", 201)

    return decorator

def delete_decorator(func, tablename):
    """ Used by 'DELETE' endpoints to delete records from the backend database tables.
    If any errors occur then the decorator will return '500'
    If the query is successful then the decorator will return '202'
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            delete_record(tablename=tablename, **kwargs)
        except OperationalError as e:
            current_app.logger.exception(f"Operational occured when deleteing record from the table: '{tablename}' with parameters: '{kwargs}'")
            return make_response("Bad Request", 400)
        except Exception as e:
            current_app.logger.exception(f"Failed to delete record from the table: '{tablename}' with parameters: '{kwargs}'")
            return make_response("Internal Server Error", 500)

        return make_response("", 202)

    return decorator
