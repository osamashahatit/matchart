from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matchart.style.base.main import BaseStyler
from .core.main import LineStyleDrawer


@dataclass(frozen=True)
class LineStyler:
    ax: Axes
    fig: Figure
    legend: str | None

    @property
    def base(self) -> BaseStyler:
        return BaseStyler(ax=self.ax, fig=self.fig)

    @property
    def lines(self) -> LineStyleDrawer:
        return LineStyleDrawer(ax=self.ax, fig=self.fig, legend=self.legend)
