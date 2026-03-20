"""
https://discourse.holoviz.org/t/streaming-data-with-bokeh-and-panel-periodic-callbacks/1022

"""

from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.io import curdoc
import numpy as np

ds = ColumnDataSource({"x": [0, 4, 5], "y": [0, 2, 3]})
i = 1

def update(event=None):
    global i
    ds.stream({"x": [i], "y": [np.random.rand()]})
    i += 1

p = figure()
p.line(x="x", y="y", source=ds)

curdoc().add_periodic_callback(update, 200)

output_file("test.html", title="Update")
show(p)
