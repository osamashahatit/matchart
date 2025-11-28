from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.axis import Axis

from .core._grid import GridDrawer


@dataclass
class GridSelector:
    axis: Axis

    @property
    def major(self) -> GridDrawer:
        return GridDrawer(tick_getter=self.axis.get_major_ticks)

    @property
    def minor(self) -> GridDrawer:
        return GridDrawer(tick_getter=self.axis.get_minor_ticks)


@dataclass
class GridStyler:
    ax: Axes

    def __post_init__(self) -> None:
        self.ax.set_axisbelow(True)

    @property
    def x(self) -> GridSelector:
        return GridSelector(axis=self.ax.xaxis)

    @property
    def y(self) -> GridSelector:
        return GridSelector(axis=self.ax.yaxis)
