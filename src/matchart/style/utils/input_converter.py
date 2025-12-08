from typing import Literal
from matplotlib.axes import Axes
from matplotlib.figure import Figure


class PointDataConverter:
    """Converter from points to data coordinates."""

    def __init__(self, ax: Axes, fig: Figure):
        self.ax = ax
        self.fig = fig

    def convert(self, axis: Literal["x", "y"], points: float) -> float:

        pixels = points * self.fig.dpi / 72.0
        bbox = self.ax.get_window_extent()

        if axis == "x":
            x_min, x_max = self.ax.get_xlim()
            data_range = x_max - x_min
            pixel_range = bbox.width
        else:
            y_min, y_max = self.ax.get_ylim()
            data_range = y_max - y_min
            pixel_range = bbox.height

        return (pixels / pixel_range) * data_range
