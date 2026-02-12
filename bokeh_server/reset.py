import time
from functools import partial
from random import random
from threading import Thread

from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure


from bokeh.layouts import column
from bokeh.models import Button

# only modify from a Bokeh session callback
source = ColumnDataSource(data=dict(x=[0], y=[0]))

# This is important! Save curdoc() to make sure all threads
# see the same document.
doc = curdoc()

def callback_reset():
    # Functional reset
    up = {"x": [], "y": []}
    source.data = up
    

def update_2():
    # Add a new point
    x, y = random(), random()
    source.stream(dict(x=[x], y=[y]))

def periodic_task():
    # Callback evey 100 ms
    doc.add_periodic_callback(update_2, 100)


p = figure(x_range=[0, 1], y_range=[0,1])
l = p.circle(x='x', y='y', source=source)

periodic_task()



# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_event('button_click', callback_reset)

# put the button and plot in a layout and add to the document
doc.add_root(column(button, p))

#thread = Thread(target=blocking_task)
#thread.start()
