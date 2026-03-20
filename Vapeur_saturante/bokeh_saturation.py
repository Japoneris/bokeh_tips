import argparse
import json
import numpy as np

from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.models import Segment, HoverTool, Slider, CustomJS, TapTool, OpenURL, LinearColorMapper
from bokeh.palettes import Plasma256, inferno

from bokeh.layouts import column, row
from bokeh.models.widgets import DataTable, TableColumn





if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Loi d'Arhenius")


    parser.add_argument("--save_path", default="approx_eau_air.html", 
            help="Where to save the file")

    parser.add_argument('-s', default=10, type=int,
                  help="Size of dots")

    parser.add_argument('-d', default=10, type=int,
                  help="Maximal link distance")
    parser.add_argument('--links', default=False, action="store_true",
                  help="Draw (if availables) the links between the nodes.")

    args = parser.parse_args()


    
    x = np.linspace(0, 100, 101)

    y = 18 / (8.314 * (x+ 273.15)) * np.exp(13.7 - 5120 / (x+273.15)) * 101325

    dico = {"X": x, "Y": y}

    source = ColumnDataSource(data=dico)
    
    p = figure(plot_width=700, plot_height=400, #x_range=(a,b), y_range=(c,d),
            x_axis_label="Temperature (°C)",
            y_axis_label="Water amount (g)",
            tools="pan,lasso_select,wheel_zoom,box_select,tap,reset,save",
            title="Rankine model: Amount of water in 1m3 at P atm = f(T).")

    
    p.line('X', 'Y', name="circ", line_width=3,source=source)
    

    hover = HoverTool(names=["circ"], tooltips=[("T°C", "@X"), ("H2O g", "@Y")])
    p.add_tools(hover)



    output_file(args.save_path, title="Map of XXX")
    show(p)



    
