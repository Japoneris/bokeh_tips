# CV Timeline

Interactive timeline visualization of a CV/resume, built with [Bokeh](https://bokeh.org/). All data lives in a single JSON file — edit it to describe your own career, then generate standalone HTML charts or embeddable components for a blog.

![](/image.png)

## Quick start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python main.py
# -> output/cv_horizontal.html
# -> output/cv_vertical.html
```

Open the HTML files in a browser. Hover over a bar to see its label; click to jump to the corresponding anchor.

## CLI options

```
python main.py [OPTIONS]
```

| Flag | Default | Description |
|---|---|---|
| `--config PATH` | `config/cv_data.json` | Path to the JSON data file |
| `--orientation horizontal\|vertical` | both | Generate only one orientation |
| `--embed` | off | Also write `_script.txt` / `_div.txt` component files for blog embedding |
| `--output-dir DIR` | `output/` | Where to write generated files |

Examples:

```bash
# Horizontal only, with embed components
python main.py --orientation horizontal --embed

# Use a custom config
python main.py --config my_cv.json --output-dir docs/
```

## Configuration

Everything is in `config/cv_data.json`. The file has four sections:

### `settings` — chart appearance

```json
{
  "horizontal_size": [1000, 300],
  "vertical_size": [300, 1000],
  "line_width": 10,
  "marker_size": 20,
  "marker_line_width": 5,
  "year_label_color": "#5697B5",
  "year_grid_color": "#8cc6bc",
  "year_grid_alpha": 0.2,
  "url_pattern": "#@click",
  "tools": "save,reset"
}
```

- `horizontal_size` / `vertical_size` — `[width, height]` in pixels for each orientation.
- `url_pattern` — URL template for click navigation. `@click` is replaced by the experience's `click` field. Use `"#@click"` for same-page anchors or `"/cv#@click"` for a specific page.
- `tools` — Bokeh toolbar buttons (comma-separated). Common values: `save`, `reset`, `pan`, `wheel_zoom`.

All settings are optional — sensible defaults are used when omitted.

### `categories` — color themes

Map category names to a pair of colors:

```json
{
  "education": { "line_color": "#5697B5", "fill_color": "#8cc6bc" },
  "work":      { "line_color": "#D4764E", "fill_color": "#F2B880" }
}
```

Each experience/event references a category by name. You can also override colors per-item (see below).

### `experiences` — time spans

Each experience is a bar on the timeline:

```json
{
  "label": "Chimie ParisTech",
  "start_date": "2013-07-01",
  "end_date": "2016-07-01",
  "lane": 0,
  "category": "education",
  "click": "enscp"
}
```

| Field | Required | Description |
|---|---|---|
| `label` | yes | Tooltip text |
| `start_date` | yes | `YYYY-MM-DD` |
| `end_date` | yes | `YYYY-MM-DD` (must be after `start_date`) |
| `lane` | yes | Integer row. Use different lanes to avoid overlapping bars (e.g. 0 = education, 1 = studies, 2 = work, 3 = research) |
| `category` | yes | Key into the `categories` color map |
| `click` | no | Anchor ID substituted into `url_pattern` on click |
| `color` | no | Override the category color for this item |

### `events` — single-point markers

Events are rendered as a single marker (no bar), useful for milestones like graduation or a defense:

```json
{
  "label": "PhD Defense",
  "date": "2022-04-01",
  "lane": 3,
  "category": "research",
  "marker": "star",
  "click": "phd-thesis"
}
```

Same fields as experiences except `date` replaces `start_date`/`end_date`, and `marker` sets the shape. Supported marker shapes: `circle`, `diamond`, `star`, `triangle`, `square`, `hex`, `cross`, `x`, and others from Bokeh's marker types.

## Project structure

```
CV/
  config/
    cv_data.json        # All data + style settings
  src/
    models.py           # Pydantic data models with validation
    chart.py            # Bokeh chart rendering (build_chart)
    output.py           # HTML and component file saving
  main.py               # CLI entry point
  requirements.txt      # bokeh>=3.0, pydantic>=2.0
  output/               # Generated files (gitignored)
```

## Embedding in a blog

Use `--embed` to generate component files:

```bash
python main.py --embed
```

This produces `CV_horizontal_script.txt` and `CV_horizontal_div.txt` (and the vertical equivalents). Include the script tag and the div in your page's HTML to embed the chart without a full standalone Bokeh page. The page must load the Bokeh JS/CSS resources separately (via CDN or locally).

## Requirements

- Python 3.10+
- bokeh >= 3.0
- pydantic >= 2.0
