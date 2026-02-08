"""Compute anchor points for line chart standard framed data labels"""

from dataclasses import dataclass

from matplotlib.axes import Axes

from matchart.style.line.core._utils import LineStyleHelper


@dataclass(frozen=True)
class FDL_Line_FrameDimension:
    """Describe the framed label's size and border thickness.

    Attributes:
        width (float): Frame width in data coordinates.
        height (float): Frame height in data coordinates.
        border_width_x (float): Border width contribution in the x direction.
        border_width_y (float): Border width contribution in the y direction.
    """

    width: float
    height: float
    border_width_x: float
    border_width_y: float

    @property
    def border_x(self) -> float:
        """Return half the x border width.

        Returns:
            float: border_width_x / 2.
        """
        return self.border_width_x / 2

    @property
    def border_y(self) -> float:
        """Return half the y border width.

        Returns:
            float: border_width_y / 2.
        """
        return self.border_width_y / 2


class FDL_Line_Anchor:
    """Resolve frame-aware anchor coordinates for a framed line label."""

    def __init__(
        self,
        ax: Axes,
        dimension: FDL_Line_FrameDimension,
        tick_label: str,
    ):
        """
        Args:
            ax (Axes): Target axes used to read tick positions and view limits.
            dimension (FDL_Line_FrameDimension): Frame size and border widths.
            tick_label (str): Text of the x-axis tick label identifying the
                category to anchor against.
        """
        self.ax = ax
        self.dimension = dimension
        self.tick_label = tick_label

    def get_x(self) -> float:
        """Return the raw x coordinate for the given tick label.

        Returns:
            float: X coordinate corresponding to the tick label.

        Raises:
            ValueError: If the tick label is not present on the Axes.
        """
        tick_labels = LineStyleHelper(ax=self.ax).get_tick_labels()
        index = tick_labels.index(self.tick_label)
        x_ticks = list(self.ax.get_xticks())
        return float(x_ticks[index])

    def get_y(self) -> float:
        """Return the raw y coordinate at the top of the current view.

        Returns:
            float: ax.get_ylim()[1].
        """
        return self.ax.get_ylim()[1]

    @property
    def x(self) -> float:
        """Return the frame-adjusted x anchor coordinate.

        Returns:
            float: X coordinate shifted left so the frame is centered on the
            tick position.
        """
        return self.get_x() - (self.dimension.width / 2) - self.dimension.border_x

    @property
    def y(self) -> float:
        """Return the frame-adjusted y anchor coordinate.

        Returns:
            float: Y coordinate shifted down so the frame sits inside the
            top plot edge.
        """
        return self.get_y() - self.dimension.height - self.dimension.border_y
