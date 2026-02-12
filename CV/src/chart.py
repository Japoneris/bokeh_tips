import math

from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    Label,
    OpenURL,
    Range1d,
    Segment,
    TapTool,
)
from bokeh.plotting import figure

from .models import CVData, CategoryStyle, date_to_float

_DEFAULT_STYLE = CategoryStyle()


def _resolve_color(item, categories: dict[str, CategoryStyle], attr: str) -> str:
    if item.color:
        return item.color
    style = categories.get(item.category, _DEFAULT_STYLE)
    return getattr(style, attr)


def build_chart(data: CVData, orientation: str = "horizontal", enable_tap: bool = False) -> figure:
    horizontal = orientation == "horizontal"
    s = data.settings

    width, height = s.horizontal_size if horizontal else s.vertical_size

    plot = figure(
        title=None,
        width=width,
        height=height,
        min_border=0,
        toolbar_location="above",
        tools=s.tools,
    )
    plot.background_fill_color = None
    plot.border_fill_color = None
    plot.axis.visible = False
    plot.xgrid.visible = False
    plot.ygrid.visible = False

    # Collect all date floats and lanes for range computation
    date_vals: list[float] = []
    lane_vals: list[int] = []

    for exp in data.experiences:
        y0, y1 = exp.to_fractional_years()
        date_vals.extend([y0, y1])
        lane_vals.append(exp.lane)

    for evt in data.events:
        date_vals.append(evt.to_fractional_year())
        lane_vals.append(evt.lane)

    if not date_vals:
        return plot

    date_min = math.floor(min(date_vals))
    date_max = math.floor(max(date_vals)) + 1
    
    # Add padding
    date_range = (date_min - 0.5, date_max + 0.5)
    lane_min = min(lane_vals) if lane_vals else 0
    lane_max = max(lane_vals) if lane_vals else 3
    lane_range = (lane_min - 2, lane_max + 1)

    if horizontal:
        plot.x_range = Range1d(date_range[0], date_range[1])
        plot.y_range = Range1d(lane_range[0], lane_range[1])
    else:
        # Vertical: dates on y-axis (negated so time flows down), lanes on x
        plot.x_range = Range1d(lane_range[0], lane_range[1])
        plot.y_range = Range1d(-date_range[1], -date_range[0])

    # Year grid lines and labels
    for year in range(date_min, date_max + 1):
        if horizontal:
            plot.line(
                x=[year, year],
                y=[lane_range[0], lane_range[1]],
                alpha=s.year_grid_alpha,
                color=s.year_grid_color,
            )
            label = Label(
                y=lane_range[0],
                x=year - 0.25,
                text=str(year),
                text_color=s.year_label_color,
            )
        else:
            plot.line(
                x=[lane_range[0], lane_range[1]],
                y=[-year, -year],
                alpha=s.year_grid_alpha,
                color=s.year_grid_color,
            )
            label = Label(
                x=lane_range[0],
                y=-year,
                text=str(year),
                text_color=s.year_label_color,
            )
        plot.add_layout(label)

    # Build experience data
    seg_data = {
        "d0": [],
        "d1": [],
        "lane": [],
        "label": [],
        "click": [],
        "line_color": [],
    }
    circle_data = {"d": [], "lane": [], "line_color": [], "fill_color": []}

    for exp in data.experiences:
        y0, y1 = exp.to_fractional_years()
        lc = _resolve_color(exp, data.categories, "line_color")
        fc = _resolve_color(exp, data.categories, "fill_color")

        if horizontal:
            seg_data["d0"].append(y0)
            seg_data["d1"].append(y1)
        else:
            seg_data["d0"].append(-y0)
            seg_data["d1"].append(-y1)

        seg_data["lane"].append(exp.lane)
        seg_data["label"].append(exp.label)
        seg_data["click"].append(exp.click or "")
        seg_data["line_color"].append(lc)

        # Endpoint circles
        for d_val in (y0, y1):
            circle_data["d"].append(d_val if horizontal else -d_val)
            circle_data["lane"].append(exp.lane)
            circle_data["line_color"].append(lc)
            circle_data["fill_color"].append(fc)

    # Draw segments
    seg_source = ColumnDataSource(seg_data)
    if horizontal:
        seg_glyph = Segment(
            x0="d0", y0="lane", x1="d1", y1="lane",
            line_color="line_color", line_width=s.line_width,
        )
    else:
        seg_glyph = Segment(
            x0="lane", y0="d0", x1="lane", y1="d1",
            line_color="line_color", line_width=s.line_width,
        )
    seg_renderer = plot.add_glyph(seg_source, seg_glyph)

    # Draw endpoint circles using plot.scatter (supports size in screen units)
    circle_source = ColumnDataSource(circle_data)
    if horizontal:
        plot.scatter(
            x="d", y="lane", source=circle_source,
            marker="circle",
            line_color="line_color", fill_color="fill_color",
            size=s.marker_size, line_width=s.marker_line_width,
        )
    else:
        plot.scatter(
            x="lane", y="d", source=circle_source,
            marker="circle",
            line_color="line_color", fill_color="fill_color",
            size=s.marker_size, line_width=s.marker_line_width,
        )

    # Draw events as scatter markers
    if data.events:
        evt_data = {
            "d": [],
            "lane": [],
            "label": [],
            "click": [],
            "line_color": [],
            "fill_color": [],
            "marker": [],
        }
        for evt in data.events:
            d = evt.to_fractional_year()
            lc = _resolve_color(evt, data.categories, "line_color")
            fc = _resolve_color(evt, data.categories, "fill_color")
            evt_data["d"].append(d if horizontal else -d)
            evt_data["lane"].append(evt.lane)
            evt_data["label"].append(evt.label)
            evt_data["click"].append(evt.click or "")
            evt_data["line_color"].append(lc)
            evt_data["fill_color"].append(fc)
            evt_data["marker"].append(evt.marker)

        evt_source = ColumnDataSource(evt_data)
        if horizontal:
            evt_renderer = plot.scatter(
                x="d", y="lane", marker="marker", source=evt_source,
                line_color="line_color", fill_color="fill_color",
                size=s.marker_size, line_width=s.marker_line_width,
            )
        else:
            evt_renderer = plot.scatter(
                x="lane", y="d", marker="marker", source=evt_source,
                line_color="line_color", fill_color="fill_color",
                size=s.marker_size, line_width=s.marker_line_width,
            )

    # Hover tool on segments
    hover = HoverTool(tooltips=[("Position", "@label")], renderers=[seg_renderer])
    plot.add_tools(hover)

    if enable_tap:
        tap = TapTool(
            renderers=[seg_renderer],
            callback=OpenURL(url=s.url_pattern, same_tab=True),
        )
        plot.add_tools(tap)

        if data.events:
            tap_evt = TapTool(
                renderers=[evt_renderer],
                callback=OpenURL(url=s.url_pattern, same_tab=True),
            )
            plot.add_tools(tap_evt)
    return plot
