"""Expose a unified entry point for line chart stylers."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ._area import AreaDrawer
from ._label import LineLabelDrawer
from ._line import LineDrawer
from ._marker import MarkerDrawer


@dataclass(frozen=True)
class LineStyleDrawer:
    """Facade providing access to all line-related style drawers.

    Attributes:
        ax (Axes): Target axes containing line-based artists.
        fig (Figure): Figure associated with the axes (used by label drawers
            requiring font/point metrics).
        legend (str | None): Optional legend label used to filter or map styles
            in drawers that support legend-based selection.
    """

    ax: Axes
    fig: Figure
    legend: str | None

    @property
    def line(self) -> LineDrawer:
        """Access the line styling drawer.

        Returns:
            LineDrawer: Drawer for styling Line2D artists.
        """
        return LineDrawer(
            ax=self.ax,
            legend=self.legend,
        )

    @property
    def area(self) -> AreaDrawer:
        """Access the area (fill) styling drawer.

        Returns:
            AreaDrawer: Drawer for styling filled areas associated with lines.
        """
        return AreaDrawer(
            ax=self.ax,
            legend=self.legend,
        )

    @property
    def marker(self) -> MarkerDrawer:
        """Access the marker styling drawer.

        Returns:
            MarkerDrawer: Drawer for styling markers on line plots.
        """
        return MarkerDrawer(
            ax=self.ax,
            legend=self.legend,
        )

    @property
    def label(self) -> LineLabelDrawer:
        """Access the line data label drawer facade.

        Returns:
            LineLabelDrawer: Entry point for standard and category line labels,
            including basic and framed variants.
        """
        return LineLabelDrawer(ax=self.ax, fig=self.fig)
