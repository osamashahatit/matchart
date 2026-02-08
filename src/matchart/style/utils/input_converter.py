"""Convert point-based sizes into data-coordinate distances.

Matplotlib styling often specifies sizes in points (e.g., line widths,
offsets, padding), while chart geometry is defined in data coordinates.
Bridging these two coordinate systems is non-trivial because the mapping
depends on figure DPI and the rendered axes size. This module provides a
small utility that converts a value expressed in points into the
equivalent distance in data units for a given axis, enabling consistent
visual spacing across different figure sizes and scales.
"""

from typing import Literal

from matplotlib.axes import Axes
from matplotlib.figure import Figure


class PointDataConverter:
    """Convert point-based distances into data-coordinate distances.

    This utility is typically used by style modules to translate visual
    spacing specified in points into equivalent distances along a data
    axis.
    """

    def __init__(self, ax: Axes, fig: Figure):
        """
        Args:
            ax (Axes): Target axes whose data limits define the conversion.
            fig (Figure): Figure used to determine DPI and pixel scaling.
        """
        self.ax = ax
        self.fig = fig

    def convert(self, axis: Literal["x", "y"], points: float) -> float:
        """Convert a distance from points to data units.

        Args:
            axis (Literal["x", "y"]): Axis along which to perform the
                conversion.
            points (float): Distance in typographic points (1/72 inch).

        Returns:
            float: Equivalent distance in data units along the chosen axis.
        """
        # Convert points to pixels using the figure DPI.
        pixels = points * self.fig.dpi / 72.0

        # Bounding box in display (pixel) coordinates.
        bbox = self.ax.get_window_extent()

        if axis == "x":
            x_min, x_max = self.ax.get_xlim()
            data_range = x_max - x_min
            pixel_range = bbox.width
        else:
            y_min, y_max = self.ax.get_ylim()
            data_range = y_max - y_min
            pixel_range = bbox.height

        # Scale pixels proportionally into data-coordinate distance.
        return (pixels / pixel_range) * data_range
