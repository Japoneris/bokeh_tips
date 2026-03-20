"""
The goal is to simulate 

- A house
- A tree

Parameters:

    - Sun angle
    - Tree height
    - House height
    - Tree distance

"""


from bokeh.plotting  import ColumnDataSource, figure, output_file, show
from bokeh.models    import HoverTool, CustomJS, Slider
from bokeh.layouts   import column

import numpy as np
import os


if __name__ == "__main__":
    

    p = figure(plot_width=700, plot_height=400,
            match_aspect=True, # X and Y same scale
            tools="pan,lasso_select,wheel_zoom,box_select,tap,reset,save",
           title="Shade of a tree over a wall VS sun angle.")
    
    # Remove ticks and grids
    p.xgrid.visible = False
    p.ygrid.visible = True

    #p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
    #p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels

    #p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

    p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
    p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks


    tree_height = 3
    wall_dist   = 4
    wall_height = 2
    sun_default = 60 # 50 total light, 30 half, 10 shade



    dic = {
        "x": [-0.5, -0.5, -2, -1, -1.5, -0.5, -1, 0, 1, 0.5, 1.5, 1, 2, 0.5, 0.5, -0.5],
        "y": [x / 4 for x in [0, 1, 1, 2, 2, 3, 3, 4, 3, 3, 2, 2, 1, 1, 0, 0]]
        }
    
    source_tree = ColumnDataSource({
        "x0": dic["x"],
        "y0": dic["y"],
        "x": dic["x"],
        "y": [tree_height * v for v in dic["y"]]
        })

    source_ground = ColumnDataSource({
        "x": [-2, 12, 12, -2],
        "y": [0, 0, -0.5, -0.5]
        })

    source_wall = ColumnDataSource({
        "x": [wall_dist for _ in range(2)],
        "y": [0, wall_height]
        })
    
    #t_sun = np.tan((90-sun_default) * np.pi / 180)
    t_sun = np.tan((sun_default) * np.pi / 180)
    x0 = -2 # Sun first point location
    y0 = tree_height + np.abs(x0) * t_sun # Height of sun at initial point
    x1 = tree_height / t_sun # Max distance of the light to the ground
    x2 = wall_height / t_sun + wall_dist # Distance from the wall if light on wall
    
    # Hauteur de la lumiere au niveau du mur
    y_light = tree_height - t_sun * wall_dist  

    dic_ray = {"x": [x0], "y": [y0]}
    if y_light < wall_height:
        # Le mur prend la lumiere
        x3 = x2+3 - y0 / t_sun
        if x1 > wall_dist: # Half light
            dic_ray["x"].extend([wall_dist, wall_dist, x2, x2+3, x3])
            dic_ray["y"].extend([y_light, wall_height, 0, 0, y0])

        else: # Full light
            dic_ray["x"].extend([x1, wall_dist, wall_dist, x2, x2+3, x3])
            dic_ray["y"].extend([0, 0, wall_height, 0, 0, y0])
        
        """
      x                  x
        x                x
        T x       xx     x
        T   x     x| x   x
        T     xxxxx|   xxx

        """
    else:
        # Le mur est à l'ombre
        x3 = x1+3 - y0 / t_sun
        dic_ray["x"].extend([x1, x1+3, x3])
        dic_ray["y"].extend([0,  0, y0])

    source_ray = ColumnDataSource(dic_ray)

    
    # Plot figures
    p.patch('x', 'y', name="tree", source=source_tree, 
            line_width=3, line_color="green", fill_color="green", line_alpha=0.7)
    
    p.patch('x', 'y', name="ground", source=source_ground, 
            line_width=3, line_color="brown", fill_color="saddlebrown", line_alpha=0.7)

    p.patch('x', 'y', name="rays", source=source_ray, 
            line_width=3, line_color="darkorange", fill_color="gold", line_alpha=0.7, alpha=0.4)

    p.line('x', 'y', name="wall", source=source_wall, 
            line_width=5, line_color="dimgray", line_alpha=0.7)

    # Define sliders
    slider_tree = Slider(start=0.5, end=50, value=tree_height, step=0.25, title="Tree height")
    slider_wall = Slider(start=0.5, end=50, value=wall_height, step=0.25, title="Wall height")
    slider_dist = Slider(start=0, end=100, value=wall_dist,   step=0.25, title="Wall-Tree distance")
    slider_sun  = Slider(start=1, end=89,  value=sun_default,   step=0.25, title="Sun angle")
    
    # Define callbacks
    callback = CustomJS(args=dict(source=source_tree,
        s_tree=slider_tree,
        ),
                        code="""
        const data = source.data;
        const v = s_tree.value;
        const vv = Math.sqrt(v);

        for (var i=0; i < data.x.length; i++){
            // data.x[i] = data.x0[i] * vv; /// With of the tree...
            data.y[i] = data.y0[i] * v;
        }

        source.change.emit();
        """)
    slider_tree.js_on_change('value', callback)


    callback = CustomJS(args=dict(source=source_wall,
        s_wall=slider_dist,
        ), code="""
        const data = source.data;
        const v = s_wall.value;

        for (var i=0; i < data.x.length; i++){
            data.x[i] = v;
        }
        source.change.emit();
        """)
    slider_dist.js_on_change('value', callback)

    callback = CustomJS(args=dict(source=source_wall,
        s_wall=slider_wall,
        ), code="""
        const data = source.data;
        data.y[1] = s_wall.value;
        source.change.emit();
        """)
    slider_wall.js_on_change('value', callback)



    callback = CustomJS(args=dict(source=source_ray,
        s_tree=slider_tree,
        s_wall=slider_wall,
        s_dist=slider_dist,
        s_sun=slider_sun,
        source_g=source_ground,
        ), code="""
        const data   = source.data;
        const tree_h = s_tree.value;
        const wall_h = s_wall.value;
        const wall_d = s_dist.value;
        const t_sun = Math.tan((s_sun.value) * 3.14159265359 / 180);
        
        const x0 = -2; // Sun first point location
        const y0 = tree_h - x0 * t_sun;
        const x1 = tree_h / t_sun; // Max distance of the light to the ground
        const x2 = wall_h / t_sun + wall_d; // # Distance from the wall if light on wall
        const y_light = tree_h - t_sun * wall_d;

        var lst_x = [x0]
        var lst_y = [y0]
        


        if (y_light < wall_h) {
            const x3 = x2+3 - y0 / t_sun;
            if (x1 > wall_d) { 
                //lumiere partielle sur le mur
                lst_x = lst_x.concat([wall_d, wall_d, x2, x2, x2+3, x3]);
                lst_y = lst_y.concat([y_light, wall_h, 0, 0, 0, y0]);
            
            } else { 
                // lumiere totale sur le mur
                lst_x = lst_x.concat([x1, wall_d, wall_d, x2, x2+3, x3])
                lst_y = lst_y.concat([0, 0, wall_h, 0, 0, y0])
            }
        } else {
            // Marche OK
            // Le mur est à l'ombre
            const x3 = x1+3 - y0 / t_sun;
            lst_x = lst_x.concat([x1, x1+3, x3, x3, x3, x3])
            lst_y = lst_y.concat([0,  0, y0,   y0, y0, y0])

        }
        

        //for (var i=0; i<data.x.length; i++) {
        //    data.x[i] = lst_x[i];
        //    data.y[i] = lst_y[i];        }

        data.x = lst_x;
        data.y = lst_y;

        // update floor
        const ground = source_g.data;
        const m = Math.max(...lst_x);
        ground.x = [-2, m+2, m+2, -2]

        source.change.emit();
        source_g.change.emit();
        """)
    
    slider_tree.js_on_change('value', callback)
    slider_wall.js_on_change('value', callback)
    slider_dist.js_on_change('value', callback)
    slider_sun.js_on_change('value', callback)



    output_file("../html/shade_tree_over_the_house.html", title="Tree shade on the house.")
    show(column(p, slider_tree, slider_dist, slider_wall, slider_sun))

