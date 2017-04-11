"""High-level methods controlling the generation of reports.

Interfaces with analyses, eventselector, plotter, texgenerator, gui, cli- basically everything.
"""
import loader
import analyses
import eventselector
import plotter
import texvar

import sqlite3
from datetime import datetime


def standard_report(names=[], dates=[], daterange=(), include_emails=False):
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
    tex_vars['arrival_chart'] = './.working/arrival_times.png'

    distinct_attend = analyses.count_attendees(events_list, distinct_only=True)
    tex_vars['distinct_all'] = distinct_attend['All']
    tex_vars['distinct_board'] = distinct_attend['Board']
    tex_vars['distinct_volunteers'] = distinct_attend['Volunteers']
    tex_vars['distinct_members'] = distinct_attend['Members']
    tex_vars['distinct_nonmembers'] = distinct_attend['Nonmembers']

    total_attend = analyses.count_attendees(events_list)
    tex_vars['total_all'] = total_attend['All']
    tex_vars['total_board'] = total_attend['Board']
    tex_vars['total_volunteers'] = total_attend['Volunteers']
    tex_vars['total_members'] = total_attend['Members']
    tex_vars['total_nonmembers'] = total_attend['Nonmembers']

    average_attend = analyses.count_attendees(events_list, average_attendance=True)
    tex_vars['average_all'] = average_attend['All']
    tex_vars['average_board'] = average_attend['Board']
    tex_vars['average_volunteers'] = average_attend['Volunteers']
    tex_vars['average_members'] = average_attend['Members']
    tex_vars['average_nonmembers'] = average_attend['Nonmembers']

    event_attend = analyses.count_attendees(events_list, average_events=True)
    tex_vars['event_all'] = event_attend['All']
    tex_vars['event_board'] = event_attend['Board']
    tex_vars['event_volunteers'] = event_attend['Volunteers']
    tex_vars['event_members'] = event_attend['Members']
    tex_vars['event_nonmembers'] = event_attend['Nonmembers']

    if include_emails:
        tex_vars['include_emails'] = ''

        tex_vars['email_board'] = ''
        tex_vars['email_volunteers'] = ''
        tex_vars['email_members'] = ''
        tex_vars['email_nonmembers'] = ''

        email_list = analyses.list_emails(events_list)
        for email in email_list['Board']:
            tex_vars['email_board'] += email + '\n'
        for email in email_list['Volunteers']:
            tex_vars['email_volunteers'] += email + '\n'
        for email in email_list['Members']:
            tex_vars['email_members'] += email + '\n'
        for email in email_list['Nonmembers']:
            tex_vars['email_nonmembers'] += email + '\n'

    events_attendance = {}
    for event in events_list:
        event_time = datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S')
        event_str = event[0] + ' ' + event_time.date().isoformat()
        events_attendance[event_str] = analyses.count_attendees([event])
    plotter.bar_chart(events_attendance, 'attendance.png')
    tex_vars['attendance_chart'] = './.working/attendance.png'

    texvar.write_tex_vars(tex_vars)
    conn.close()


