from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .core.axis.main import AxisStyler
from .core.grid.main import GridStyler
from .core.legend.main import LegendStyler
from .core.text.main import TextStyler


@dataclass
class BaseStyler:

    ax: Axes
    fig: Figure

    @property
    def axis(self) -> AxisStyler:
        return AxisStyler(ax=self.ax)

    @property
    def grid(self) -> GridStyler:
        return GridStyler(ax=self.ax)

    @property
    def legend(self) -> LegendStyler:
        return LegendStyler(ax=self.ax)

    @property
    def text(self) -> TextStyler:
        return TextStyler(ax=self.ax, fig=self.fig)
