from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matchart.style.base.main import BaseStyler


@dataclass(frozen=True)
class LineStyler:
    ax: Axes
    fig: Figure

    @property
    def base(self) -> BaseStyler:
        return BaseStyler(ax=self.ax, fig=self.fig)
