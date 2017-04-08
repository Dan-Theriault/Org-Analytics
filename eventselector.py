"""Methods for generating event-selecting queries.

results are fed to methods in analyses.py by the program orchestrator
"""
from datetime import datetime


def query_from_name(event_name):
    """Use to select all events sharing a  name."""
    return ('SELECT * FROM events WHERE name=?', [event_name])


def query_from_date(event_date):
    """Use to select all events on a single date."""
    if isinstance(event_date, datetime.date):
        raise TypeError('event_date must be of type datetime.date')
    return ('SELECT * FROM events WHERE date(time) = date(?)', [event_date.isoformat()])


def query_from_full_key(event_name, event_date):
    """Use to select a single event."""
    if not isinstance(event_date, datetime.date):
        raise TypeError('event_date must be of type datetime.date')
    return ('SELECT * FROM events WHERE name=? AND date(time) = date(?)',
            [event_name, event_date.isoformat()])


def query_from_date_range(start_date, end_date):
    """Use to select all events in a date range."""
    if not isinstance(start_date, datetime.date):
        raise TypeError('start_date must be of type datetime.date')
    if not isinstance(end_date, datetime.date):
        raise TypeError('end_date must be of type datetime.date')

    return ('SELECT * FROM events WHERE date(time) BETWEEN ? AND ?',
            [start_date.isoformat(), end_date.isoformat()])


def query_from_name_and_date_range(name, start_date, end_date):
    """Use to select all events sharing a name in a date range."""
    if not isinstance(start_date, datetime.date):
        raise TypeError('start_date must be of type datetime.date')
    if not isinstance(end_date, datetime.date):
        raise TypeError('end_date must be of type datetime.date')

    return ('SELECT * FROM events WHERE name=? AND date(time) BETWEEN ? AND ?',
            [name, start_date.isoformat(), end_date.isoformat()])
