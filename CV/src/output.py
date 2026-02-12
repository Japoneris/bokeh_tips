from pathlib import Path

from bokeh.embed import components
from bokeh.io import save
from bokeh.plotting import figure
from bokeh.resources import CDN


def save_standalone_html(plot: figure, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    save(plot, filename=str(path), resources=CDN, title="CV Timeline")


def save_components(plot: figure, path_prefix: str | Path) -> None:
    path_prefix = Path(path_prefix)
    path_prefix.parent.mkdir(parents=True, exist_ok=True)
    script, div = components(plot)
    Path(f"{path_prefix}_script.txt").write_text(script)
    Path(f"{path_prefix}_div.txt").write_text(div)
