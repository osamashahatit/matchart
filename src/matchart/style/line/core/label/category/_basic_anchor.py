from matplotlib.axes import Axes

from ..._utils import LineStyleHelper


class CBDL_Line_Anchor:
    def __init__(self, ax: Axes, tick_label: str):
        self.ax = ax
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
        return self.get_x()

    @property
    def y(self) -> float:
        return self.get_y()
