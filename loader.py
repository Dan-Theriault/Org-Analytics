#!/bin/env python3

"""Moves data from xlsx files to sqlite."""

from os import listdir
from os.path import isfile, join
import sqlite3
import xlrd

DATA_DIR = 'Data'
DB = 'GTCSO.db'


def main():
    """Parse all reports found in DATA_DIR."""
    data_files = [f for f in listdir(DATA_DIR) if isfile(join(DATA_DIR, f))]

    for entry in data_files:
        parse_xlsx(join(DATA_DIR, entry), (entry.rsplit(' Participation'))[0])


def parse_xlsx(file_, event_name):
    """Parse an xlsx file and insert data into SQLite instance."""
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    sheet = (xlrd.open_workbook(file_)).sheet_by_name('Participation')

    # 2D list of cells, excluding label row
    rows = [sheet.row_slice(i+1) for i in range(sheet.nrows-1)]

    # check if event is already in db
    # if so, return
    # if not, add name and date of event to db and continue
    time = rows[0][0].value
    event_info = [event_name, time]
    cur.execute('SELECT * FROM events WHERE name=? AND time=?',
                event_info)
    if cur.fetchall() == []:
        cur.execute('INSERT INTO events VALUES (?,?)', event_info)
    else:
        return

    for row in rows:
        # First get student's information
        name = '{} {}'.format(row[3].value, row[2].value)  # first last
        email = row[4].value  # this is a unique ID
        group_names = (row[11].value).split(', ')
        groups = [1 if ('General Members' in group_names) else 0,
                  1 if ('CSO Pillar Volunteers' in group_names) else 0,
                  1 if ('CSO Board' in group_names) else 0]

        # Create or update record of this student
        cur.execute('SELECT * FROM students WHERE email=?', [email])
        if cur.fetchall() == []:
            cur.execute('INSERT INTO students VALUES (?,?,?,?,?)',
                        ([email, name] + groups))
        else:
            cur.execute('UPDATE students SET is_member=?, is_volunteer=?,'
                        + 'is_board=? WHERE email=?', groups + [email])

        # Move on to recording this attendance instance
        checkin_time = row[9].value
        checkin_time = 'Manual' if (checkin_time == '') else checkin_time
        cur.execute('INSERT INTO records VALUES (?,?,?,?)',
                    event_info + [email, checkin_time])

    conn.commit()
    conn.close()
    return

if __name__ == "__main__":
    main()
