"""Expose the primary public entry point for bar chart stylers."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matchart.style.base.main import BaseStyler

from .core.main import BarStyleDrawer


@dataclass(frozen=True)
class BarStyler:
    """Provide top-level styling access for bar charts.

    BarStyler is intended as the primary user-facing object when styling bar
    charts. It exposes:
    - base: figure/axes-level styling (grids, spines, etc.)
    - bars: bar-specific styling (colors, borders, labels)

    Attributes:
        ax (Axes): Target axes to be styled.
        fig (Figure): Figure associated with the axes.
        horizontal (bool): Whether the bars are horizontal.
        legend (str | None): Optional legend key used to scope bar styling.
    """

    ax: Axes
    fig: Figure
    horizontal: bool
    legend: str | None

    @property
    def base(self) -> BaseStyler:
        """Return the base (figure/axes-level) styler.

        Returns:
            BaseStyler: A new base styler instance bound to this Axes/Figure.
        """
        return BaseStyler(ax=self.ax, fig=self.fig)

    @property
    def bars(self) -> BarStyleDrawer:
        """Return the bar-specific styler.

        Returns:
            BarStyleDrawer: A new bar style drawer configured for this Axes.
        """
        return BarStyleDrawer(
            ax=self.ax,
            fig=self.fig,
            horizontal=self.horizontal,
            legend=self.legend,
        )
