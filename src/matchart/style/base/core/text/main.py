"""Expose high-level text styling helpers."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .core._title import TitleDrawer


@dataclass
class TextStyler:
    """Facade for text-related styling on a Matplotlib Axes."""

    ax: Axes
    fig: Figure

    @property
    def title(self) -> TitleDrawer:
        """Access the Axes title styler.

        Returns:
            TitleDrawer: Helper for drawing and styling the Axes title,
            including font, color, alignment, and point-based offsets.
        """
        return TitleDrawer(ax=self.ax, fig=self.fig)
