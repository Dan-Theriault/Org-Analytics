"""High-level methods controlling the generation of reports.

Interfaces with analyses, eventselector, plotter, texgenerator, gui, cli- basically everything.
"""
import loader
import analyses
import eventselector
import plotter
import texvar

import sqlite3
import subprocess
from datetime import datetime
import os


def standard_report(names=[], dates=[], daterange=(), include_emails=False, verbose=False):
    """Generate a standard report on a single group of events.

    Takes in a list of names, a list of dates, and a 2-tuple containing a start and end date.
    """
    conn = sqlite3.connect(loader.DB)
    cur = conn.cursor()
    events_query, query_vars = eventselector.build_query(names, dates, daterange)
    cur.execute(events_query, query_vars)
    events_list = cur.fetchall()

    tex_vars = {}

    tex_vars['groupname'] = eventselector.name_group(names, dates, daterange)

    arrival_times = analyses.get_arrival_deltas(events_list)
    plotter.arrival_chart(arrival_times, 'arrival_times.png')
    tex_vars['arrivalchart'] = './.working/arrival_times.png'

    distinct_attend = analyses.count_attendees(events_list, distinct_only=True)
    tex_vars['distinctall'] = distinct_attend['All']
    tex_vars['distinctboard'] = distinct_attend['Board']
    tex_vars['distinctvolunteers'] = distinct_attend['Volunteers']
    tex_vars['distinctmembers'] = distinct_attend['Members']
    tex_vars['distinctnonmembers'] = distinct_attend['Nonmembers']

    total_attend = analyses.count_attendees(events_list)
    tex_vars['totalall'] = total_attend['All']
    tex_vars['totalboard'] = total_attend['Board']
    tex_vars['totalvolunteers'] = total_attend['Volunteers']
    tex_vars['totalmembers'] = total_attend['Members']
    tex_vars['totalnonmembers'] = total_attend['Nonmembers']

    average_attend = analyses.count_attendees(events_list, average_attendance=True)
    tex_vars['averageall'] = average_attend['All']
    tex_vars['averageboard'] = average_attend['Board']
    tex_vars['averagevolunteers'] = average_attend['Volunteers']
    tex_vars['averagemembers'] = average_attend['Members']
    tex_vars['averagenonmembers'] = average_attend['Nonmembers']

    event_attend = analyses.count_attendees(events_list, average_events=True)
    tex_vars['eventall'] = event_attend['All']
    tex_vars['eventboard'] = event_attend['Board']
    tex_vars['eventvolunteers'] = event_attend['Volunteers']
    tex_vars['eventmembers'] = event_attend['Members']
    tex_vars['eventnonmembers'] = event_attend['Nonmembers']

    if include_emails:
        tex_vars['emailboard'] = ''
        tex_vars['emailvolunteers'] = ''
        tex_vars['emailmembers'] = ''
        tex_vars['emailnonmembers'] = ''

        email_list = analyses.list_emails(events_list)
        for email in email_list['Board']:
            tex_vars['emailboard'] += email + '\n'
        for email in email_list['Volunteers']:
            tex_vars['emailvolunteers'] += email + '\n'
        for email in email_list['Members']:
            tex_vars['emailmembers'] += email + '\n'
        for email in email_list['Nonmembers']:
            tex_vars['emailnonmembers'] += email + '\n'

    events_attendance = []
    events_list = sorted(events_list, key=lambda x: x[1])
    for event in events_list:
        event_time = datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S')
        event_str = event[0] + '\n' + event_time.date().isoformat()
        events_attendance.append((event_str, analyses.count_attendees([event])))

    events_attendance = [
        [e[0]] +
        [e[1]['Board']] +
        [e[1]['Volunteers']] +
        [e[1]['Members']] +
        [e[1]['Nonmembers']]
        for e in events_attendance
    ][::-1]  # reverse the resulting list

    plotter.bar_chart(events_attendance, 'attendance.png')
    tex_vars['attendancechart'] = './.working/attendance.png'

    texvar.write_tex_vars(tex_vars)
    subprocess.check_output('pdflatex -output-directory Reports Templates/standard.tex', shell=True)
    os.remove('./Reports/standard.aux')
    os.remove('./Reports/standard.log')
    conn.close()


