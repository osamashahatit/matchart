from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .core._title import TitleDrawer


@dataclass
class TextStyler:
    ax: Axes
    fig: Figure

    @property
    def title(self) -> TitleDrawer:
        return TitleDrawer(ax=self.ax, fig=self.fig)
