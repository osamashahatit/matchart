"""Provide accessors for styling major/minor grid lines on x/y axes."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.axis import Axis

from .core._grid import GridDrawer


@dataclass
class GridSelector:
    """Select major or minor grid styling helpers for a Matplotlib Axis.

    Attributes:
        axis (Axis): Matplotlib Axis (xaxis or yaxis) whose ticks provide
            the grid lines to be styled.
    """

    axis: Axis

    @property
    def major(self) -> GridDrawer:
        """Return the major grid drawer.

        Returns:
            GridDrawer: Drawer configured for axis.get_major_ticks().
        """
        return GridDrawer(tick_getter=self.axis.get_major_ticks)

    @property
    def minor(self) -> GridDrawer:
        """Return the minor grid drawer.

        Returns:
            GridDrawer: Drawer configured for axis.get_minor_ticks().
        """
        return GridDrawer(tick_getter=self.axis.get_minor_ticks)


@dataclass
class GridStyler:
    """Facade for styling grid lines on an Axes.

    Attributes:
        ax (Axes): Matplotlib axes whose grid lines will be styled.
    """

    ax: Axes

    def __post_init__(self) -> None:
        """Configure the axes so grids render beneath plot artists."""
        self.ax.set_axisbelow(True)

    @property
    def x(self) -> GridSelector:
        """Return grid selector for the x-axis.

        Returns:
            GridSelector: Selector bound to ax.xaxis.
        """
        return GridSelector(axis=self.ax.xaxis)

    @property
    def y(self) -> GridSelector:
        """Return grid selector for the y-axis.

        Returns:
            GridSelector: Selector bound to ax.yaxis.
        """
        return GridSelector(axis=self.ax.yaxis)
