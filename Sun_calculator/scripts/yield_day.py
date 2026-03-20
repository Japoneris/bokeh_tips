"""
Assuming you can rotate your panel on the ground (but you cannot change the tilt angle), such that the panel follow the sun.
Measure the yield for each tilt angle.
f(day, latitude)

The yield is independent of the day length (i.e. it is relative to the day period)
"""

from bokeh.plotting  import ColumnDataSource, figure, output_file, show
from bokeh.models    import HoverTool, CustomJS,  Slider
from bokeh.layouts   import column


import numpy as np

def d2r(x):
    return x/180 * np.pi

def r2d(x):
    return x / np.pi * 180


if __name__ == "__main__":
    

    # Default value to initialize the plot
    lat0   = 50
    day0   = 30
    gamma0 =  23.433333 * np.sin(2 * np.pi * (day0 + 284) / 365);


    hours = np.linspace(0, 24, 200)
    hra    = d2r(15 * (hours - 12)) 
    beta   = np.arange(90)

    A = np.sin(d2r(gamma0)) * np.sin(d2r(lat0))
    B = np.cos(d2r(gamma0)) * np.cos(d2r(lat0)) 
    angles = np.arcsin(A + B * np.cos(hra))
    angles = angles[angles >= 0]

    vals = []
    for b in beta:
        vals.append(100 * (np.sin(d2r(b) + angles).clip(0).mean()))

    b_max    = beta[np.argmax(vals)]
    source   = ColumnDataSource(data=dict(x=beta, y=vals, xx=d2r(beta)))
    source_t = ColumnDataSource(data=dict(t=hra))
    source_m = ColumnDataSource(data=dict(x=[b_max, b_max], y=[0, np.max(vals)])) # Max line



    # Slider lat
    slider_lat   = Slider(start=0, end=90, value=lat0, step=0.00001, title="Latitude")
    # Slider day
    slider_day   = Slider(start=0, end=365, value=day0, step=1, title="Days since 1st of Jan.")


    callback = CustomJS(args=dict(source=source, 
        source_t=source_t,
        source_m=source_m,
        s_lat=slider_lat,
        s_day=slider_day,
        ),
                        code="""
        const data = source.data;
        const timing = source_t.data;
        const PI  = 3.14159265359;
        const N = s_day.value // Days since 1st of january
        const LAT = s_lat.value * PI / 180;
        const GAMMA = 23.433333 * PI / 180 * Math.sin(2 * PI * (N + 284) / 365);
        
        const A = Math.sin(GAMMA) * Math.sin(LAT);
        const B = Math.cos(GAMMA) * Math.cos(LAT);

        var a_max = 0; // Maximal angle
        var r_max = 0; // Maximal yield
        
        for (var i=0; i < data.x.length; i++) {
            var b = data.xx[i];
            var s = 0;
            var c = 1; // 1 to avoid division by zero
            
            for (var j=0; j < timing.t.length; j++) {
                var ax = Math.asin(A + B*Math.cos(timing.t[j]))

                var a = Math.sin(b + ax);
                if (ax > 0) {
                    s = s + a;
                    c = c + 1;
                }
            }
            data.y[i] = 100 * s / c;
            if (data.y[i] > r_max) {
                r_max = data.y[i];
                a_max = data.x[i];
            }
        }

        source_m.data.x = [a_max, a_max];
        source_m.data.y = [0, r_max];


        source.change.emit();
        source_m.change.emit();
        """)

    

    slider_lat.js_on_change('value', callback)
    slider_day.js_on_change('value', callback)

     # Create the figure
    p = figure(plot_width=1000, plot_height=300,
            x_range=[0, 90],
            y_range=[0, 105],
            tools="pan,wheel_zoom,reset,save",
           title="Yield = f(day, lat) | independently of the day lenght, for a rotative panel.")
    
    # Plot circles. Define name for the item
    p.line('x', 'y', name="lines", source=source, line_width=3, line_alpha=0.7)
    p.line("x", "y", source=source_m, line_color="black",line_dash="dashed")
    
    hover = HoverTool(tooltips=[("Angle (°)", '@x'), ("Yield (%)", "@y")])
    p.add_tools(hover)


    p.xaxis.axis_label = 'Tilt angle °'
    p.yaxis.axis_label = 'Yield (%)'
    p.xgrid.minor_grid_line_alpha = 0.4
    p.xgrid.grid_line_alpha = 0.7
    p.xgrid.ticker = [i*5 for i in range(19)]
    p.xaxis.ticker = [i*5 for i in range(19)]

    output_file("../html/sun_yield_day_fixed_panel.html", title="Average Yield over a day.")
    show(column(p, slider_lat, slider_day))
    

