"""Build a query for selecting events. Result should be fed into analyses.py methods."""
from datetime import datetime


def build_query(names=[], dates=[], date_range=()):
    """Dynamically build a query of events table."""
    query = 'SELECT * FROM events WHERE ('
    for name in names:
        query += 'name=? OR '
    if len(names) >= 1:
        query = query[:-4] + ') AND ('

    datestrings = []
    for date in dates:
        if not isinstance(date, datetime):
            raise TypeError('date must be of type datetime.date')
        query += 'date(time) = date(?) OR '
        datestrings.append(date.isoformat())
    if len(dates) >= 1:
        query = query[:-4] + ') AND ('

    if date_range == ():
        query = query[:-5]
    elif len(date_range) != 2:
        raise ValueError('date_range must be a 2-tuple')
    else:
        rangestrings = []
        if not isinstance(date_range[0], datetime):
            raise TypeError('start date must be of type datetime.date')
        if not isinstance(date_range[1], datetime):
            raise TypeError('end date must be of type datetime.date')
        query += 'date(time) BETWEEN ? and ?)'
        rangestrings.append(date_range[0].isoformat())
        rangestrings.append(date_range[1].isoformat())

    return (query, names + datestrings + list(date_range))


def name_group(names=[], dates=[], date_range=()):
    """Produce a human-readable string describing the event group."""
    groupname = ""

    # Event names are the first part of the string
    if names == []:
        groupname = "Events"
    else:
        if len(names) == 1:
            groupname = "`{}'".format(names[0])
        elif len(names) == 2:
            groupname = "`{}' and `{}'".format(names[0], names[1])
        else:
            for name in names[:-1]:
                groupname += "`{}', ".format(name)
            groupname += "and `{}'".format(names[-1])

    # Dates come next, but there's an interaction with date_range-- only dates in the range are shown
    # If both date and range arguments are present, only show resulting dates
    if date_range != ():
        if len(dates) == 0:
            groupname += " from {} to {}".format(
                date_range[0].isoformat()[:10],
                date_range[1].isoformat()[:10]
            )
        else:
            dates = [date for date in dates if date > date_range[0] and date < date_range[1]]

    if len(dates) == 1:
        groupname += " on {}".format(dates[0].isoformat()[:10])
    elif len(dates) == 2:
        groupname += " on {} and {}".format(dates[0].isoformat()[:10], dates[1].isoformat()[:10])
    elif len(dates) > 2:
        groupname += " on "
        for date in dates[:-1]:
            groupname += "{}, ".format(date.isoformat()[:10])
        groupname += "and {}".format(dates[-1].isoformat()[:10])

    return groupname
