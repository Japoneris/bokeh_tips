"""
Working script:

bokeh serve --show test_2.py


Link:

https://www.tutorialspoint.com/bokeh/bokeh_server.htm

"""

import psutil
import time 
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure


print(__name__)
VERBOSE = True

def setupper(dico, dico1):
    for item, vals in dico1.items():
        for idx, val in enumerate(vals):
            label = val.label
            if label == "":
                dico["{}_{}".format(item, idx)] = []
            else:
                dico["{}_{}".format(item, label)] = []
    return dico

def updater(dic_update, dico1):
    for item, vals in dico1.items():
        for idx, val in enumerate(vals):
            label = val.label
            if label == "":
                dic_update["{}_{}".format(item, idx)] = [val.current]
            else:
                dic_update["{}_{}".format(item, label)] = [val.current]
                
    return dic_update


### For each psutil fx

def setup_fans(dico):
    dico = setupper(dico, psutil.sensors_fans())
    
    if VERBOSE:
        print(dico)
        
    return dico


def update_fan(dic_update):
    """Update fans values
    """
    return updater(dic_update, psutil.sensors_fans())
    

def setup_temp(dico):
    dico = setupper(dico, psutil.sensors_temperatures())
    if VERBOSE:
        print(dico)
        
    return dico


def update_temp(dic_update):
    """Update fans values
    """
    return updater(dic_update, psutil.sensors_temperatures())


                
if True:
    
        
                
    dico = {"t": []}
    dico = setup_fans(dico)
    S_fans = set(dico) - {"t"}
    
    dico = setup_temp(dico)
    S_temp = set(dico) - ({"t"} | S_fans)
    
    
    source = ColumnDataSource(data = dico)
    
    t0 = time.time()
    
    def update_all(event=None):
        """Streaming:
        Feed a dictionnary with the changes
        Update the old dictionnary.
        """
        t1 = round(time.time() - t0, 3)  
        dic_update = {"t": [t1]}
        update_fan(dic_update)
        update_temp(dic_update)
        
        source.stream(dic_update)
        
    
    color_list = ["brown", "darkturquoise", "royalblue",
                 "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred",
                  "darksalmon", "darkseagreen", "darkslateblue", "darkslategray", "darkslategrey",
                  "darkturquoise", "darkviolet", "deeppink", "deepskyblue" 
                 ]
    
    # Initialize fans
    p_fans = figure(plot_height = 400, plot_width = 800, title = "Fan speed",
                    y_axis_label="RPM", x_axis_label="time (sec)",
              tools="pan,lasso_select,wheel_zoom,box_select,tap,reset,save",)
    
    TOOLTIPS = []
    for idx, key in enumerate(S_fans):
        TOOLTIPS.append((key, "@{}".format(key)))
        p_fans.line('t', key, source = source, line_width = 3, line_alpha = 0.6, color=color_list[idx])
    
    hover = HoverTool(tooltips=TOOLTIPS)
    p_fans.add_tools(hover)
    

    # Initialize temperature
    p_temp = figure(plot_height = 400, plot_width = 800, title = "Core temperature",
                    y_axis_label="°C", x_axis_label="time (sec)",
              tools="pan,lasso_select,wheel_zoom,box_select,tap,reset,save",)
    
    for idx, key in enumerate(S_temp):
        p_temp.line('t', key, name=key, source = source, line_width = 3, line_alpha = 0.6, color=color_list[idx])
        p_temp.add_tools(HoverTool(names=[key], tooltips=[("time", "@t"), (key,  "@{}".format(key))]))
        
    
    
    
    # Initialize CPU Usage
    
    
    
    curdoc().add_periodic_callback(update_all, 500) # TODO: config


    curdoc().add_root(column(p_fans, p_temp))
    curdoc().title = "Sensors"