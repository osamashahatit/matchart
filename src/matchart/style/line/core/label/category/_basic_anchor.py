"""Compute anchor points for line chart category basic data labels"""

from matplotlib.axes import Axes

from matchart.style.line.core._utils import LineStyleHelper


class CBDL_Line_Anchor:
    """Resolve anchor coordinates for a category-level line label."""

    def __init__(self, ax: Axes, tick_label: str):
        """
        Args:
            ax (Axes): Target axes used to read tick positions and view limits.
            tick_label (str): Text of the x-axis tick label identifying the
                category to anchor against.
        """
        self.ax = ax
        self.tick_label = tick_label

    def get_x(self) -> float:
        """Return the x coordinate for the given tick label.

        Returns:
            float: X coordinate corresponding to the tick label.

        Raises:
            ValueError: If the tick label is not present on the Axes.

        Notes:
            The x coordinate is resolved by matching the tick label index to
            the x-ticks returned by ax.get_xticks().
        """
        tick_labels = LineStyleHelper(ax=self.ax).get_tick_labels()
        index = tick_labels.index(self.tick_label)
        x_ticks = list(self.ax.get_xticks())
        return float(x_ticks[index])

    def get_y(self) -> float:
        """Return the y coordinate at the top of the current view.

        Returns:
            float: ax.get_ylim()[1].
        """
        return self.ax.get_ylim()[1]

    @property
    def x(self) -> float:
        """Return the resolved x anchor coordinate.

        Returns:
            float: X coordinate for the category label anchor.
        """
        return self.get_x()

    @property
    def y(self) -> float:
        """Return the resolved y anchor coordinate.

        Returns:
            float: Y coordinate for the category label anchor.
        """
        return self.get_y()
