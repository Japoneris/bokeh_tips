from datetime import date
from typing import Optional

from pydantic import BaseModel, model_validator


def date_to_float(d: str) -> float:
    """Convert a YYYY-MM-DD date string to a fractional year."""
    dt = date.fromisoformat(d)
    year_start = date(dt.year, 1, 1)
    year_end = date(dt.year + 1, 1, 1)
    fraction = (dt - year_start).days / (year_end - year_start).days
    return dt.year + fraction


class Experience(BaseModel):
    label: str
    start_date: str  # YYYY-MM-DD
    end_date: str  # YYYY-MM-DD
    lane: int
    category: str
    color: Optional[str] = None
    click: Optional[str] = None

    @model_validator(mode="after")
    def check_dates(self):
        if date.fromisoformat(self.end_date) <= date.fromisoformat(self.start_date):
            raise ValueError(
                f"end_date ({self.end_date}) must be after start_date ({self.start_date})"
            )
        return self

    def to_fractional_years(self) -> tuple[float, float]:
        return date_to_float(self.start_date), date_to_float(self.end_date)


class Event(BaseModel):
    label: str
    date: str  # YYYY-MM-DD
    lane: int
    category: str
    color: Optional[str] = None
    click: Optional[str] = None
    marker: str = "circle"

    def to_fractional_year(self) -> float:
        return date_to_float(self.date)


class CategoryStyle(BaseModel):
    line_color: str = "#5697B5"
    fill_color: str = "#8cc6bc"


class ChartSettings(BaseModel):
    horizontal_size: tuple[int, int] = (1000, 300)
    vertical_size: tuple[int, int] = (300, 1000)
    line_width: int = 10
    marker_size: int = 20
    marker_line_width: int = 5
    year_label_color: str = "#5697B5"
    year_grid_color: str = "#8cc6bc"
    year_grid_alpha: float = 0.2
    lane_spacing: float = 1.0
    url_pattern: str = "#@click"
    tools: str = "save,reset"


class CVData(BaseModel):
    settings: ChartSettings = ChartSettings()
    categories: dict[str, CategoryStyle] = {}
    experiences: list[Experience] = []
    events: list[Event] = []
