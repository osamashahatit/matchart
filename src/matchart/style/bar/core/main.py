from dataclasses import dataclass
from matplotlib.axes import Axes

from ._color import BarColorDrawer
from ._border import BarBorderDrawer


@dataclass(frozen=True)
class BarStyleDrawer:
    ax: Axes
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
