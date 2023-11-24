from bokeh.embed import components

def get_plot_limits(Y_lst):
    """
    Get maximal range for the given list for x and y.
    """
    x1, y1 = np.max(list(map(lambda Y: Y.max(axis=0), Y_lst)), axis=0)
    x0, y0 = np.min(list(map(lambda Y: Y.min(axis=0), Y_lst)), axis=0)

    #return x0, x1, y0, y1

    dx = x1 - x0
    dy = y1 - y0
    dd = max(dx, dy) * 1.05 / 2
    mux = (x0 + x1) / 2
    muy = (y0 + y1) / 2


    return mux-dd, mux+dd, muy-dd, muy+dd



def remove_axis(p):
    """
    Remove grid and make axis invisible
    """
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
    p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
    p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
    p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks



def save_bokeh_to_script(layout, path):
    """
    Creates div and script to embed the figure in an HTML page
    Two files:
        - xxx_div.txt
        - xxx_script.txt

    Note: script need to be embedded within two <html> balises


    :param layout: final figure that will be showed
    :param path: save location
    :rparam: None
    """

    script, div = components(layout)

    with open(path + "_script.txt", "w") as fp:
        #fp.write("<html>" + script + "</html>")
        fp.write(script)

    with open(path + "_div.txt", "w") as fp:
        fp.write(div)




