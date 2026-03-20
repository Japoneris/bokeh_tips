"""
Yield over the year = F(beta; lat)

Do integration by summing over each day yield.
Assumption that the panel rotate on the ground, at the hour angle speed.

"""

from bokeh.plotting  import ColumnDataSource, figure, output_file, show
from bokeh.models    import HoverTool, CustomJS, Slider
from bokeh.layouts   import column

import numpy as np

def d2r(x):
    return x/180 * np.pi

def r2d(x):
    return x / np.pi * 180


if __name__ == "__main__":
    
    # Default param
    lat0  = 50
    
    
    hours = np.linspace(0, 24, 200)
    hra    = d2r(15 * (hours - 12)) 
    beta_range = np.arange(90)
    
    # Compute yield for each day of the year
    yields = np.zeros(len(beta_range))

    for N in range(365):
        gamma0 =  23.433333 * np.sin(2 * np.pi * (N + 284) / 365);

        A = np.sin(d2r(gamma0)) * np.sin(d2r(lat0))
        B = np.cos(d2r(gamma0)) * np.cos(d2r(lat0)) 
        angles = np.arcsin(A + B * np.cos(hra))
        angles = angles[angles >= 0]
        
        for idx, beta in enumerate(beta_range):
            yields[idx] += np.sin(d2r(beta) + angles).clip(0).sum()
        
    yields = yields / (len(hra) * 365) * 2 * 100

    # Initialize tources
    b_max = beta_range[np.argmax(yields)]
    source = ColumnDataSource(data=dict(x=beta_range, y=yields, xx=d2r(beta_range)))
    source_t = ColumnDataSource(data=dict(t=np.cos(hra)))
    source_m = ColumnDataSource(data=dict(x=[b_max, b_max], y=[0, np.max(yields)])) # Max line



    # Initialize objects
    slider_lat   = Slider(start=0, end=90, value=lat0, step=0.01, title="Latitude")


    callback = CustomJS(args=dict(source=source, 
        source_t=source_t,
        source_m=source_m,
        s_lat=slider_lat,
        ),
                        code="""
        const data = source.data;
        const timing = source_t.data;
        const PI  = 3.14159265359;
        const LAT = s_lat.value * PI / 180;
        

        
        // reset to 0
        for (var i=0; i < data.y.length; i++) {
            data.y[i] = 0;
        }
        
        console.log("Reset ok")


        // by symmetry, can be fasten by 2
        for (var N=0; N < 365; N++) {
            const GAMMA = 23.433333 * PI / 180 * Math.sin(2 * PI * (N + 284) / 365);
            
            const A = Math.sin(GAMMA) * Math.sin(LAT);
            const B = Math.cos(GAMMA) * Math.cos(LAT);
            
            for (var i=0; i < timing.t.length; i++) {
                var a = Math.asin(A + B * timing.t[i]);
                if (a > 0) {
                    for (var j=0; j < data.x.length; j++) {
                        data.y[j] = data.y[j] + Math.max(Math.sin(data.xx[j] + a), 0);
                    }
                }
            }
        }


        var a_max = 0; // Maximal angle
        var r_max = 0; // Maximal yield
        
        console.log(data.y.length)

        for (var i=0; i < data.y.length; i++) {
            console.log(data.y[i])
            data.y[i] = data.y[i] / (365 * timing.t.length) * 200;
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

    
    # Create the figure
    p = figure(plot_width=1000, plot_height=300,
            x_range=[0, 90],
            y_range=[0, 105],
            tools="pan,lasso_select,wheel_zoom,box_select,reset,save",
           title="Average yield over a day N and lat as a function of the tilt angle, + day length.")
    
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

    output_file("../html/yield_year.html", title="Average yield over the year.")
    show(column(p, slider_lat))
    

