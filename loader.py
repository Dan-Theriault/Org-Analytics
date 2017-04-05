"""Moves data from xlsx files to sqlite."""

import xlrd
import sqlite3
from os import listdir
from os.path import isfile, join
from dateutil.parser import parse as dateparse

data_dir = 'Data'
db = 'GTCSO.db'


def parse_xlsx(f, event_name):
    """parse an xlsx file and insert data into SQLite instance."""
    conn = sqlite3.connect(db)
    c = conn.cursor

    sheet = (xlrd.open_workbook(f)).sheet_by_name('Participation')

    # 2D list of cells, excluding label row
    rows = [sheet.row_slice(i+1) for i in range(sheet.nrows-1)]
    # TODO: add name and date of event to db
    time = rows[0][0].value
    c.execute('INSERT INTO events

    # Step 1: pull data from excel sheet
    for row in rows:
        # firstname lastname
        name = '{} {}'.format(row[3].value, row[2].value)

        # unique identifier
        email = row[4].value

        checkin = dateparse(row[9].value)
        # time format HH:MM, ie 18:01
        checkin = '{}:{}'.format(checkin.hour, checkin.minute)

        # ... Well this will make the schema fun
        groups = (row[11].value).split(', ')

    # TODO: Step 2: insert data to SQLite Database


data_files = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]

# TODO: exclude already-parsed items in data_files

for entry in data_files:
    parse_xlsx(join(data_dir, entry), entry[:-19])

c.commit()
conn.close()
