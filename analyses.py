import datetime
from monthdelta import monthdelta
import sqlite3


def get_arrival_times(events_list):
    """Return a list of arrival times (as deltas vs start time)."""
    arrival_times = []
    for event in events_list:
        pass
    return arrival_times


def get_attendee_counts(events_list):
    """Return a list of dictionaries of arrival times."""
    attendee_counts = [{'All': 0,
                        'Nonmembers': 0,
                        'Members': 0,
                        'Volunteers': 0,
                        'Board': 0}]
    for event in events_list:
        pass
    if len(attendee_counts) == 2:
        attendee_counts = [attendee_counts[0]]
    return attendee_counts


def get_attendee_stats(events_list, drop_cutoff):
    """Compute and return statistics about event attendance."""
    pass
