"""Methods for generating event-selecting queries.

results are fed to methods in analyses.py by the program orchestrator
"""
from datetime import datetime


def query_from_name(name):
    """Use to select events by name."""
    return ('SELECT * FROM events WHERE name=?', [name])


def query_from_date(event_date):
    """Use to select events on a single date."""
    if isinstance(event_date, datetime.date):
        raise TypeError('event_date must be of type datetime.date')
    return ('SELECT * FROM events WHERE date(time) = date(?)', [event_date.isoformat()])
