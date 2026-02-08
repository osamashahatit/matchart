"""Provide a unified base styling facade for Matplotlib Axes."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .core.axis.main import AxisStyler
from .core.grid.main import GridStyler
from .core.legend.main import LegendStyler
from .core.text.main import TextStyler


@dataclass
class BaseStyler:
    """Root facade for shared Matplotlib chart styling."""

    ax: Axes
    fig: Figure

    @property
    def axis(self) -> AxisStyler:
        """Access axis-related styling helpers.

        Returns:
            AxisStyler: Styling helpers for axis labels, ranges, ticks,
            margins, and spines.
        """
        return AxisStyler(ax=self.ax)

    @property
    def grid(self) -> GridStyler:
        """Access grid styling helpers.

        Returns:
            GridStyler: Styling helpers for major and minor grid lines on
            both axes.
        """
        return GridStyler(ax=self.ax)

    @property
    def legend(self) -> LegendStyler:
        """Access legend styling helpers.

        Returns:
            LegendStyler: Styling helpers for legend frame, layout, labels,
            markers, position, and title.
        """
        return LegendStyler(ax=self.ax)

    @property
    def text(self) -> TextStyler:
        """Access text styling helpers.

        Returns:
            TextStyler: Styling helpers for Axes-level text elements such
            as titles.
        """
        return TextStyler(ax=self.ax, fig=self.fig)
