"""
Total yield over a day for a non-rotative solar panel.




"""

from bokeh.plotting  import ColumnDataSource, figure, output_file, show
from bokeh.models    import HoverTool, CustomJS, Slider
from bokeh.layouts   import column

import numpy as np

def d2r(x):
    return x/180 * np.pi

def r2d(x):
    return x / np.pi * 180

N_HOUR = 200
N_BETA = 200

if __name__ == "__main__":

    lat0  = 50
    day0 = 30
    gamma0 =  23.433333 * np.sin(2 * np.pi * (day0 + 284) / 365);


    hours = np.linspace(0, 24, N_HOUR)
    hra    = d2r(15 * (hours - 12)) 
    CH = np.cos(hra)
    SH = np.sin(hra)
    
    beta = np.linspace(0, 90, N_BETA)
    beta_r = d2r(beta)

    A = np.sin(d2r(gamma0)) * np.sin(d2r(lat0))
    B = np.cos(d2r(gamma0)) * np.cos(d2r(lat0)) 
    alpha = np.arcsin(A + B * np.cos(hra))
    msk = alpha >= 0

    
    TH = np.tan(hra)
    TA = np.tan(alpha.clip(0))
    X = 1 + TH**2 + TA**2

    vals = []
    for cb, sb in zip(np.cos(beta_r), np.sin(beta_r)):

        Y = sb * TA - cb * CH
        X = 1 + TA**2

        V_A = np.sqrt(1 - SH**2/X)
        V_B = np.sqrt(1 - Y**2/X)
        V_AB = Y*SH/X

        Yield = np.sqrt(1 - (V_AB / (V_A * V_B))**2) * V_B * V_A
        vals.append(100 * Yield[msk].sum() / len(hra))
        
        
    b_max = beta[np.argmax(vals)]
    source = ColumnDataSource(data=dict(x=beta, y=vals, cb=np.cos(beta_r), sb=np.sin(beta_r)))
    source_t = ColumnDataSource(data=dict(t=hra, ch=CH, sh=SH))
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
            
            var s = 0;
            for (var j=0; j < timing.t.length; j++) {
                const alpha = Math.asin(A + B*Math.cos(timing.t[j]))
                

                //var a = Math.sin(timing.b[i] + ax);
                if (alpha > 0) {
                    const TH = Math.tan(timing.t[j])
                    const TA = Math.tan(alpha)
                    
                    const Y = data.sb[i] * TA - data.cb[i] * timing.ch[j]
                    const X = 1 + TA**2

                    const V_A = Math.sqrt(1 - timing.sh[j]**2/X)
                    const V_B = Math.sqrt(1 - Y**2 / X)
                    const V_AB = Y*timing.sh[j] / X


                    const yield = Math.sqrt(1 - (V_AB / (V_A * V_B))**2) * V_B * V_A

                    s = s + yield;
                }
            }
            data.y[i] = 100 * s / timing.t.length;
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

    output_file("../html/yield_day_fixed_panel_norot.html", title="Average Yield over a day for fixed panel.")
    show(column(p, slider_lat, slider_day))
    

