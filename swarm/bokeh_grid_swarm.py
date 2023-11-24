# Bokeh libs
from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.models import Slider, CustomJS
from bokeh.layouts import column
from bokeh.models import Arrow, NormalHead

import argparse
import os

import numpy as np

# In this repository
import swarm
import tips


SIZE = 800
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Display DBLP input files.')

    parser.add_argument('n', type=int, help='Grid size')
    parser.add_argument('--method', choices=["4c", "4", "8"], default="8", help='Method to update the grid')
    parser.add_argument('--steps', type=int, default=10, help='Number of steps')
    parser.add_argument('--arrow_length', type=float, default=0.8, help='Length of an arrow. To adapt with n')
    args = parser.parse_args()

    os.makedirs("./html/", exist_ok=True)
    
    n = args.n
    n_steps = args.steps
    lbd = args.arrow_length
    method = args.method
    
    # Select update function
    update_fx = swarm.update_9
    if method == "4":
        update_fx = swarm.update_4
    
    elif method == "4c":
        update_fx = swarm.update_4
        
        
    #####################
    # Create the figure #
    #####################
    
    p = figure(width=SIZE, height=SIZE,
               tools="pan,wheel_zoom,reset,save",
               title="Grid swarm")
    
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
    p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
    p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
    p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks


    
    M = np.random.rand(n, n) * 2 * np.pi + np.random.rand() * np.pi
    
    nh = NormalHead(fill_color="blue", fill_alpha=0.5, line_color="blue", size=5)
    
    
    # START
    dico = {"x": [], "y": [], "x_end": [], "y_end": []}

    xx, yy = np.meshgrid(np.arange(n), np.arange(n))
    dico["x"] = xx.reshape(-1)
    dico["y"] = yy.reshape(-1)
    dico["x_end"] = np.cos(M.reshape(-1)) * lbd + dico["x"]
    dico["y_end"] = np.sin(M.reshape(-1)) * lbd + dico["y"]

    source = ColumnDataSource(data=dico)
    # END 
    
    ##############################
    # Add elements to the figure #
    ##############################
    
    p.circle(x="x", y="y", radius=0.1, color="blue", alpha=0.4, source=source)
    
    p.add_layout(Arrow(end=nh, line_color="blue", 
                       x_start="x", y_start="y", x_end="x_end", y_end="y_end",
                      source=source))
    
    ##################################
    # Source for the different steps #
    ##################################
    
    dico_update = {"xs": [dico["x_end"]], "ys": [dico["y_end"]]}
    for s in range(n_steps):
        M = swarm.update_4(M)
        dico_update["xs"].append(np.cos(M.reshape(-1)) * lbd + dico["x"])
        dico_update["ys"].append(np.sin(M.reshape(-1)) * lbd + dico["y"])
        
    source_up = ColumnDataSource(data=dico_update)
    
    ###################
    # Create a slider #
    ###################
    
    my_slider = Slider(start=0, end=n_steps, value=0, step=1, title="Step", width=SIZE-50)
    
    code_slider = """
                var t = this.value;
                var df = source_plot.data;

                df.x_end = source_mem.data.xs[t];
                df.y_end = source_mem.data.ys[t];

                source_plot.change.emit();            
        """

    my_slider.js_on_change("value", CustomJS(args=dict(source_plot=source, 
                                                       source_mem=source_up),
                                                      code=code_slider))
    
    ##########
    # Output #
    ##########
    
    output_file("./html/grid_swarm_{}_{}_{}.html".format(method, n, n_steps), title="Grid Swarm")

    show(column(p, my_slider))
