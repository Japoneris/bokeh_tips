from bokeh.io import show
from bokeh.models import ColumnDataSource, Grid, LinearAxis, MultiPolygons, Plot
from bokeh.models import CustomJS, Slider
from bokeh.models import Range1d
from bokeh.layouts import column, row

from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Div

import numpy as np




COLOR_1 = "chocolate"
COLOR_2 = "peru"
COLOR_3 = "sandybrown"
COLOR_4 = "sienna"

if False:
    # Test 
    COLOR_1 = "white"
    COLOR_2 = "white"
    COLOR_3 = "white"
    COLOR_4 = "white"
    

# CONFIG
R = 0.7
a = R
b = 1 - R
diag_a = np.sqrt(2 * a * a)
diag_b = np.sqrt(2 * b * b)

x = 2 * a + b
y = np.sqrt(x*x/2) - diag_b
z = diag_a - diag_b
L = y * 2 + 4 * diag_b + z

DD = diag_a + diag_b

# Figure setup

plot = figure(
    title=None, width=500, height=500,
    min_border=0, toolbar_location="above", tools="save,reset")#, output_backend="svg") # Bug if SVG. USe for blog only

plot.background_fill_color = None
plot.border_fill_color = None
plot.axis.visible = False

# Inner background setup
XS = [[0, 0, L, L]]
YS = [[0, L, L, 0]]
source_bg = ColumnDataSource(dict(xs=[[XS]], ys=[[YS]]))
glyph = MultiPolygons(xs="xs", ys="ys", line_width=1, fill_color=COLOR_3)
plot.add_glyph(source_bg, glyph)



# PART 1

lst0 = [[diag_a + diag_b/2, 2 * diag_a + diag_b],
      [diag_a + diag_b, 2 * diag_a + diag_b*1.5],
       [2*diag_a + diag_b*1.5, diag_a + diag_b],
       [2*diag_a + diag_b, diag_a + diag_b/2]
      ]

lst0.append(lst0[0])

XS = []
YS = []

for XX, YY in [[0,0], [1, 0], [0, 1], [1, 1], [-1, -1], [-1, 0], [0, -1], [-1, 1], [1, -1]]:

    XS.append([i[0]+XX*DD for i in lst0])
    YS.append([i[1]+YY*DD for i in lst0])
    
source_0 = ColumnDataSource(dict(xs=[[XS]], ys=[[YS]]))

glyph = MultiPolygons(xs="xs", ys="ys", line_width=1, fill_color=COLOR_1)
plot.add_glyph(source_0, glyph)

    

lst1 = [[diag_a/2, diag_a/2+diag_b/2],
      [1.5*diag_a + diag_b * 0.5, diag_a * 1.5 + diag_b],
      [1.5*diag_a + diag_b, diag_a * 1.5 + diag_b*0.5],
       [diag_a*0.5 + diag_b*0.5, diag_a*0.5]
      ]
lst1.append(lst1[0])


XS = []
YS = []


for XX, YY in [[0,0], [1, 0], [0, 1], [1, 1], [-1, 0], [0, -1], [-1, 1], [1, -1], [-1, -1], [2, 0], [2, 1], [2, 2], [1, 2], [0, 2]]:
    XS.append([i[0]+XX*DD for i in lst1])
    YS.append([i[1]+YY*DD for i in lst1])

source_1 = ColumnDataSource(dict(xs=[[XS]], ys=[[YS]]))

glyph = MultiPolygons(xs="xs", ys="ys", line_width=1, fill_color=COLOR_2)
plot.add_glyph(source_1, glyph)

    
    
# Corners
    
LX = [[[[y, 0, 0],  [L-y, L, L], [y, 0, 0], [L-y, L, L]]]]
LY = [[[[0, y, 0],  [0, y, 0], [L, L-y, L], [L, L-y, L]]]]

