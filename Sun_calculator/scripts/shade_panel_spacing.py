"""

Find the optimal distance between two solar panels knowing tilt and declinaison angle.

Draw a solar panel and its shade.

"""


from bokeh.plotting  import ColumnDataSource, figure, output_file, show
from bokeh.models    import HoverTool, CustomJS, Slider
from bokeh.layouts   import column

import numpy as np

def d2r(x):
    return x/180*np.pi

def r2d(x):
    return x*180/np.pi


if __name__ == "__main__":
    
    p = figure(plot_width=700, plot_height=400,
            match_aspect=True, # X and Y same scale
            tools="pan,wheel_zoom,reset,save",
           title="Shade of a solar panel.")
    
    #hover = HoverTool(tooltips=[("(x, y)", '($sx, $sy)')])
    #p.add_tools(hover)


    # Remove ticks and grids
    p.xgrid.visible = False
    p.ygrid.visible = True

    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
    p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks

    #p.xgrid.minor_grid_line_alpha = 0.4
    #p.xgrid.grid_line_alpha = 0.7
    #p.xgrid.ticker = [i*0.5 for i in range(-5, 40)]
    p.xaxis.ticker = [i*0.5 for i in range(-5, 40)]


    panel_angle = 20 # degree
    panel_size  = 1  # size in m 
    sun_default = 60 # 50 total light, 30 half, 10 shade

    
    H = panel_size * np.sin(d2r(panel_angle))
    D = panel_size * np.cos(d2r(panel_angle))

    H1 = max(1, H)*2
    D2 = H1 / np.tan(d2r(sun_default))
    D1 = H / np.tan(d2r(sun_default))

    # Simple line
    dic_panel = {
            "x": [0, D],
            "y": [0, H],
            }

    # Big rectangle
    dic_soil = {
            "x": [-1, D+D1+1, D+D1+1, -1],
            "y": [0, 0, -0.1, -0.1],
            }

    # Sunny area
    dic_sun = {
            'x': [-1, 0, D, D+D1, D+D1+1, D+D1+1-D2, -1 -D2],  
            "y": [0, 0, H, 0, 0, H1, H1],
            }
    
    source_panel = ColumnDataSource(dic_panel)
    source_soil  = ColumnDataSource(dic_soil)
    source_sun   = ColumnDataSource(dic_sun)


    
    # Plot figures
    p.patch('x', 'y', name="ground", source=source_soil, 
            line_width=3, line_color="brown", fill_color="saddlebrown", line_alpha=0.7)

    p.patch('x', 'y', name="Sun", source=source_sun, 
            line_width=3, line_color="darkorange", fill_color="gold", line_alpha=0.7, alpha=0.4)

    p.line('x', 'y', name="wall", source=source_panel, 
            line_width=5, line_color="dimgray", line_alpha=0.7)


    # Define sliders
    slider_p_size  = Slider(start=0.25, end=20, value=panel_size, step=0.25, title="Panel size")
    slider_p_angle = Slider(start=0., end=90-0.5, value=panel_angle, step=0.25, title="Panel angle")
    slider_s_angle = Slider(start=0.5, end=90, value=sun_default,   step=0.25, title="Sun elevation angle.")
    
    

    # Define callbacks
    callback = CustomJS(args=dict(
        source_sun=source_sun,
        source_pan=source_panel,
        source_soil=source_soil,
        s_p_size = slider_p_size,
        s_p_angl = slider_p_angle,
        s_s_angl = slider_s_angle,
        ),
                        code="""
        const PI = 3.14159265359;
        const sun    = source_sun.data;
        const panel  = source_pan.data;
        const ground = source_soil.data;

        const alpha = s_s_angl.value / 180 * PI;
        const beta  = s_p_angl.value / 180 * PI;
        const S     = s_p_size.value;

        const H = S * Math.sin(beta);
        const D = S * Math.cos(beta);

        const H1 = Math.max(1, H)*2
        const D2 = H1 / Math.tan(alpha);
        const D1 = H / Math.tan(alpha);

        // Update

        panel.x = [0, D];
        panel.y = [0, H];

        ground.x = [-1, D+D1+1, D+D1+1, -1];
        ground.y = [0, 0, -0.1, -0.1];

        sun.x = [-1, 0, D, D+D1, D+D1+1, D+D1+1-D2, -1 -D2]
        sun.y =  [0, 0, H, 0, 0, H1, H1]



        source_sun.change.emit();
        source_pan.change.emit();
        source_soil.change.emit();
        """)
    
    slider_p_size.js_on_change('value', callback)
    slider_p_angle.js_on_change('value', callback)
    slider_s_angle.js_on_change('value', callback)




    output_file("../html/shade_solar_panel_spacing.html", title="Shade of a solar panel given panel and sun angles.")
    show(column(p, slider_p_size, slider_p_angle, slider_s_angle))

