from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matchart.style.base.main import BaseStyler

from .core.main import BarStyleDrawer


@dataclass(frozen=True)
class BarStyler:
    ax: Axes
    fig: Figure
    horizontal: bool
    legend: str | None

    @property
    def base(self) -> BaseStyler:
        return BaseStyler(ax=self.ax, fig=self.fig)

    @property
    def bars(self) -> BarStyleDrawer:
        return BarStyleDrawer(
            ax=self.ax,
            horizontal=self.horizontal,
            legend=self.legend,
        )
