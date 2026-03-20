"""
Solar panel yield simulation.
 
Suppose you can rotate on the ground your panel, so it is always facing the sun.
However, you need to select a fixed tilt angle.

Compute the yield for a date at a given latitude over the time

"""

from bokeh.plotting  import ColumnDataSource, figure, output_file, show
from bokeh.models    import  HoverTool, CustomJS, Slider
from bokeh.layouts   import column

import numpy as np

def d2r(x):
    return x/180 * np.pi

def r2d(x):
    return x / np.pi * 180


if __name__ == "__main__":
    
    lat0  = 50
    day0 = 30
    gamma0 =  23.433333 * np.sin(2 * np.pi * (day0 + 284) / 365);


    hours = np.linspace(0, 24, 200)
    hra    = 15 * (hours - 12) 
    angles = np.arcsin(np.sin(d2r(gamma0)) * np.sin(d2r(lat0)) 
                      + np.cos(d2r(gamma0)) * np.cos(d2r(lat0)) * np.cos(d2r(hra)))

    source = ColumnDataSource(data=dict(x=hours, y=100*np.sin(angles), h=hra*np.pi/180 ))

    # Slider lat
    slider_lat   = Slider(start=0, end=90, value=lat0, step=0.00001, title="Latitude")
    # Slider day
    slider_day   = Slider(start=0, end=365, value=day0, step=1, title="Days since 1st of Jan.")
    # Slider orientation
    slider_panel   = Slider(start=0, end=90, value=0, step=0.25, title="Solar panel tilt angle.")

    callback = CustomJS(args=dict(source=source, 
        s_lat=slider_lat,
        s_day=slider_day,
        s_pan=slider_panel,
        ),
                        code="""
        const data = source.data;
        const PI  = 3.14159265359;
        const N = s_day.value // Days since 1st of january
        const LAT = s_lat.value * PI / 180;
        const GAMMA = 23.433333 * PI / 180 * Math.sin(2 * PI * (N + 284) / 365);

        const A = Math.sin(GAMMA) * Math.sin(LAT);
        const B = Math.cos(GAMMA) * Math.cos(LAT);
        const beta = s_pan.value * PI / 180;

        for (var i=0; i < data.x.length; i++){
            var a = Math.asin(A + B * Math.cos(data.h[i]));
            if (Math.sin(a) > 0) { 
                // day time
                data.y[i] = a + beta;
                data.y[i] = 100 * Math.sin(Math.max(0, data.y[i])); // Ratio
            } else {
                data.y[i] = 1/0; // night time
            }

        }

        source.change.emit();
        """)

    

    slider_lat.js_on_change('value', callback)
    slider_day.js_on_change('value', callback)
    slider_panel.js_on_change('value', callback)

     # Create the figure
    p = figure(plot_width=1000, plot_height=300,
            x_range=[0, 24],
            y_range=[0, 105],
            tools="pan,lasso_select,wheel_zoom,box_select,reset,save",
           title="Sun height over a day.")
    
    # Plot circles. Define name for the item
    p.line('x', 'y', name="lines", source=source, line_width=3, line_alpha=0.7)
    
    hover = HoverTool(tooltips=[("Hour", '@x'), ("Ratio", "@y")])
    p.add_tools(hover)


    p.xaxis.axis_label = 'Hours'
    p.yaxis.axis_label = 'Energy ratio (%)'
    p.xgrid.minor_grid_line_alpha = 0.4
    p.xgrid.grid_line_alpha = 0.7
    p.xgrid.ticker = [i for i in range(25)]
    p.xaxis.ticker = [i*3 for i in range(9)]

    output_file("../html/yield_rotative_fixed_tilt.html", title="Rotative solar panel yield.")
    show(column(p, slider_lat, slider_day, slider_panel))
    

