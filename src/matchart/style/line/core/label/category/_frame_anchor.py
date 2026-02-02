from dataclasses import dataclass

from matplotlib.axes import Axes

from ..._utils import LineStyleHelper


@dataclass(frozen=True)
class CFDL_Line_FrameDimension:
    width: float
    height: float
    border_width_x: float
    border_width_y: float

    @property
    def border_x(self) -> float:
        return self.border_width_x / 2

    @property
    def border_y(self) -> float:
        return self.border_width_y / 2


class CFDL_Line_Anchor:
    def __init__(
        self,
        ax: Axes,
        dimension: CFDL_Line_FrameDimension,
        tick_label: str,
    ):
        self.ax = ax
        self.dimension = dimension
        self.tick_label = tick_label

    def get_x(self) -> float:
        tick_labels = LineStyleHelper(ax=self.ax).get_tick_labels()
        index = tick_labels.index(self.tick_label)
        x_ticks = list(self.ax.get_xticks())
        return float(x_ticks[index])

    def get_y(self) -> float:
        return self.ax.get_ylim()[1]

    @property
    def x(self) -> float:
        return self.get_x() - (self.dimension.width / 2) - self.dimension.border_x

    @property
    def y(self) -> float:
        return self.get_y() - self.dimension.height - self.dimension.border_y
