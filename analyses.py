"""Basic units of analysis; methods to query database and return usable data sets."""
from datetime import datetime
# from monthdelta import monthdelta
import sqlite3
import loader


def get_arrival_deltas(events_list):
    """Return a list of arrival times (as deltas vs start time).

    event_query should return a full tuple from events of format (name, time)
    """
    conn = sqlite3.connect(loader.DB)
    cur = conn.cursor()

    arrival_times = []
    for event in events_list:
        cur.execute('SELECT checkin_time FROM records WHERE event_name=? AND event_time=?',
                    list(event))
        checkins = [t[0] for t in cur.fetchall() if t[0] != 'Manual']

        for checkin in checkins:
            arrival_datetime = datetime.strptime(checkin, '%Y-%m-%d  %H:%M')
            event_datetime = datetime.strptime(event[1], '%Y-%m-%d  %H:%M')
            arrival_delta = arrival_datetime - event_datetime
            arrival_times.append(arrival_delta.total_seconds() / 60)

    conn.close()
    return arrival_times


def count_attendees(events_list,
                    distinct_only=False,  # return the number of distinct attendees
                    average_attendance=False,  # return avg number of attendees
                    average_events=False):  # return avg number of events attended
    """Return a list of dictionaries of arrival times."""
    conn = sqlite3.connect(loader.DB)
    cur = conn.cursor()

    if ((distinct_only and (average_attendance or average_events)) or
            (average_attendance and average_events)):
        raise ValueError('Incompatible options selected')

    if average_events:
        attendee_distinct = count_attendees(events_list, distinct_only=True)

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

    if average_attendance:
        for field in attendee_counts:
            attendee_counts[field] = attendee_counts[field] / len(events_list)

    if average_events:
        for field in attendee_counts:
            attendee_counts[field] = attendee_counts[field] / attendee_distinct[field]

    conn.close()
    return attendee_counts


def list_emails(events_list):
    """Return a list of dictionaries of arrival times."""
    conn = sqlite3.connect(loader.DB)
    cur = conn.cursor()

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


def compare_attendees(events_list_a, events_list_b):
    """Compute and return statistics about event attendance."""
    conn = sqlite3.connect(loader.DB)
    cur = conn.cursor()

    attendees_a = []
    for event in events_list_a:
        cur.execute('SELECT student_email FROM records ' +
                    'WHERE event_name=? AND event_time=?',
                    list(event))
        events_list_a += cur.fetchall()
    attendees_a = list(set(attendees_a))

    attendees_b = []
    for event in events_list_b:
        cur.execute('SELECT student_email FROM records ' +
                    'WHERE event_name=? AND event_time=?',
                    list(event))
        events_list_b += cur.fetchall()
    attendees_b = list(set(attendees_b))

    a_not_b = [attendee for attendee in attendees_a if attendee not in attendees_b]
    b_not_a = [attendee for attendee in attendees_b if attendee not in attendees_a]

    conn.close()
    return (a_not_b, b_not_a)
