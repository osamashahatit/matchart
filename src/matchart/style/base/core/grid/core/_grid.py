from typing import Callable
from matplotlib.axis import Tick


class GridDrawer:

    def __init__(self, tick_getter: Callable[[], list[Tick]]) -> None:
        self.tick_getter = tick_getter

    def draw(
        self,
        show: bool = True,
        color: str | None = None,
        width: float | None = None,
        style: str | None = None,
        alpha: float | None = None,
    ) -> None:
        """
        Draw and style grid lines.

        Parameters
        ----------
        show : bool, default=True
            Show or hide the grid lines.
        color : str or None. Default is None.
            The color of the grid lines.
        width : float or None. Default is None.
            The width of the grid lines.
        style : str or None. Default is None.
            The style of the grid lines.
        alpha : float or None. Default is None.
            The transparency of the grid lines.

        Returns
        -------
        None
            The method modifies the object in place.
        """

        grid = [tick.gridline for tick in self.tick_getter()]
        for line in grid:
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
