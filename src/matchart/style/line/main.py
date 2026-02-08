"""Expose the primary public entry point for line chart stylers."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matchart.style.base.main import BaseStyler

from .core.main import LineStyleDrawer


@dataclass(frozen=True)
class LineStyler:
    """Top-level facade for styling Matplotlib line charts.

    Attributes:
        ax (Axes): Target axes containing line artists.
        fig (Figure): Figure associated with the axes.
        legend (str | None): Optional legend key used to scope legend-aware
            styling operations.
    """

    ax: Axes
    fig: Figure
    legend: str | None

    @property
    def base(self) -> BaseStyler:
        """Access shared, chart-agnostic styling helpers.

        Returns:
            BaseStyler: Styling helpers for axes, grid, legend, and text.
        """
        return BaseStyler(ax=self.ax, fig=self.fig)

    @property
    def lines(self) -> LineStyleDrawer:
        """Access line-specific styling drawers.

        Returns:
            LineStyleDrawer: Facade exposing line, marker, area, and label
            styling helpers for line charts.
        """
        return LineStyleDrawer(
            ax=self.ax,
            fig=self.fig,
            legend=self.legend,
        )
