from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .label.standard._basic_drawer import BDL_Bar_Drawer
from .label.standard._frame_drawer import FDL_Bar_Drawer
from .label.category._basic_drawer import CBDL_Bar_Drawer
from .label.category._frame_drawer import CFDL_Bar_Drawer


@dataclass(frozen=True)
class StandardBarLabelDrawer:
    ax: Axes
    fig: Figure
    horizontal: bool

    @property
    def basic(self) -> BDL_Bar_Drawer:
        return BDL_Bar_Drawer(
            ax=self.ax,
            horizontal=self.horizontal,
        )

    @property
    def framed(self) -> FDL_Bar_Drawer:
        return FDL_Bar_Drawer(
            ax=self.ax,
            fig=self.fig,
            horizontal=self.horizontal,
        )


@dataclass(frozen=True)
class CategoryBarLabelDrawer:
    ax: Axes
    fig: Figure
    horizontal: bool

    @property
    def basic(self) -> CBDL_Bar_Drawer:
        return CBDL_Bar_Drawer(
            ax=self.ax,
            horizontal=self.horizontal,
        )

    @property
    def framed(self) -> CFDL_Bar_Drawer:
        return CFDL_Bar_Drawer(
            ax=self.ax,
            fig=self.fig,
            horizontal=self.horizontal,
        )


@dataclass(frozen=True)
class BarLabelDrawer:
    ax: Axes
    fig: Figure
    horizontal: bool

    @property
    def standard(self) -> StandardBarLabelDrawer:
        return StandardBarLabelDrawer(
            ax=self.ax,
            fig=self.fig,
            horizontal=self.horizontal,
        )

    @property
    def category(self) -> CategoryBarLabelDrawer:
        return CategoryBarLabelDrawer(
            ax=self.ax,
            fig=self.fig,
            horizontal=self.horizontal,
        )
