from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .label._basic_drawer import BarBDLDrawer
from .label._frame_drawer import BarFDLDrawer


from dataclasses import dataclass


@dataclass(frozen=True)
class BarLabelDrawer:
    ax: Axes
    fig: Figure
    horizontal: bool

    @property
    def basic(self) -> BarBDLDrawer:
        return BarBDLDrawer(
            ax=self.ax,
            horizontal=self.horizontal,
        )

    @property
    def framed(self) -> BarFDLDrawer:
        return BarFDLDrawer(
            ax=self.ax,
            fig=self.fig,
            horizontal=self.horizontal,
        )
