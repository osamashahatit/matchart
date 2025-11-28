from dataclasses import dataclass
from matplotlib.axes import Axes

from ._label import AxisLabelDrawer
from ._range import AxisRangeDrawer
from ._tick import AxisTickSelector


@dataclass
class AxisLabel:
    ax: Axes

    @property
    def x(self) -> AxisLabelDrawer:
        return AxisLabelDrawer(axis=self.ax.xaxis)

    @property
    def y(self) -> AxisLabelDrawer:
        return AxisLabelDrawer(axis=self.ax.yaxis)


@dataclass
class AxisRange:
    ax: Axes

    @property
    def x(self) -> AxisRangeDrawer:
        return AxisRangeDrawer(
            limit_getter=self.ax.get_xlim,
            limit_setter=self.ax.set_xlim,
        )

    @property
    def y(self) -> AxisRangeDrawer:
        return AxisRangeDrawer(
            limit_getter=self.ax.get_ylim,
            limit_setter=self.ax.set_ylim,
        )


@dataclass
class AxisTick:
    ax: Axes

    @property
    def x(self) -> AxisTickSelector:
        return AxisTickSelector(axis=self.ax.xaxis)

    @property
    def y(self) -> AxisTickSelector:
        return AxisTickSelector(axis=self.ax.yaxis)
