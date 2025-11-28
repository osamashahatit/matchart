from dataclasses import dataclass
from matplotlib.axes import Axes

from .core.main import AxisLabel
from .core._margin import AxisMargin
from .core.main import AxisRange
from .core._spine import AxisSpine
from .core.main import AxisTick


@dataclass
class AxisStyler:
    ax: Axes

    @property
    def label(self):
        return AxisLabel(ax=self.ax)

    @property
    def margin(self):
        return AxisMargin(ax=self.ax)

    @property
    def range(self):
        return AxisRange(ax=self.ax)

    @property
    def spine(self):
        return AxisSpine(ax=self.ax)

    @property
    def tick(self):
        return AxisTick(ax=self.ax)
