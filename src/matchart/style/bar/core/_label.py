"""Expose a unified entry point for bar chart data label drawers."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .label.category._basic_drawer import CBDL_Bar_Drawer
from .label.category._frame_drawer import CFDL_Bar_Drawer
from .label.standard._basic_drawer import BDL_Bar_Drawer
from .label.standard._frame_drawer import FDL_Bar_Drawer


@dataclass(frozen=True)
class StandardBarLabelDrawer:
    """Provide access to per-bar (standard) label drawers.

    Attributes:
        ax (Axes): Target axes that contains bar artists.
        fig (Figure): Figure used by framed labels for measurement/conversion.
        horizontal (bool): Whether the bar chart is horizontal.
    """

    ax: Axes
    fig: Figure
    horizontal: bool

    @property
    def basic(self) -> BDL_Bar_Drawer:
        """Return a drawer for basic per-bar labels.

        Returns:
            BDL_Bar_Drawer: A new drawer instance configured for this Axes.
        """
        return BDL_Bar_Drawer(
            ax=self.ax,
            horizontal=self.horizontal,
        )

    @property
    def framed(self) -> FDL_Bar_Drawer:
        """Return a drawer for framed per-bar labels.

        Returns:
            FDL_Bar_Drawer: A new drawer instance configured for this Axes/Figure.
        """
        return FDL_Bar_Drawer(
            ax=self.ax,
            fig=self.fig,
            horizontal=self.horizontal,
        )


@dataclass(frozen=True)
class CategoryBarLabelDrawer:
    """Provide access to per-category (per-tick) label drawers.

    Category labels draw a single label per tick/category, typically a total
    across bar containers (unless a custom mapping is provided).

    Attributes:
        ax (Axes): Target axes that contains bar artists.
        fig (Figure): Figure used by framed labels for measurement/conversion.
        horizontal (bool): Whether the bar chart is horizontal.
    """

    ax: Axes
    fig: Figure
    horizontal: bool

    @property
    def basic(self) -> CBDL_Bar_Drawer:
        """Return a drawer for basic per-category labels.

        Returns:
            CBDL_Bar_Drawer: A new drawer instance configured for this Axes.
        """
        return CBDL_Bar_Drawer(
            ax=self.ax,
            horizontal=self.horizontal,
        )

    @property
    def framed(self) -> CFDL_Bar_Drawer:
        """Return a drawer for framed per-category labels.

        Returns:
            CFDL_Bar_Drawer: A new drawer instance configured for this Axes/Figure.
        """
        return CFDL_Bar_Drawer(
            ax=self.ax,
            fig=self.fig,
            horizontal=self.horizontal,
        )


@dataclass(frozen=True)
class BarLabelDrawer:
    """Top-level facade for bar label drawers.

    Use this facade to access either per-bar ("standard") drawers or
    per-category ("category") drawers.

    Attributes:
        ax (Axes): Target axes that contains bar artists.
        fig (Figure): Figure used by framed labels for measurement/conversion.
        horizontal (bool): Whether the bar chart is horizontal.
    """

    ax: Axes
    fig: Figure
    horizontal: bool

    @property
    def standard(self) -> StandardBarLabelDrawer:
        """Return the per-bar label drawer group.

        Returns:
            StandardBarLabelDrawer: Group of per-bar drawers.
        """
        return StandardBarLabelDrawer(
            ax=self.ax,
            fig=self.fig,
            horizontal=self.horizontal,
        )

    @property
    def category(self) -> CategoryBarLabelDrawer:
        """Return the per-category label drawer group.

        Returns:
            CategoryBarLabelDrawer: Group of per-category drawers.
        """
        return CategoryBarLabelDrawer(
            ax=self.ax,
            fig=self.fig,
            horizontal=self.horizontal,
        )
