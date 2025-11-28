from dataclasses import dataclass
from matplotlib.axes import Axes

from ._color import BarColorDrawer


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
