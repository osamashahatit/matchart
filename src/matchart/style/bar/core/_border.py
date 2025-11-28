from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.patches import Patch
from matplotlib.colors import to_rgba

from ._utils import (
    BarStyleHelper,
    BarPatchGenerator,
)


@dataclass
class BarBorderProperties:
    """Encapsulates properties for bar border."""

    color: str | list[str] | dict[str, str] | None
    alpha: float | None
    width: float | None
    style: str | None


@dataclass
class BarBorderExtremaProperties:
    """Encapsulates properties for extrema bar border."""

    min_color: str | None
    max_color: str | None
    alpha: float | None
    width: float | None
    style: str | None


class BarBorderStyler:

    def __init__(self, patch: Patch) -> None:
        self.patch = patch

    def set_border_color(self, color: str | None) -> None:
        """Set the border color of a patch."""

        self.patch.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.patch.set_edgecolor((r, g, b, a))

    def set_border_alpha(self, alpha: float | None) -> None:
        """Set the border alpha of a patch."""

        self.patch.set_alpha(None)
        if alpha is not None:
            r, g, b, _ = to_rgba(self.patch.get_edgecolor())
            self.patch.set_edgecolor((r, g, b, alpha))

    def set_border_width(self, width: float | None) -> None:
        """Set the border width of a patch."""

        if width is not None:
            self.patch.set_linewidth(width)

    def set_border_style(self, style: str | None) -> None:
        """Set the border style of a patch."""

        if style is not None:
            self.patch.set_linestyle(style)


class BarBorderDrawer:

    def __init__(self, ax: Axes, horizontal: bool, legend: str | None) -> None:
        self.ax = ax
        self.horizontal = horizontal
        self.legend = legend
        self.help = BarStyleHelper(ax=self.ax, horizontal=self.horizontal)

    def _style(self, patch: Patch) -> BarBorderStyler:
        return BarBorderStyler(patch=patch)

    def draw(
        self,
        color: str | list[str] | dict[str, str] | None = None,
        alpha: float | None = None,
        width: float | None = None,
        style: str | None = None,
    ) -> "BarBorderDrawer":
        """
        Set bars border style.

        When legend is set, color can only be provided as a dictionary mapping
        legend labels to colors.

        Parameters:
        ----------
        color : str | list[str] | dict[str, str] | None. Default is None.
            The color(s) to set for the borders.
            - String: specifying a single color for all borders.
            - List: specifying a list of color strings to cycle through for the borders.
            - Dictionary: mapping tick labels or legend labels to colors.
        alpha : float | None. Default is None.
            The alpha (transparency) value to set for the borders.
        width : float | None. Default is None.
            The width of the borders.
        style : str | None. Default is None.
            The line style of the borders.

        Returns:
        -------
        BarBorderDrawer
            The current instance for method chaining.

        Raises:
        ------
        ValueError
            If color is a string or list while legend is set.
            If color is a dictionary but does not match tick or legend entries.
        """

        properties = BarBorderProperties(
            color=color,
            alpha=alpha,
            width=width,
            style=style,
        )
        patches = BarPatchGenerator(ax=self.ax, horizontal=self.horizontal)

        if self.legend is not None:
            if isinstance(color, str):
                raise ValueError("Color by string is not supported when legend is set.")
            if isinstance(color, list):
                raise ValueError("Color by list is not supported when legend is set.")
            if isinstance(color, dict):
                self.help.validate_legend_entry(dict=color)
                for patch, color in patches.map_legend(property=color):
                    self._style(patch).set_border_color(color=color)
                    self._style(patch).set_border_alpha(alpha=properties.alpha)
                    self._style(patch).set_border_width(width=properties.width)
                    self._style(patch).set_border_style(style=properties.style)

        if self.legend is None:
            if isinstance(color, str):
                for patch in patches.standard():
                    self._style(patch).set_border_color(color=color)
                    self._style(patch).set_border_alpha(alpha=properties.alpha)
                    self._style(patch).set_border_width(width=properties.width)
                    self._style(patch).set_border_style(style=properties.style)
            if isinstance(color, list):
                for patch, color in patches.cycle(property=color):
                    self._style(patch).set_border_color(color=color)
                    self._style(patch).set_border_alpha(alpha=properties.alpha)
                    self._style(patch).set_border_width(width=properties.width)
                    self._style(patch).set_border_style(style=properties.style)
            if isinstance(color, dict):
                self.help.validate_tick_entry(dict=color)
                for patch, color in patches.map_tick(property=color):
                    self._style(patch).set_border_color(color=color)
                    self._style(patch).set_border_alpha(alpha=properties.alpha)
                    self._style(patch).set_border_width(width=properties.width)
                    self._style(patch).set_border_style(style=properties.style)

        return self

    def extrema(
        self,
        min_color: str | None = "#FF0000",
        max_color: str | None = "#00FF00",
        alpha: float | None = None,
        width: float | None = None,
        style: str | None = None,
    ) -> "BarBorderDrawer":
        """
        Set the color of borders corresponding to extrema (min and/or max) values.

        When legend is set, extrema coloring is not supported.

        Parameters:
        ----------
        min_color : str | None. Default is "#FF0000".
            The color to set for borders with minimum values.
        max_color : str | None. Default is "#00FF00".
            The color to set for borders with maximum values.
        alpha : float | None. Default is None.
            The alpha (transparency) value to set for the extrema borders.
        width : float | None. Default is None.
            The width to set for the extrema borders.
        style : str | None. Default is None.
            The style to set for the extrema borders.
        Returns:
        -------
        BarBorderDrawer
            The current instance for method chaining.

        Raises:
        ------
        ValueError
            If legend is set, as extrema coloring is not supported in that case.
        """

        properties = BarBorderExtremaProperties(
            min_color=min_color,
            max_color=max_color,
            alpha=alpha,
            width=width,
            style=style,
        )
        patches = BarPatchGenerator(ax=self.ax, horizontal=self.horizontal)

        if self.legend is not None:
            raise ValueError("Extrema coloring is not supported when legend is active.")

        if properties.min_color is not None:
            for patch in patches.extrema(target="min"):
                self._style(patch).set_border_color(color=properties.min_color)
                self._style(patch).set_border_alpha(alpha=properties.alpha)
                self._style(patch).set_border_width(width=properties.width)
                self._style(patch).set_border_style(style=properties.style)

        if properties.max_color is not None:
            for patch in patches.extrema(target="max"):
                self._style(patch).set_border_color(color=properties.max_color)
                self._style(patch).set_border_alpha(alpha=properties.alpha)
                self._style(patch).set_border_width(width=properties.width)
                self._style(patch).set_border_style(style=properties.style)

        return self
