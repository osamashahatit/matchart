"""Expose a unified entry point for line chart data label drawers."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .label.category._basic_drawer import CBDL_Line_Drawer
from .label.category._frame_drawer import CFDL_Line_Drawer
from .label.standard._basic_drawer import BDL_Line_Drawer
from .label.standard._frame_drawer import FDL_Line_Drawer


@dataclass(frozen=True)
class StandatdLineLabelDrawer:
    """Group standard (per-point) line label drawers.

    Attributes:
        ax (Axes): Target axes used by created drawers.
        fig (Figure): Figure used by drawers that require font/point metrics.
    """

    ax: Axes
    fig: Figure

    @property
    def basic(self) -> BDL_Line_Drawer:
        """Return a drawer for basic (unframed) point labels.

        Returns:
            BDL_Line_Drawer: A new drawer instance configured for this Axes.
        """
        return BDL_Line_Drawer(ax=self.ax)

    @property
    def framed(self) -> FDL_Line_Drawer:
        """Return a drawer for framed point labels.

        Returns:
            FDL_Line_Drawer: A new drawer instance configured for this Axes/Figure.
        """
        return FDL_Line_Drawer(ax=self.ax, fig=self.fig)


@dataclass(frozen=True)
class CategoryLineLabelDrawer:
    """Group category (per-tick aggregate) line label drawers.

    Category drawers typically compute an aggregate (e.g., totals across series)
    for each tick label and draw one label per category.

    Attributes:
        ax (Axes): Target axes used by created drawers.
        fig (Figure): Figure used by framed drawers for font/point metrics.
    """

    ax: Axes
    fig: Figure

    @property
    def basic(self) -> CBDL_Line_Drawer:
        """Return a drawer for basic (unframed) category labels.

        Returns:
            CBDL_Line_Drawer: A new drawer instance configured for this Axes.
        """
        return CBDL_Line_Drawer(ax=self.ax)

    @property
    def framed(self) -> CFDL_Line_Drawer:
        """Return a drawer for framed category labels.

        Returns:
            CFDL_Line_Drawer: A new drawer instance configured for this Axes/Figure.
        """
        return CFDL_Line_Drawer(ax=self.ax, fig=self.fig)


@dataclass(frozen=True)
class LineLabelDrawer:
    """Top-level facade for line-chart data label drawers.

    Attributes:
        ax (Axes): Target axes used by created drawers.
        fig (Figure): Figure used by framed drawers for font/point metrics.
    """

    ax: Axes
    fig: Figure

    @property
    def standard(self) -> StandatdLineLabelDrawer:
        """Access standard (per-point) line label drawers.

        Returns:
            StandatdLineLabelDrawer: Group containing basic and framed drawers.
        """
        return StandatdLineLabelDrawer(ax=self.ax, fig=self.fig)

    @property
    def category(self) -> CategoryLineLabelDrawer:
        """Access category (per-tick aggregate) line label drawers.

        Returns:
            CategoryLineLabelDrawer: Group containing basic and framed drawers.
        """
        return CategoryLineLabelDrawer(ax=self.ax, fig=self.fig)