source_corner = ColumnDataSource(dict(xs=LX, ys=LY))
glyph = MultiPolygons(xs="xs", ys="ys", line_width=1, fill_color=COLOR_3)
plot.add_glyph(source_corner, glyph)


# Borders
LX = [[[[0, L+b, L+b, 0], [L, L+b, L+b, L], [L, L, -b, -b], [0, -b, -b, 0]]]]
LY = [[[[0, 0, -b, -b], [0, 0, L+b, L+b], [L, L+b, L+b, L], [-b, -b, L, L]]]]

source_border = ColumnDataSource(dict(xs=LX, ys=LY))
glyph = MultiPolygons(xs="xs", ys="ys", line_width=1, fill_color=COLOR_4)
plot.add_glyph(source_border, glyph)


# Background external

LX = [[[[-100, -100, 100, 100], [-b, -b, L+b, L+b]]]]
LY = [[[[-100, 100, 100, -100], [L+b, -b, -b, L+b]]]]

source_background = ColumnDataSource(dict(xs=LX, ys=LY))
glyph = MultiPolygons(xs="xs", ys="ys", line_width=1, fill_color="white")
plot.add_glyph(source_background, glyph)


#####################
# Slider definition #
#####################

slider_ratio = Slider(start=0.5, end=1, value=R, step=.01, title="Ratio")
slider_length = Slider(start=0.5, end=3, value=1, step=.01, title="Length")

callback = CustomJS(args=dict(source_border=source_border, 
                              source_corner=source_corner, 
                              sld=slider_ratio),
                    code="""
    const R = sld.value

    const a = R
    const b = 1 - R
    
    const Da = Math.sqrt(a*a*2)
    const Db = Math.sqrt(b*b*2)
    
    const x = 2 * a + b
    const y = Math.sqrt(x*x/2) - Db
    const z = Da - Db
    const L = y * 2 + 4 * Db + z


    // border
    source_border.data.xs = [[[[0, L+b, L+b, 0], [L, L+b, L+b, L], [L, L, -b, -b], [0, -b, -b, 0]]]]
    source_border.data.ys = [[[[0, 0, -b, -b], [0, 0, L+b, L+b], [L, L+b, L+b, L], [-b, -b, L, L]]]]
    source_border.change.emit();
    
    
    // corner
    source_corner.data.xs = [[[[y, 0, 0],  [L-y, L, L], [y, 0, 0], [L-y, L, L]]]]
    source_corner.data.ys = [[[[0, y, 0],  [0, y, 0], [L, L-y, L], [L, L-y, L]]]]
    source_corner.change.emit();
    
""")


callback_loop = CustomJS(args=dict(source=source_0, 
                              sld=slider_ratio),
                    code="""
    console.log("Bonjour")
    const R = sld.value;

    const a = R
    const b = 1 - R
    
    const Da = Math.sqrt(a*a*2)
    const Db = Math.sqrt(b*b*2)
    const DD = Da + Db
    
    const x = 2 * a + b
    const y = Math.sqrt(x*x/2) - Db
    const z = Da - Db
    const L = y * 2 + 4 * Db + z

    var XS = []
    var YS = []
    
    var pts = [[Da + Db/2, 2 * Da + Db],
      [Da + Db, 2 * Da + Db*1.5],
       [2*Da + Db*1.5, Da + Db],
       [2*Da + Db, Da + Db/2]
      ]
    pts.push(pts[0])
    
    for (var i=-1; i < 2; i++) {
        for (var j=-1; j < 2; j++) {
            var tmp_xs = [];
            var tmp_ys = [];
            
            for (var k=0; k < pts.length; k++) {
                tmp_xs.push(pts[k][0] + i * DD)
                tmp_ys.push(pts[k][1] + j * DD)
            }
            XS.push(tmp_xs)
            YS.push(tmp_ys)
        }
    }
    
    // update
    source.data.xs = [[XS]]
    source.data.ys = [[YS]]
    source.change.emit();
""")


