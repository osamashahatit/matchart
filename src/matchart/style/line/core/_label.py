from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .label.standard._basic_drawer import BDL_Line_Drawer
from .label.standard._frame_drawer import FDL_Line_Drawer


@dataclass(frozen=True)
class StandatdLineLabelDrawer:
    ax: Axes
    fig: Figure

    @property
    def basic(self) -> BDL_Line_Drawer:
        return BDL_Line_Drawer(ax=self.ax)

    @property
    def frame(self) -> FDL_Line_Drawer:
        return FDL_Line_Drawer(ax=self.ax, fig=self.fig)


@dataclass(frozen=True)
class LineLabelDrawer:
    ax: Axes
    fig: Figure

    @property
    def standard(self) -> StandatdLineLabelDrawer:
        return StandatdLineLabelDrawer(ax=self.ax, fig=self.fig)
