"""
How to use bokeh with arguments ?

bokeh serve combined.py --args my_pos_arg1


bokeh serve LED_simulator.py --args line 34
bokeh serve LED_simulator.py --args matrix 16 10
bokeh serve LED_simulator.py --args --delay=10 border 20 12


The server would crash after loading the first page if bad arguments are passed
"""
import argparse
import numpy as np

from bokeh.io import curdoc, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Rect



import importlib.util

def module_from_file(module_name, file_path):
    # Load a module from file.
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module



parser = argparse.ArgumentParser('LED simulator aggregator')


parser.add_argument("--file", default="my_coloring_template.py", help="script location")
parser.add_argument("--delay", type=int, default=100, help="Time in ms between updates")

subparsers = parser.add_subparsers(dest='command')

sub_line = subparsers.add_parser('line', help='line simulator')
sub_line.add_argument("LED", type=int, help="Number of led in the row")


sub_matrix = subparsers.add_parser('matrix', help='matrix simulator')
sub_matrix.add_argument("LED_x", type=int, help="Number of led in the row")
sub_matrix.add_argument("LED_y", type=int, help="Number of led in a column")


sub_border = subparsers.add_parser('border', help='matrix simulator')
sub_border.add_argument("LED_x", type=int, help="Number of led in the row(+1)")
sub_border.add_argument("LED_y", type=int, help="Number of led in a column(+1)")

args = parser.parse_args()

print(args)

led_module = module_from_file("foo", args.file)

# Variable initialisation
x, y, w, h = None, None, None, None

WIDTH = 800
LED_x = 1
LED_y = 1



if args.command == "line":
    print(args.LED)
    LED = args.LED
    LED_x = LED


    x = np.arange(LED)
    y = np.zeros(LED)
    w = np.ones(LED)
    h = np.ones(LED)
    

elif args.command == "matrix":
    print("Horizontal LED:", args.LED_x)
    print("Vertical LED:  ", args.LED_y)
    
    LED_x = args.LED_x
    LED_y = args.LED_y
    
    LED = LED_x * LED_y
    LED = LED_x * LED_y

    M = np.arange(LED).reshape((LED_x, LED_y))

    for i in range(LED_x): # LED_y
        if i % 2 == 1:
            M[i] = M[i][::-1]

    # SETUP LED grid locations
    x = np.zeros(LED)
    y = np.zeros(LED)
    h = np.ones(LED)
    w = np.ones(LED)
    for idx, row in enumerate(M):
        for jdx, v in enumerate(row):
            y[v] = idx
            x[v] = jdx

    #custom_fx = led_module.create_matrix(LED_x, LED_y)
    

elif args.command == "border":
    print(args.LED_x)
    print(args.LED_y)
    LED_x = args.LED_x
    LED_y = args.LED_y
    
    LED = 2 * (LED_x + LED_y)

    x = np.zeros(LED)
    y = np.zeros(LED)

    x[:LED_x+1] = np.arange(LED_x+1)
    x[-(LED_y + LED_x+1)+1:-LED_y] = np.arange(1,LED_x+1)[::-1]
    x[LED_x+1:-(LED_y+LED_x)] = LED_x

    y[LED_x:LED_x+LED_y+1] = np.arange(LED_y+1)
    y[LED_x+LED_y+1:LED_x*2+LED_y+1] = LED_y
    y[LED_x*2+LED_y+1:] = np.arange(1,LED_y)[::-1]

    w = np.ones(LED)
    h = np.ones(LED)


    #custom_fx = led_module.create_border(LED_x, LED_y)

else:
    print("Error, does not exist")
    assert(False)

mod = led_module.Strip(LED)
custom_fx = lambda t: mod.update()

S = int(WIDTH / (LED_x + 2))

# Initialization of the datasource
source = ColumnDataSource(dict(x=x, y=y, w=w, h=h, col=["black" for _ in x]))

p = figure(width=(2+LED_x)*S, height=(LED_y + 2) * S, title="LED simulator")

glyph = Rect(x="x", y="y", width="w", height="h", fill_color="col")
p.add_glyph(source, glyph)

p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks

p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels

p.xaxis.major_label_text_color = None  # turn off x-axis tick labels leaving space
p.yaxis.major_label_text_color = None  # turn off y-axis tick labels leaving space

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

doc = curdoc()


t = 0

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def my_update():
    global t

    # Should return n x 3 array for the three colors
    # Should be of type INT
    RGB = custom_fx(t)

    
    # Convert to RGB hex code
    vals = [rgb_to_hex(r, g, b) for r, g, b in RGB]


    source.data["col"] = vals
    t += 1

doc.add_periodic_callback(my_update, args.delay)

doc.add_root(p)


