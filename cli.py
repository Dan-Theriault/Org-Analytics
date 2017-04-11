"""Command Line Interface to the orchestrator component."""
import orchestrator

import argparse
from datetime import datetime


def main():
    """Execute when program is directly invoked."""
    main_parser = argparse.ArgumentParser(
        description='Org Analytics report generator.'
    )
    main_parser.add_argument(
        '--emails', dest='emails', action='store_true',
        help='Enable generation of email lists.'
    )
    main_parser.set_defaults(emails=False)

    main_parser.add_argument(
        '--names', '-n', metavar='NAMES', nargs='*', default=[],
        help='Names of events to include in report'
    )
    main_parser.add_argument(
        '--dates', '-d', metavar='DATES', nargs='*', default=[],
        help='ISO 8601 formatted dates of events to include in report'
    )
    main_parser.add_argument(
        '--start', '-s', metavar='STARTDATE', nargs='?',
        help='ISO 8601 formatted date starting a date-range selection for event inclusion'
    )
    main_parser.add_argument(
        '--end', '-e', metavar='ENDDATE', nargs='?', default=datetime.today().isoformat()[:-16],
        help="ISO 8601 formatted date terminating a date-range selection for event inclusion, defaults to today."
    )

    # Secondary / subcommand parser for comparison reports
    subparsers = main_parser.add_subparsers(dest='subparser_name')
    vs_parser = subparsers.add_parser(
        'vs', description='Specify a second group of events to compare the first selection with.'
    )
    vs_parser.add_argument(
        '--names_vs', '--names', '-n', metavar='NAMES', nargs='*', default=[],
        help='Names of events to include in report'
    )
    vs_parser.add_argument(
        '--dates_vs', '--dates', '-d', metavar='DATES', nargs='*', default=[],
        help='ISO 8601 formatted dates of events to include in report'
    )
    vs_parser.add_argument(
        '--start_vs', '--start', '-s', metavar='STARTDATE', nargs='?',
        help='ISO 8601 formatted date starting a date-range selection for event inclusion'
    )
    vs_parser.add_argument(
        '--end_vs', '--end', '-e', metavar='ENDDATE', nargs='?', default=datetime.today().isoformat()[:-16],
        help='ISO 8601 formatted date terminating a date-range selection for event inclusion. Defaults to today.'
    )

    # print(main_parser.parse_args())

    # Argument Parsing Logic -- reads parsed args and calls orchestrator's report-generating methods
    cargs = main_parser.parse_args()
    date_range = () if cargs.start is None else (cargs.start, cargs.end)
    if cargs.subparser_name is None:
        # Call to standard report generator-- 1 event group
        orchestrator.standard_report(cargs.names, cargs.dates, date_range, include_emails=cargs.emails)
    elif cargs.subparser_name == 'vs':
        date_range_vs = () if cargs.start_vs is None else (cargs.start_vs, cargs.end_vs)
        # call to comparison report generator-- 2 event groups
        orchestrator.comparison_report(
            (cargs.names, cargs.dates, date_range),
            (cargs.names_vs, cargs.dates_vs, date_range_vs),
            include_emails=cargs.emails
        )

if __name__ == '__main__':
    main()
