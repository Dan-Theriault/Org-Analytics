"""Basic script to start a fresh database."""
import sqlite3
import loader
from sys import argv

conn = sqlite3.connect(loader.DB)
c = conn.cursor()

c.execute('PRAGMA foreign_keys = ON;')

c.execute('CREATE TABLE students(email TEXT PRIMARY KEY, name TEXT, is_member BOOLEAN, is_volunteer BOOLEAN, is_board BOOLEAN)')
c.execute('CREATE TABLE events(name TEXT, time TEXT, PRIMARY KEY(name, time))')
c.execute('''CREATE TABLE records(event_name TEXT, event_time TEXT, student_email TEXT, checkin_time TEXT, FOREIGN KEY(event_name, event_time) REFERENCES events(name, time), FOREIGN KEY(student_email) REFERENCES students(email))''')

conn.commit()
conn.close()

if len(argv) == 2:
    loader.main(argv[1])
