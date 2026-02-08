"""Draw and style grid lines associated with axis ticks."""

from typing import Callable

from matplotlib.axis import Tick


class GridDrawer:
    """Apply visibility and styling to grid lines derived from ticks."""

    def __init__(self, tick_getter: Callable[[], list[Tick]]) -> None:
        """
        Args:
            tick_getter (Callable[[], list[Tick]]): Callable returning the
                ticks whose grid lines should be styled (e.g.,
                ax.xaxis.get_major_ticks).
        """
        self.tick_getter = tick_getter

    def draw(
        self,
        show: bool = True,
        color: str | None = None,
        width: float | None = None,
        style: str | None = None,
        alpha: float | None = None,
    ) -> None:
        """Show, hide, and style grid lines.

        Args:
            show (bool): Whether to display (`True`) or hide (`False`)
                the grid lines.
            color (str | None): Grid line color. Examples include named
                colors ("gray") or hex strings ("#cccccc").
            width (float | None): Grid line width in points.
            style (str | None): Grid line style (e.g. "-", "--", ":").
            alpha (float | None): Grid line transparency in the range
                [0.0, 1.0].

        Returns:
            None: Grid line objects are modified in place.
        """
        grid_lines = [tick.gridline for tick in self.tick_getter()]

        for line in grid_lines:
            if show:
                line.set_visible(show)

            if color is not None:
                line.set_color(color)

            if style is not None:
                line.set_linestyle(style)

            if width is not None:
                line.set_linewidth(width)

            if alpha is not None:
                line.set_alpha(alpha)