def comparison_report(events_data_a, events_data_b, include_emails=False):
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

    tex_vars = {}

    # Create dictionary entries for numbers of distinct attendees
    distinct_attend_a = analyses.count_attendees(events_list_a, distinct_only=True)
    tex_vars['distinct_a_all'] = distinct_attend_a['All']
    tex_vars['distinct_a_board'] = distinct_attend_a['Board']
    tex_vars['distinct_a_volunteers'] = distinct_attend_a['Volunteers']
    tex_vars['distinct_a_members'] = distinct_attend_a['Members']
    tex_vars['distinct_a_nonmembers'] = distinct_attend_a['Nonmembers']
    distinct_attend_b = analyses.count_attendees(events_list_b, distinct_only=True)
    tex_vars['distinct_b_all'] = distinct_attend_b['All']
    tex_vars['distinct_b_board'] = distinct_attend_b['Board']
    tex_vars['distinct_b_volunteers'] = distinct_attend_b['Volunteers']
    tex_vars['distinct_b_members'] = distinct_attend_b['Members']
    tex_vars['distinct_b_nonmembers'] = distinct_attend_b['Nonmembers']

    # Create dictionary entries for total numbers of attendees
    total_attend_a = analyses.count_attendees(events_list_a)
    tex_vars['total_a_all'] = total_attend_a['All']
    tex_vars['total_a_board'] = total_attend_a['Board']
    tex_vars['total_a_volunteers'] = total_attend_a['Volunteers']
    tex_vars['total_a_members'] = total_attend_a['Members']
    tex_vars['total_a_nonmembers'] = total_attend_a['Nonmembers']
    total_attend_b = analyses.count_attendees(events_list_b)
    tex_vars['total_b_all'] = total_attend_b['All']
    tex_vars['total_b_board'] = total_attend_b['Board']
    tex_vars['total_b_volunteers'] = total_attend_b['Volunteers']
    tex_vars['total_b_members'] = total_attend_b['Members']
    tex_vars['total_b_nonmembers'] = total_attend_b['Nonmembers']

    # Create dictionary entries for average number of attendees per event
    average_attend_a = analyses.count_attendees(events_list_a, average_attendance=True)
    tex_vars['average_a_all'] = average_attend_a['All']
    tex_vars['average_a_board'] = average_attend_a['Board']
    tex_vars['average_a_volunteers'] = average_attend_a['Volunteers']
    tex_vars['average_a_members'] = average_attend_a['Members']
    tex_vars['average_a_nonmembers'] = average_attend_a['Nonmembers']
    average_attend_b = analyses.count_attendees(events_list_b, average_attendance=True)
    tex_vars['average_b_all'] = average_attend_b['All']
    tex_vars['average_b_board'] = average_attend_b['Board']
    tex_vars['average_b_volunteers'] = average_attend_b['Volunteers']
    tex_vars['average_b_members'] = average_attend_b['Members']
    tex_vars['average_b_nonmembers'] = average_attend_b['Nonmembers']

    # Create dictionary entries for the average number of events an attendee has attended
    event_attend_a = analyses.count_attendees(events_list_a, average_events=True)
    tex_vars['event_a_all'] = event_attend_a['All']
    tex_vars['event_a_board'] = event_attend_a['Board']
    tex_vars['event_a_volunteers'] = event_attend_a['Volunteers']
    tex_vars['event_a_members'] = event_attend_a['Members']
    tex_vars['event_a_nonmembers'] = event_attend_a['Nonmembers']
    event_attend_b = analyses.count_attendees(events_list_b, average_events=True)
    tex_vars['event_b_all'] = event_attend_b['All']
    tex_vars['event_b_board'] = event_attend_b['Board']
    tex_vars['event_b_volunteers'] = event_attend_b['Volunteers']
    tex_vars['event_b_members'] = event_attend_b['Members']
    tex_vars['event_b_nonmembers'] = event_attend_b['Nonmembers']

    # Compare the overlap / lack thereof of the attendee groups
    comparison = analyses.compare_attendees(events_list_a, events_list_b)
    attends_both = comparison['a_and_b']
    attends_only_a = comparison['a_not_b']
    attends_only_b = comparison['b_not_a']

    tex_vars['all_both'] = len(attends_both['All'])
    tex_vars['board_both'] = len(attends_both['Board'])
    tex_vars['volunteers_both'] = len(attends_both['Volunteers'])
    tex_vars['members_both'] = len(attends_both['Members'])
    tex_vars['nonmembers_both'] = len(attends_both['Nonmembers'])

    tex_vars['all_only_a'] = len(attends_only_a['All'])
    tex_vars['board_only_a'] = len(attends_only_a['Board'])
    tex_vars['volunteers_only_a'] = len(attends_only_a['Volunteers'])
    tex_vars['members_only_a'] = len(attends_only_a['Members'])
    tex_vars['nonmembers_only_a'] = len(attends_only_a['Nonmembers'])

    tex_vars['all_only_b'] = len(attends_only_b['All'])
    tex_vars['board_only_b'] = len(attends_only_b['Board'])
    tex_vars['volunteers_only_b'] = len(attends_only_b['Volunteers'])
    tex_vars['members_only_b'] = len(attends_only_b['Members'])
    tex_vars['nonmembers_only_b'] = len(attends_only_b['Nonmembers'])

    # optionally, generate email lists
    if include_emails:
        tex_vars['include_emails'] = ''

        tex_vars['email_board_both'] = ''
        tex_vars['email_volunteers_both'] = ''
        tex_vars['email_members_both'] = ''
        tex_vars['email_nonmembers_both'] = ''
        tex_vars['email_board_only_a'] = ''
        tex_vars['email_volunteers_only_a'] = ''
        tex_vars['email_members_only_a'] = ''
        tex_vars['email_nonmembers_only_a'] = ''
        tex_vars['email_board_only_b'] = ''
        tex_vars['email_volunteers_only_b'] = ''
        tex_vars['email_members_only_b'] = ''
        tex_vars['email_nonmembers_only_b'] = ''

        for email in attends_both['Board']:
            tex_vars['email_board_both'] += email + '\n'
        for email in attends_both['Volunteers']:
            tex_vars['email_volunteers_both'] += email + '\n'
        for email in attends_both['Members']:
            tex_vars['email_members_both'] += email + '\n'
        for email in attends_both['Nonmembers']:
            tex_vars['email_nonmembers_both'] += email + '\n'
        for email in attends_only_a['Board']:
            tex_vars['email_board_only_a'] += email + '\n'
        for email in attends_only_a['Volunteers']:
            tex_vars['email_volunteers_only_a'] += email + '\n'
        for email in attends_only_a['Members']:
            tex_vars['email_members_only_a'] += email + '\n'
        for email in attends_only_a['Nonmembers']:
            tex_vars['email_nonmembers_only_a'] += email + '\n'
        for email in attends_only_b['Board']:
            tex_vars['email_board_only_b'] += email + '\n'
        for email in attends_only_b['Volunteers']:
            tex_vars['email_volunteers_only_b'] += email + '\n'
        for email in attends_only_b['Members']:
            tex_vars['email_members_only_b'] += email + '\n'
        for email in attends_only_b['Nonmembers']:
            tex_vars['email_nonmembers_only_b'] += email + '\n'

    events_attendance_a = {}
    events_attendance_b = {}
    for event in events_list_a:
        event_time = datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S')
        event_str = event[0] + ' ' + event_time.date().isoformat()
        events_attendance_a[event_str] = analyses.count_attendees([event])
    for event in events_list_b:
        event_time = datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S')
        event_str = event[0] + ' ' + event_time.date().isoformat()
        events_attendance_b[event_str] = analyses.count_attendees([event])
    plotter.bar_chart(events_attendance_a, 'attendance_a.png')
    plotter.bar_chart(events_attendance_b, 'attendance_b.png')
    tex_vars['attendance_chart'] = './.working/attendance_a.png'
    tex_vars['attendance_chart'] = './.working/attendance_b.png'

    texvar.write_tex_vars(tex_vars)
    conn.close()
