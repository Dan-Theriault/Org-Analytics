"""Used by orchestrator to draw graphs."""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
from os import path

WORK_DIR = '.working'


def arrival_chart(dataset, filename):
    """Line plot of the arrival times."""
    df = pd.DataFrame(dataset)
    df = df.rename(columns={0: '(Arrival Time - Start Time)'})
    df = pd.DataFrame(df.groupby('(Arrival Time - Start Time)').size())
    df = df.rename(columns={0: 'Attendees'})

    filename = path.join('.working', filename)
    plot = df.plot(
        colormap='Set2',
        figsize=(7, 4),
        title="Relative Arrival Times"
    )
    plot.set_xlim(-20, 40)

    fig = plot.get_figure()
    fig.savefig(filename)
    plt.close(fig)


def bar_chart(dataset, filename, title="Event Attendance"):
    """Stacked bar chart of attendance at events in dataset, includes attendee type data."""
    df = pd.DataFrame(
        dataset, index=[event[0] for event in dataset],
        columns=['Event', 'Board', 'Volunteers', 'Members', 'Nonmembers']
    )

    filename = path.join('.working', filename)
    plot = df.plot.barh(
        stacked=True,
        title=title,
        colormap='Set2',
        figsize=(16.1, 1 + .55 * len(dataset))
    )

    fig = plot.get_figure()
    fig.savefig(filename)
    plt.close(fig)


def pie_chart(dataset, filename):
    """Pie chart of attendance at an event."""
    df = pd.DataFrame(dataset)
    df = df.drop('All', 0)

    filename = path.join('.working', filename)
    fig = df.plot.pie(subplots=True)[0].get_figure()
    fig.savefig(filename)
    plt.close(fig)


def venn_diagram(dataset, filename, title=''):
    """Draw a venn diagram.

    dataset should be of form (Ab, aB, AB).
    """
    venn2(dataset)

    filename = path.join('.working', filename)
    plt.savefig(filename)
    plt.close()
