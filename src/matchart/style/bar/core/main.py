from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ._color import BarColorDrawer
from ._border import BarBorderDrawer
from ._label import BarLabelDrawer


@dataclass(frozen=True)
class BarStyleDrawer:
    ax: Axes
    fig: Figure
    horizontal: bool
    legend: str | None

    @property
    def color(self) -> BarColorDrawer:
        return BarColorDrawer(
            ax=self.ax,
            horizontal=self.horizontal,
            legend=self.legend,
        )

    @property
    def border(self) -> BarBorderDrawer:
        return BarBorderDrawer(
            ax=self.ax,
            horizontal=self.horizontal,
            legend=self.legend,
        )

    @property
    def label(self) -> "BarLabelDrawer":
        return BarLabelDrawer(
            ax=self.ax,
            fig=self.fig,
            horizontal=self.horizontal,
        )
