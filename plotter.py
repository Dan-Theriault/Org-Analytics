"""Used by orchestrator to draw graphs."""
import pandas as pd
from os import path

WORK_DIR = '.working'


def arrival_chart(dataset, filename):
    """Line plot of the arrival times."""
    df = pd.DataFrame(dataset)
    df = df.rename(columns={0: 'Relative Arrival Times'})
    df = pd.DataFrame(df.groupby('Relative Arrival Times').size())
    df = df.rename(columns={0: 'Attendees'})

    filename = path.join('.working', filename)
    plot = df.plot()
    plot.get_figure().savefig(filename)


def bar_chart(dataset, filename):
    """Stacked bar chart of attendance at events in dataset, includes attendee type data."""
    df = pd.DataFrame(dataset)
    df = df.drop('All', 0)
    df = df.transpose()

    filename = path.join('.working', filename)
    plot = df.plot.bar(stacked=True)
    plot.get_figure().savefig(filename)


def pie_chart(dataset, filename):
    """Pie chart of attendance at an event."""
    df = pd.DataFrame(dataset)
    df = df.drop('All', 0)

    filename = path.join('.working', filename)
    plot = df.plot.pie(subplots=True)[0]
    plot.get_figure().savefig(filename)