callback_loop1 = CustomJS(args=dict(source=source_1, 
                              sld=slider_ratio),
                    code="""
    console.log("Bonjour 1")
    const R = sld.value;

    const a = R
    const b = 1 - R
    
    const Da = Math.sqrt(a*a*2)
    const Db = Math.sqrt(b*b*2)
    const DD = Da + Db
    
    const x = 2 * a + b
    const y = Math.sqrt(x*x/2) - Db
    const z = Da - Db
    const L = y * 2 + 4 * Db + z

    var XS = []
    var YS = []
    
    
    var pts = [[Da/2, Da/2+Db/2],
      [1.5*Da + Db * 0.5, Da * 1.5 + Db],
      [1.5*Da + Db, Da * 1.5 + Db*0.5],
       [Da*0.5 +Db*0.5, Da*0.5]
      ]
      
    pts.push(pts[0])
    
    for (var i=-1; i < 3; i++) {
        for (var j=-1; j < 3; j++) {
            var tmp_xs = [];
            var tmp_ys = [];
            
            for (var k=0; k < pts.length; k++) {
                tmp_xs.push(pts[k][0] + i * DD)
                tmp_ys.push(pts[k][1] + j * DD)
            }
            XS.push(tmp_xs)
            YS.push(tmp_ys)
        }
    }
    
    // update
    source.data.xs = [[XS]]
    source.data.ys = [[YS]]
    source.change.emit();
""")


callback_background = CustomJS(args=dict(source=source_background, 
                                         source_2=source_bg,
                              sld=slider_ratio),
                    code="""
    const R = sld.value;

    const a = R
    const b = 1 - R
    
    const Da = Math.sqrt(a*a*2)
    const Db = Math.sqrt(b*b*2)
    const DD = Da + Db
    
    const x = 2 * a + b
    const y = Math.sqrt(x*x/2) - Db
    const z = Da - Db
    const L = y * 2 + 4 * Db + z

    // update
    source.data.xs = [[[[-100, -100, 100, 100], [-b, -b, L+b, L+b]]]]
    source.data.ys = [[[[-100, 100, 100, -100], [L+b, -b, -b, L+b]]]]
    source.change.emit();
    
    source_2.data.xs = [[[[0, 0, L, L]]]]
    source_2.data.ys = [[[[0, L, L, 0]]]]
    source_2.change.emit();

""")

mydiv = Div(text="start")


callback_values = CustomJS(args=dict(div=mydiv, 
                              sld=slider_ratio,
                                    sld_l = slider_length),
                    code="""
    const R = sld.value;
    const L0 = sld_l.value;

    const a = R 
    const b = (1 - R)
    
    const Da = Math.sqrt(a*a*2)
    const Db = Math.sqrt(b*b*2)
    const DD = Da + Db
    
    const x = 2 * a + b
    const y = Math.sqrt(x*x/2) - Db
    const z = Da - Db
    const L = y * 2 + 4 * Db + z

    const ratio = L0 / (2 * b + L)


    // update
    div.text = "a = " + (a*ratio).toFixed(3) + "<br>" + "b = " + (b*ratio).toFixed(3) + "<br> L = " + L0  + "<br> y = " + (y * ratio).toFixed(3) + "<br> z = " + (z * ratio).toFixed(3) 
""")



slider_ratio.js_on_change('value', callback)
slider_ratio.js_on_change('value', callback_loop)
slider_ratio.js_on_change('value', callback_loop1)
slider_ratio.js_on_change('value', callback_background)
slider_ratio.js_on_change('value', callback_values)
slider_length.js_on_change('value', callback_values)




left, right, bottom, top = -b*2, L+b+b, -b*2, L+b*2
plot.x_range=Range1d(left, right)
plot.y_range=Range1d(bottom, top)



show(row([plot, column([slider_ratio, slider_length, mydiv])]))

