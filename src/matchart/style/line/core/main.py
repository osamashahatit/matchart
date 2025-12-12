from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ._line import LineDrawer
from ._area import AreaDrawer


@dataclass(frozen=True)
class LineStyleDrawer:
    ax: Axes
    fig: Figure
    legend: str | None

    @property
    def line(self) -> LineDrawer:
        return LineDrawer(
            ax=self.ax,
            legend=self.legend,
        )

    @property
    def area(self) -> AreaDrawer:
        return AreaDrawer(
            ax=self.ax,
            legend=self.legend,
        )
