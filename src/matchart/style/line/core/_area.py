from typing import Any
from matplotlib.axes import Axes
from matplotlib.collections import FillBetweenPolyCollection
from matplotlib.colors import to_rgba

from ._utils import LineStyleHelper, AreaGenerator


class AreaStyler:

    def __init__(self, area: FillBetweenPolyCollection) -> None:
        self.area = area

    def set_area_color(self, color: str | None) -> None:

        if color is not None:
            current_facecolor: Any = self.area.get_facecolor()
            current_alpha = current_facecolor[0][3]
            r, g, b, _ = to_rgba(color)
            self.area.set_facecolor((r, g, b, current_alpha))

    def set_area_alpha(self, alpha: float | None) -> None:

        self.area.set_alpha(None)
        if alpha is not None:
            facecolor: Any = self.area.get_facecolor()
            r: float = facecolor[0][0]
            g: float = facecolor[0][1]
            b: float = facecolor[0][2]
            self.area.set_facecolor((r, g, b, alpha))


class AreaDrawer:

    def __init__(self, ax: Axes, legend: str | None) -> None:
        self.ax = ax
        self.legend = legend
        self.help = LineStyleHelper(ax=self.ax)

    def _style(self, area: FillBetweenPolyCollection) -> AreaStyler:
        return AreaStyler(area=area)

    def draw(
        self,
        color: str | dict[str, str] | None = None,
        alpha: float | dict[str, float] | None = None,
    ) -> None:
        """
        Set area properties.

        Parameters
        ----------
        color : str | dict[str, str] | None. Default is None.
            Area color as a single string or a dictionary mapping legend labels to colors.
        alpha : float | dict[str, float] | None. Default is None.
            Area alpha as a single float or a dictionary mapping legend labels to alpha values.
        """

        areas = AreaGenerator(ax=self.ax)

        if self.legend is not None:
            # Area color
            if isinstance(color, str):
                raise TypeError("Area color must be a dictionary when legend is set.")
            if isinstance(color, dict):
                self.help.validate_legend_entry(dict=color)
                for area, color in areas.map_legend(property=color):
                    self._style(area=area).set_area_color(color=color)
            # Area alpha
            if isinstance(alpha, float):
                raise TypeError("Area alpha must be a dictionary when legend is set.")
            if isinstance(alpha, dict):
                self.help.validate_legend_entry(dict=alpha)
                for area, alpha in areas.map_legend(property=alpha):
                    self._style(area=area).set_area_alpha(alpha=alpha)

        if self.legend is None:
            # Area color
            if isinstance(color, dict):
                raise TypeError("Area color must be a string when legend is not set.")
            if isinstance(color, str):
                for area in areas.standard():
                    self._style(area=area).set_area_color(color=color)
            # Area alpha
            if isinstance(alpha, dict):
                raise TypeError("Area alpha must be a float when legend is not set.")
            if isinstance(alpha, float):
                for area in areas.standard():
                    self._style(area=area).set_area_alpha(alpha=alpha)
