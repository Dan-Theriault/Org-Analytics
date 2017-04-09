"""High-level methods controlling the generation of reports.

Interfaces with analyses, eventselector, plotter, texgenerator, gui, cli- basically everything.
"""
import loader
import analyses
import eventselector
import plotter

import sqlite3
from datetime import datetime


def standard_report(names=[], dates=[], daterange=(), include_emails=False, keep_tex=False):
    """Generate a standard report on a single group of events.

    Takes in a list of names, a list of dates, and a 2-tuple containing a start and end date.
    """
    conn = sqlite3.connect(loader.DB)
    cur = conn.cursor()
    events_query, query_vars = eventselector.build_query(names, dates, daterange)
    cur.execute(events_query, query_vars)
    events_list = cur.fetchall()

    tex_vars = {}

    arrival_times = analyses.get_arrival_deltas(events_list)
    plotter.arrival_chart(arrival_times, 'arrival_times.png')

    distinct_attend = analyses.count_attendees(events_list, distinct_only=True)

    total_attend = analyses.count_attendees(events_list)

    attend_average = analyses.count_attendees(events_list, average_attendance=True)

    event_average = analyses.count_attendees(events_list, average_events=True)

    if include_emails:
        email_list = analyses.list_emails(events_list)

    events_attendance = {}
    for event in events_list:
        event_time = datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S')
        event_str = event[0] + ' ' + event_time.date().isoformat()
        events_attendance[event_str] = analyses.count_attendees([event])
    if len(events_attendance) == 1:
        plotter.pie_chart(events_attendance, 'attendance.png')
    else:
        plotter.bar_chart(events_attendance, 'attendance.png')

    conn.close()


def comparison_report(events_data_a, events_data_b, include_emails=False, keep_tex=False):
    """Compare two groups of events.

    events_data_* variables should be 3-tuples of format (names, dates, daterange).
    see docstring on standard_report for further information on these three variables.
    """
    conn = sqlite3.connect(loader.DB)
    cur = conn.cursor()

    events_query = eventselector.build_query(*events_data_a)
    cur.execute(*events_query)
    events_list_a = cur.fetchall()

    events_query = eventselector.build_query(*events_data_b)
    cur.execute(*events_query)
    events_list_b = cur.fetchall()

    distinct_attendees_a = analyses.count_attendees(events_list_a, distinct_only=True)
    distinct_attendees_b = analyses.count_attendees(events_list_b, distinct_only=True)

    total_attendance_a = analyses.count_attendees(events_list_a)
    total_attendance_b = analyses.count_attendees(events_list_b)

    average_attendance_a = analyses.count_attendees(events_list_a, average_attendance=True)
    average_attendance_b = analyses.count_attendees(events_list_b, average_attendance=True)

    average_attended_a = analyses.count_attendees(events_list_a, average_events=True)
    average_attended_b = analyses.count_attendees(events_list_b, average_events=True)

    if include_emails:
        email_list_a = analyses.list_emails(events_list_a)
        email_list_b = analyses.list_emails(events_list_b)

    attends_only_a, attends_only_b = *(analyses.compare_attendees(events_list_a, events_list_b))

    events_attendance = {}
    for event in events_list_a:
        event_time = datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S')
        event_str = event[0] + ' ' + event_time.date().isoformat()
        events_attendance[event_str] = analyses.count_attendees([event])
    for event in events_list_b:
        event_time = datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S')
        event_str = event[0] + ' ' + event_time.date().isoformat()
        events_attendance[event_str] = analyses.count_attendees([event])
    plotter.bar_chart(events_attendance, 'attendance.png')

    conn.close()


def calendar_report(names, daterange, compare_range=(), include_emails=False, keep_tex=False):
    """Present events in a calendar / timeline format."""
    conn = sqlite3.connect(loader.DB)
    cur = conn.cursor()
    events_query, query_vars = eventselector.build_query(names, [], daterange)
    cur.execute(events_query, query_vars)
    events_list = cur.fetchall()
    
    distinct_attend = analyses.count_attendees(events_list, distinct_only=True)

    total_attend = analyses.count_attendees(events_list)

    attend_average = analyses.count_attendees(events_list, average_attendance=True)

    event_average = analyses.count_attendees(events_list, average_events=True)

    if compare_range != ():
        events_query, query_vars = eventselector.build_query(names, [], compare_range)
        cur.execute(events_query, query_vars)
        comparison_list = cur.fetchall()
        new, lost = *(analyses.compare_attendees(events_list, comparison_list))

    if include_emails:
        email_list = analyses.list_emails(events_list)

    events_attendance = {}
    for event in events_list:
        event_time = datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S')
        event_str = event[0] + ' ' + event_time.date().isoformat()
        events_attendance[event_str] = analyses.count_attendees([event])

    conn.close()
