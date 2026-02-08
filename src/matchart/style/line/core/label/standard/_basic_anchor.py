"""Compute anchor points for line chart standard basic data labels"""

import numpy as np
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from matchart.style.line.core._utils import LineStyleHelper


class BDL_Line_Anchor:
    """Resolve anchor coordinates for a basic data label on a line chart.

    This class computes the (x, y) position of a label corresponding to a
    specific tick label on a given Line2D object.

    Attributes:
        ax (Axes): Matplotlib Axes containing the line.
        line (Line2D): Line artist providing y-data values.
        tick_label (str): X-axis tick label identifying the target point.
    """

    def __init__(self, ax: Axes, line: Line2D, tick_label: str):
        """
        Args:
            ax (Axes): Axes containing the line and x-axis ticks.
            line (Line2D): Line artist whose data will be labeled.
            tick_label (str): X-axis tick label used to locate the data point.
        """
        self.ax = ax
        self.line = line
        self.tick_label = tick_label

    def get_x(self) -> float:
        """Return the x-coordinate corresponding to the tick label.

        Returns:
            float: X-axis data coordinate for the given tick label.

        Raises:
            ValueError: If the tick label does not exist on the Axes.
        """
        tick_labels = LineStyleHelper(ax=self.ax).get_tick_labels()
        index = tick_labels.index(self.tick_label)
        x_ticks = list(self.ax.get_xticks())
        return float(x_ticks[index])

    def get_y(self) -> float:
        """Return the y-coordinate from the line at the tick label index.

        Returns:
            float: Y-value from the line's data corresponding to the tick.

        Raises:
            ValueError: If the tick label does not exist on the Axes.
            IndexError: If the line does not have a y-value at that index.
        """
        tick_labels = LineStyleHelper(ax=self.ax).get_tick_labels()
        index = tick_labels.index(self.tick_label)
        y_data = np.asarray(self.line.get_ydata(), dtype=float)
        return float(y_data[index])

    @property
    def x(self) -> float:
        """float: X-coordinate of the label anchor."""
        return self.get_x()

    @property
    def y(self) -> float:
        """float: Y-coordinate of the label anchor."""
        return self.get_y()