def comparison_report(events_data_a, events_data_b, include_emails=False, verbose=False):
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
    tex_vars['groupnamea'] = eventselector.name_group(*events_data_a)
    tex_vars['groupnameb'] = eventselector.name_group(*events_data_b)

    # Create dictionary entries for numbers of distinct attendees
    distinct_attend_a = analyses.count_attendees(events_list_a, distinct_only=True)
    tex_vars['distinctall'] = distinct_attend_a['All']
    tex_vars['distinctaboard'] = distinct_attend_a['Board']
    tex_vars['distinctavolunteers'] = distinct_attend_a['Volunteers']
    tex_vars['distinctamembers'] = distinct_attend_a['Members']
    tex_vars['distinctanonmembers'] = distinct_attend_a['Nonmembers']
    distinct_attend_b = analyses.count_attendees(events_list_b, distinct_only=True)
    tex_vars['distinctball'] = distinct_attend_b['All']
    tex_vars['distinctbboard'] = distinct_attend_b['Board']
    tex_vars['distinctbvolunteers'] = distinct_attend_b['Volunteers']
    tex_vars['distinctbmembers'] = distinct_attend_b['Members']
    tex_vars['distinctbnonmembers'] = distinct_attend_b['Nonmembers']

    # Create dictionary entries for total numbers of attendees
    total_attend_a = analyses.count_attendees(events_list_a)
    tex_vars['totalaall'] = total_attend_a['All']
    tex_vars['totalaboard'] = total_attend_a['Board']
    tex_vars['totalavolunteers'] = total_attend_a['Volunteers']
    tex_vars['totalamembers'] = total_attend_a['Members']
    tex_vars['totalanonmembers'] = total_attend_a['Nonmembers']
    total_attend_b = analyses.count_attendees(events_list_b)
    tex_vars['totalball'] = total_attend_b['All']
    tex_vars['totalbboard'] = total_attend_b['Board']
    tex_vars['totalbvolunteers'] = total_attend_b['Volunteers']
    tex_vars['totalbmembers'] = total_attend_b['Members']
    tex_vars['totalbnonmembers'] = total_attend_b['Nonmembers']

    # Create dictionary entries for average number of attendees per event
    average_attend_a = analyses.count_attendees(events_list_a, average_attendance=True)
    tex_vars['averageaall'] = average_attend_a['All']
    tex_vars['averageaboard'] = average_attend_a['Board']
    tex_vars['averageavolunteers'] = average_attend_a['Volunteers']
    tex_vars['averageamembers'] = average_attend_a['Members']
    tex_vars['averageanonmembers'] = average_attend_a['Nonmembers']
    average_attend_b = analyses.count_attendees(events_list_b, average_attendance=True)
    tex_vars['averageball'] = average_attend_b['All']
    tex_vars['averagebboard'] = average_attend_b['Board']
    tex_vars['averagebvolunteers'] = average_attend_b['Volunteers']
    tex_vars['averagebmembers'] = average_attend_b['Members']
    tex_vars['averagebnonmembers'] = average_attend_b['Nonmembers']

    # Create dictionary entries for the average number of events an attendee has attended
    event_attend_a = analyses.count_attendees(events_list_a, average_events=True)
    tex_vars['eventaall'] = event_attend_a['All']
    tex_vars['eventaboard'] = event_attend_a['Board']
    tex_vars['eventavolunteers'] = event_attend_a['Volunteers']
    tex_vars['eventamembers'] = event_attend_a['Members']
    tex_vars['eventanonmembers'] = event_attend_a['Nonmembers']
    event_attend_b = analyses.count_attendees(events_list_b, average_events=True)
    tex_vars['eventball'] = event_attend_b['All']
    tex_vars['eventbboard'] = event_attend_b['Board']
    tex_vars['eventbvolunteers'] = event_attend_b['Volunteers']
    tex_vars['eventbmembers'] = event_attend_b['Members']
    tex_vars['eventbnonmembers'] = event_attend_b['Nonmembers']

    # Compare the overlap / lack thereof of the attendee groups
    comparison = analyses.compare_attendees(events_list_a, events_list_b)
    attends_both = comparison['a_and_b']
    attends_only_a = comparison['a_not_b']
    attends_only_b = comparison['b_not_a']

    tex_vars['allboth'] = len(attends_both['All'])
    tex_vars['boardboth'] = len(attends_both['Board'])
    tex_vars['volunteersboth'] = len(attends_both['Volunteers'])
    tex_vars['membersboth'] = len(attends_both['Members'])
    tex_vars['nonmembersboth'] = len(attends_both['Nonmembers'])

    tex_vars['allonlya'] = len(attends_only_a['All'])
    tex_vars['boardonlya'] = len(attends_only_a['Board'])
    tex_vars['volunteersonlya'] = len(attends_only_a['Volunteers'])
    tex_vars['membersonlya'] = len(attends_only_a['Members'])
    tex_vars['nonmembersonlya'] = len(attends_only_a['Nonmembers'])

    tex_vars['allonlyb'] = len(attends_only_b['All'])
    tex_vars['boardonlyb'] = len(attends_only_b['Board'])
    tex_vars['volunteersonlyb'] = len(attends_only_b['Volunteers'])
    tex_vars['membersonlyb'] = len(attends_only_b['Members'])
    tex_vars['nonmembersonlyb'] = len(attends_only_b['Nonmembers'])

    # optionally, generate email lists
    if include_emails:
        tex_vars['emailboardboth'] = ''
        tex_vars['emailvolunteersboth'] = ''
        tex_vars['emailmembersboth'] = ''
        tex_vars['emailnonmembersboth'] = ''
        tex_vars['emailboardonlya'] = ''
        tex_vars['emailvolunteersonlya'] = ''
        tex_vars['emailmembersonlya'] = ''
        tex_vars['emailnonmembersonlya'] = ''
        tex_vars['emailboardonlyb'] = ''
        tex_vars['emailvolunteersonly_b'] = ''
        tex_vars['emailmembersonly_b'] = ''
        tex_vars['emailnonmembersonly_b'] = ''

        for email in attends_both['Board']:
            tex_vars['emailboardboth'] += email + '\n'
        for email in attends_both['Volunteers']:
            tex_vars['emailvolunteersboth'] += email + '\n'
        for email in attends_both['Members']:
            tex_vars['emailmembersboth'] += email + '\n'
        for email in attends_both['Nonmembers']:
            tex_vars['emailnonmembersboth'] += email + '\n'
        for email in attends_only_a['Board']:
            tex_vars['emailboardonlya'] += email + '\n'
        for email in attends_only_a['Volunteers']:
            tex_vars['emailvolunteersonlya'] += email + '\n'
        for email in attends_only_a['Members']:
            tex_vars['emailmembersonlya'] += email + '\n'
        for email in attends_only_a['Nonmembers']:
            tex_vars['emailnonmembersonlya'] += email + '\n'
        for email in attends_only_b['Board']:
            tex_vars['emailboardonlyb'] += email + '\n'
        for email in attends_only_b['Volunteers']:
            tex_vars['emailvolunteersonlyb'] += email + '\n'
        for email in attends_only_b['Members']:
            tex_vars['emailmembersonly_b'] += email + '\n'
        for email in attends_only_b['Nonmembers']:
            tex_vars['emailnonmembersonlyb'] += email + '\n'

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
    tex_vars['attendancecharta'] = './.working/attendance_a.png'
    tex_vars['attendancechartb'] = './.working/attendance_b.png'

    texvar.write_tex_vars(tex_vars)
    subprocess.check_output('pdflatex -output-directory Reports Templates/comparison.tex', shell=True)
    conn.close()
