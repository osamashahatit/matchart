"""Style fill between area."""

from typing import Any

from matplotlib.axes import Axes
from matplotlib.collections import FillBetweenPolyCollection
from matplotlib.colors import to_rgba

from ._utils import AreaYielder, LineStyleHelper


class AreaStyler:
    """Apply face (fill) styling to a single fill_between area artist."""

    def __init__(self, area: FillBetweenPolyCollection) -> None:
        """
        Args:
            area (FillBetweenPolyCollection): The area artist to style.
        """
        self.area = area

    def set_area_color(self, color: str | None) -> None:
        """Set the area face color while preserving the current alpha channel.

        Args:
            color (str | None): Matplotlib-compatible color string. If None,
                no change is applied.
        """
        if color is not None:
            current_facecolor: Any = self.area.get_facecolor()
            current_alpha = current_facecolor[0][3]
            r, g, b, _ = to_rgba(color)
            self.area.set_facecolor((r, g, b, current_alpha))

    def set_area_alpha(self, alpha: float | None) -> None:
        """Override the alpha channel of the area face color.

        Args:
            alpha (float | None): Alpha value in [0.0, 1.0]. If None, no change
                is applied.
        """
        # Reset global alpha so per-channel RGBA values are respected.
        self.area.set_alpha(None)

        if alpha is not None:
            facecolor: Any = self.area.get_facecolor()
            r: float = facecolor[0][0]
            g: float = facecolor[0][1]
            b: float = facecolor[0][2]
            self.area.set_facecolor((r, g, b, alpha))


class AreaDrawer:
    """Apply face color/alpha styling across fill_between areas on an Axes."""

    def __init__(self, ax: Axes, legend: str | None) -> None:
        """
        Args:
            ax (Axes): Axes that already contains fill_between area artists.
            legend (str | None): When not None, enables legend-based mapping
                behavior (dict-only inputs) for draw(). The value is used as a
                presence flag.
        """
        self.ax = ax
        self.legend = legend
        self.helper = LineStyleHelper(ax=self.ax)

    def _style(self, area: FillBetweenPolyCollection) -> AreaStyler:
        """Create an AreaStyler for a given area artist."""
        return AreaStyler(area=area)

    def draw(
        self,
        color: str | dict[str, str] | None = None,
        alpha: float | dict[str, float] | None = None,
    ) -> None:
        """Set area face color and alpha using scalar or legend-mapped inputs.

        In legend mode (legend is not None), properties must be provided as
        dictionaries mapping legend labels to values. Otherwise, properties are
        applied uniformly to all areas.

        Args:
            color (str | dict[str, str] | None): Area face color specification:
              - str: apply one color to all areas (legend=None only).
              - dict[str, str]: map legend labels to colors (legend mode).
            alpha (float | dict[str, float] | None): Area alpha specification:
              - float: apply one alpha to all areas (legend=None only).
              - dict[str, float]: map legend labels to alpha values
                (legend mode).

        Raises:
            TypeError: If legend is set and a scalar is provided instead of a
                dict, or if legend is not set and a dict is provided.

        Notes:
            This method mutates FillBetweenPolyCollection artists in place and
            does not return self (not chainable).
        """
        areas = AreaYielder(ax=self.ax)

        if self.legend is not None:
            # Area color (legend-mapped)
            if isinstance(color, str):
                raise TypeError("Area color must be a dictionary when legend is set.")
            if isinstance(color, dict):
                self.helper.validate_legend_entry(mapping=color)
                for area, color in areas.map_legend(property=color):
                    self._style(area=area).set_area_color(color=color)

            # Area alpha (legend-mapped)
            if isinstance(alpha, float):
                raise TypeError("Area alpha must be a dictionary when legend is set.")
            if isinstance(alpha, dict):
                self.helper.validate_legend_entry(mapping=alpha)
                for area, alpha in areas.map_legend(property=alpha):
                    self._style(area=area).set_area_alpha(alpha=alpha)

        if self.legend is None:
            # Area color (uniform)
            if isinstance(color, dict):
                raise TypeError("Area color must be a string when legend is not set.")
            if isinstance(color, str):
                for area in areas.standard():
                    self._style(area=area).set_area_color(color=color)

            # Area alpha (uniform)
            if isinstance(alpha, dict):
                raise TypeError("Area alpha must be a float when legend is not set.")
            if isinstance(alpha, float):
                for area in areas.standard():
                    self._style(area=area).set_area_alpha(alpha=alpha)
