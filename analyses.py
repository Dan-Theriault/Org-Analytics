"""Basic units of analysis; methods to query database and return usable data sets."""
from datetime import datetime
# from monthdelta import monthdelta
import sqlite3
import loader


def get_arrival_times(events_query, query_vars):
    """Return a list of arrival times (as deltas vs start time).

    event_query should return a full tuple from events of format (name, time)
    """
    conn = sqlite3.connect(loader.DB)
    cur = conn.cursor()
    cur.execute(events_query, query_vars)
    events_list = cur.fetchall()

    arrival_times = []
    for event in events_list:
        cur.execute('SELECT checkin_time FROM records WHERE event_name=? AND event_time=?',
                    list(event))
        checkins = [t[0] for t in cur.fetchall() if t[0] != 'Manual']

        for checkin in checkins:
            arrival_datetime = datetime.strptime(checkin, '%Y-%m-%d  %I:%M %p')
            event_datetime = datetime.strptime(event[1], '%Y-%m-%d  %I:%M %p')
            arrival_delta = arrival_datetime - event_datetime
            arrival_times.append(arrival_delta.total_seconds() / 60)

    conn.close()
    return arrival_times


def get_attendee_counts(events_query, query_vars=[], distinct_only=False):
    """Return a list of dictionaries of arrival times."""
    conn = sqlite3.connect(loader.DB)
    cur = conn.cursor()
    cur.execute(events_query, query_vars)
    events_list = cur.fetchall()

    attendee_counts = {'All': 0,
                       'Nonmembers': 0,
                       'Members': 0,
                       'Volunteers': 0,
                       'Board': 0}

    attendees = []

    for event in events_list:
        cur.execute('SELECT student_email FROM records ' +
                    'WHERE event_name=? AND event_time=?',
                    list(event))
        attendees += cur.fetchall()

    if distinct_only:
        attendees = list(set(attendees))

    for attendee in attendees:
        cur.execute('SELECT is_member,is_volunteer,is_board FROM students WHERE email=?',
                    attendee)
        attendee_group = cur.fetchone()

        attendee_counts['All'] += 1

        if attendee_group[2]:
            attendee_counts['Board'] += 1
        elif attendee_group[1]:
            attendee_counts['Volunteers'] += 1
        elif attendee_group[0]:
            attendee_counts['Members'] += 1
        else:
            attendee_counts['Nonmembers'] += 1

    conn.close()
    return attendee_counts


def get_email_list(events_query, query_vars=[]):
    """Return a list of dictionaries of arrival times."""
    conn = sqlite3.connect(loader.DB)
    cur = conn.cursor()
    cur.execute(events_query, query_vars)
    events_list = cur.fetchall()

    email_lists = {'All': [],
                   'Nonmembers': [],
                   'Members': [],
                   'Volunteers': [],
                   'Board': []}
    attendees = []

    for event in events_list:
        cur.execute('SELECT student_email FROM records ' +
                    'WHERE event_name=? AND event_time=?',
                    list(event))
        attendees += cur.fetchall()

    attendees = list(set(attendees))  # ensure all elements of attendees are distinct

    for attendee in attendees:
        cur.execute('SELECT is_member,is_volunteer,is_board FROM students WHERE email=?',
                    attendee)
        attendee_group = cur.fetchone()

        email_lists['All'].append(attendee[0])

        if attendee_group[2]:
            email_lists['Board'].append(attendee[0])
        elif attendee_group[1]:
            email_lists['Volunteers'].append(attendee[0])
        elif attendee_group[0]:
            email_lists['Members'].append(attendee[0])
        else:
            email_lists['Nonmembers'].append(attendee[0])

    conn.close()
    return email_lists


def get_attendee_stats(events_query, query_vars=[]):
    """Compute and return statistics about event attendance."""
    conn = sqlite3.connect(loader.DB)
    cur = conn.cursor()
    cur.execute(events_query, query_vars)
    events_list = cur.fetchall()

    for event in events_list:
        cur.execute('SELECT student_email FROM records ' +
                    'WHERE event_name=? AND event_time=?',
                    list(event))

    conn.close()
    return
