"""Provide a unified facade for styling Matplotlib axes."""

from dataclasses import dataclass

from matplotlib.axes import Axes

from .core._margin import AxisMargin
from .core._spine import AxisSpine
from .core.main import AxisLabel, AxisRange, AxisTick


@dataclass
class AxisStyler:
    """Facade for styling all aspects of a Matplotlib axis.

    Attributes:
        ax (Axes): Matplotlib axes instance to be styled.
    """

    ax: Axes

    @property
    def label(self) -> AxisLabel:
        """Access axis label styling helpers.

        Returns:
            AxisLabel: Facade exposing x/y axis label drawers.
        """
        return AxisLabel(ax=self.ax)

    @property
    def margin(self) -> AxisMargin:
        """Access axis margin styling helper.

        Returns:
            AxisMargin: Helper for applying data-relative axis margins.
        """
        return AxisMargin(ax=self.ax)

    @property
    def range(self) -> AxisRange:
        """Access axis range (limits) styling helpers.

        Returns:
            AxisRange: Facade exposing x/y axis range drawers.
        """
        return AxisRange(ax=self.ax)

    @property
    def spine(self) -> AxisSpine:
        """Access axis spine styling helper.

        Returns:
            AxisSpine: Helper for showing, hiding, and styling axis spines.
        """
        return AxisSpine(ax=self.ax)

    @property
    def tick(self) -> AxisTick:
        """Access axis tick styling helpers.

        Returns:
            AxisTick: Facade exposing major/minor tick styling helpers for
            x and y axes.
        """
        return AxisTick(ax=self.ax)
