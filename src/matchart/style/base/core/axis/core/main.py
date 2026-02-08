"""Expose a structured facade for axis label, range, and tick styling."""

from dataclasses import dataclass

from matplotlib.axes import Axes

from ._label import AxisLabelDrawer
from ._range import AxisRangeDrawer
from ._tick import AxisTickSelector


@dataclass
class AxisLabel:
    """Provide x/y accessors for axis label styling.

    Attributes:
        ax (Axes): Matplotlib axes whose axis labels will be styled.
    """

    ax: Axes

    @property
    def x(self) -> AxisLabelDrawer:
        """Return the x-axis label drawer.

        Returns:
            AxisLabelDrawer: Drawer configured for ax.xaxis.
        """
        return AxisLabelDrawer(axis=self.ax.xaxis)

    @property
    def y(self) -> AxisLabelDrawer:
        """Return the y-axis label drawer.

        Returns:
            AxisLabelDrawer: Drawer configured for ax.yaxis.
        """
        return AxisLabelDrawer(axis=self.ax.yaxis)


@dataclass
class AxisRange:
    """Provide x/y accessors for axis range styling.

    Attributes:
        ax (Axes): Matplotlib axes whose limits may be modified.
    """

    ax: Axes

    @property
    def x(self) -> AxisRangeDrawer:
        """Return the x-axis range drawer.

        Returns:
            AxisRangeDrawer: Drawer configured for get_xlim/set_xlim.
        """
        return AxisRangeDrawer(
            limit_getter=self.ax.get_xlim,
            limit_setter=self.ax.set_xlim,
        )

    @property
    def y(self) -> AxisRangeDrawer:
        """Return the y-axis range drawer.

        Returns:
            AxisRangeDrawer: Drawer configured for get_ylim/set_ylim.
        """
        return AxisRangeDrawer(
            limit_getter=self.ax.get_ylim,
            limit_setter=self.ax.set_ylim,
        )


@dataclass
class AxisTick:
    """Provide x/y accessors for major/minor tick styling.

    Attributes:
        ax (Axes): Matplotlib axes whose ticks may be styled.
    """

    ax: Axes

    @property
    def x(self) -> AxisTickSelector:
        """Return the x-axis tick selector.

        Returns:
            AxisTickSelector: Tick selector configured for ax.xaxis.
        """
        return AxisTickSelector(axis=self.ax.xaxis)

    @property
    def y(self) -> AxisTickSelector:
        """Return the y-axis tick selector.

        Returns:
            AxisTickSelector: Tick selector configured for ax.yaxis.
        """
        return AxisTickSelector(axis=self.ax.yaxis)
