"""Build a query for selecting events. Result should be fed into analyses.py methods."""
from datetime import datetime


def build_query(names=[], dates=[], date_range=()):
    """Dynamically build a query of events table."""
    query = 'SELECT * FROM events WHERE '
    for name in names:
        query += 'name=? OR '
    if len(names) >= 1:
        query = query[:-4] + ' AND '

    datestrings = []
    for date in dates:
        if not isinstance(date, datetime):
            raise TypeError('date must be of type datetime.date')
        query += 'date(time) = date(?) OR '
        datestrings.append(date.isoformat())
    if len(dates) >= 1:
        query = query[:-4] + ' AND '

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
        query += 'date(time) BETWEEN ? and ?'
        rangestrings.append(date_range[0].isoformat())
        rangestrings.append(date_range[1].isoformat())

    return (query, names + datestrings + list(date_range))
