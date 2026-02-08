"""Expose a unified entry point for bar chart stylers."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ._border import BarBorderDrawer
from ._color import BarColorDrawer
from ._label import BarLabelDrawer


@dataclass(frozen=True)
class BarStyleDrawer:
    """Group all bar styling drawers under a single interface.

    Attributes:
        ax (Axes): Target axes used by created drawers.
        fig (Figure): Figure used by drawers that require font/point metrics.
        horizontal (bool): Whether the bars are horizontal.
        legend (str | None): Optional legend key used by color and border
            drawers to scope styling.
    """

    ax: Axes
    fig: Figure
    horizontal: bool
    legend: str | None

    @property
    def color(self) -> BarColorDrawer:
        """Return a drawer for bar fill/color styling.

        Returns:
            BarColorDrawer: A new drawer instance configured for this Axes.
        """
        return BarColorDrawer(
            ax=self.ax,
            horizontal=self.horizontal,
            legend=self.legend,
        )

    @property
    def border(self) -> BarBorderDrawer:
        """Return a drawer for bar border/edge styling.

        Returns:
            BarBorderDrawer: A new drawer instance configured for this Axes.
        """
        return BarBorderDrawer(
            ax=self.ax,
            horizontal=self.horizontal,
            legend=self.legend,
        )

    @property
    def label(self) -> BarLabelDrawer:
        """Return a drawer for bar data labels.

        Returns:
            BarLabelDrawer: A new drawer instance configured for this Axes/Figure.
        """
        return BarLabelDrawer(
            ax=self.ax,
            fig=self.fig,
            horizontal=self.horizontal,
        )
