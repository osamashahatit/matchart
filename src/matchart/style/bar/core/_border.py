from matplotlib.axes import Axes
from matplotlib.patches import Patch
from matplotlib.colors import to_rgba

from ._utils import BarStyleHelper, BarPatchGenerator


class BarBorderStyler:

    def __init__(self, patch: Patch) -> None:
        self.patch = patch

    def set_border_color(self, color: str | None) -> None:

        self.patch.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.patch.set_edgecolor((r, g, b, a))

    def set_border_alpha(self, alpha: float | None) -> None:

        self.patch.set_alpha(None)
        if alpha is not None:
            r, g, b, _ = to_rgba(self.patch.get_edgecolor())
            self.patch.set_edgecolor((r, g, b, alpha))

    def set_border_style(self, style: str | None) -> None:

        if style is not None:
            self.patch.set_linestyle(style)

    def set_border_width(self, width: float | None) -> None:

        if width is not None:
            self.patch.set_linewidth(width)


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
        alpha: float | list[float] | dict[str, float] | None = None,
        style: str | list[str] | dict[str, str] | None = None,
        width: float | list[float] | dict[str, float] | None = None,
    ) -> "BarBorderDrawer":
        """
        Set the bars border properties.

        When legend is set, properties can only be provided as a dictionary mapping
        legend labels to property value.

        Parameters
        ----------
        color : str | list[str] | dict[str, str] | None. Default is None.
            The border color(s) to set for the bars.
            - String: specifying a single color for all bars.
            - List: specifying a list of colors to cycle through for the bars.
            - Dictionary: mapping tick labels or legend labels to colors.
        alpha : float | list[float] | dict[str, float] | None. Default is None.
            The border alpha (transparency) value to set for the bars.
            - Float: specifying a single alpha value for all bars.
            - List: specifying a list of alpha values to cycle through for the bars.
            - Dictionary: mapping tick labels or legend labels to alpha values.
        style : str | list[str] | dict[str, str] | None. Default is None.
            The border style to set for the bars.
            - String: specifying a single style for all bars.
            - List: specifying a list of styles to cycle through for the bars.
            - Dictionary: mapping tick labels or legend labels to styles.
        width : float | list[float] | dict[str, float] | None. Default is None.
            The border width to set for the bars.
            - Float: specifying a single width for all bars.
            - List: specifying a list of widths to cycle through for the bars.
            - Dictionary: mapping tick labels or legend labels to widths.

        Returns
        -------
        BarBorderDrawer
            The current instance for method chaining.
        """

        patches = BarPatchGenerator(ax=self.ax, horizontal=self.horizontal)

        if self.legend is not None:
            # Border color
            if isinstance(color, str):
                raise ValueError(
                    "Border color must be a dictionary when legend is set."
                )
            if isinstance(color, list):
                raise ValueError(
                    "Border color must be a dictionary when legend is set."
                )
            if isinstance(color, dict):
                self.help.validate_legend_entry(dict=color)
                for patch, color in patches.map_legend(property=color):
                    self._style(patch).set_border_color(color=color)
            # Border alpha
            if isinstance(alpha, float):
                raise ValueError(
                    "Border alpha must be a dictionary when legend is set."
                )
            if isinstance(alpha, list):
                raise ValueError(
                    "Border alpha must be a dictionary when legend is set."
                )
            if isinstance(alpha, dict):
                self.help.validate_legend_entry(dict=alpha)
                for patch, alpha in patches.map_legend(property=alpha):
                    self._style(patch).set_border_alpha(alpha=alpha)
            # Border style
            if isinstance(style, str):
                raise ValueError(
                    "Border style must be a dictionary when legend is set."
                )
            if isinstance(style, list):
                raise ValueError(
                    "Border style must be a dictionary when legend is set."
                )
            if isinstance(style, dict):
                self.help.validate_legend_entry(dict=style)
                for patch, style in patches.map_legend(property=style):
                    self._style(patch).set_border_style(style=style)
            # Border width
            if isinstance(width, float):
                raise ValueError(
                    "Border width must be a dictionary when legend is set."
                )
            if isinstance(width, list):
                raise ValueError(
                    "Border width must be a dictionary when legend is set."
                )
            if isinstance(width, dict):
                self.help.validate_legend_entry(dict=width)
                for patch, width in patches.map_legend(property=width):
                    self._style(patch).set_border_width(width=width)

        if self.legend is None:
            # Border color
            if isinstance(color, str):
                for patch in patches.standard():
                    self._style(patch).set_border_color(color=color)
            if isinstance(color, list):
                for patch, color in patches.cycle(property=color):
                    self._style(patch).set_border_color(color=color)
            if isinstance(color, dict):
                self.help.validate_tick_entry(dict=color)
                for patch, color in patches.map_tick(property=color):
                    self._style(patch).set_border_color(color=color)
            # Border alpha
            if isinstance(alpha, float):
                for patch in patches.standard():
                    self._style(patch).set_border_alpha(alpha=alpha)
            if isinstance(alpha, list):
                for patch, alpha in patches.cycle(property=alpha):
                    self._style(patch).set_border_alpha(alpha=alpha)
            if isinstance(alpha, dict):
                self.help.validate_tick_entry(dict=alpha)
                for patch, alpha in patches.map_tick(property=alpha):
                    self._style(patch).set_border_alpha(alpha=alpha)
            # Border style
            if isinstance(style, str):
                for patch in patches.standard():
                    self._style(patch).set_border_style(style=style)
            if isinstance(style, list):
                for patch, style in patches.cycle(property=style):
                    self._style(patch).set_border_style(style=style)
            if isinstance(style, dict):
                self.help.validate_tick_entry(dict=style)
                for patch, style in patches.map_tick(property=style):
                    self._style(patch).set_border_style(style=style)
            # Border width
            if isinstance(width, float):
                for patch in patches.standard():
                    self._style(patch).set_border_width(width=width)
            if isinstance(width, list):
                for patch, width in patches.cycle(property=width):
                    self._style(patch).set_border_width(width=width)
            if isinstance(width, dict):
                self.help.validate_tick_entry(dict=width)
                for patch, width in patches.map_tick(property=width):
                    self._style(patch).set_border_width(width=width)

        return self

    def extrema(
        self,
        min_color: str | None = "#FF0000",
        max_color: str | None = "#00FF00",
        min_alpha: float | None = None,
        max_alpha: float | None = None,
        min_width: float | None = None,
        max_width: float | None = None,
        min_style: str | None = None,
        max_style: str | None = None,
    ) -> "BarBorderDrawer":
        """
        Set the border properties for the extrema bars (minimum and maximum values).

        When legend is set, extrema styling is not supported.

        Parameters
        ----------
        min_color : str | None. Default is "#FF0000".
            The border color to set for bars with minimum values.
        max_color : str | None. Default is "#00FF00".
            The border color to set for bars with maximum values.
        min_alpha : float | None. Default is None.
            The border alpha (transparency) value to set for bars with minimum values.
        max_alpha : float | None. Default is None.
            The border alpha (transparency) value to set for bars with maximum values.
        min_width : float | None. Default is None.
            The border width to set for bars with minimum values.
        max_width : float | None. Default is None.
            The border width to set for bars with maximum values.
        min_style : str | None. Default is None.
            The border style to set for bars with minimum values.
        max_style : str | None. Default is None.
            The border style to set for bars with maximum values.

        Returns
        -------
        BarBorderDrawer
            The current instance for method chaining.
        """

        patches = BarPatchGenerator(ax=self.ax, horizontal=self.horizontal)

        if self.legend is not None:
            raise ValueError("Extrema coloring is not supported when legend is set.")

        if self.legend is None:
            # Min bars
            for patch in patches.extrema(target="min"):
                self._style(patch).set_border_color(color=min_color)
                self._style(patch).set_border_alpha(alpha=min_alpha)
                self._style(patch).set_border_width(width=min_width)
                self._style(patch).set_border_style(style=min_style)
            # Max bars
            for patch in patches.extrema(target="max"):
                self._style(patch).set_border_color(color=max_color)
                self._style(patch).set_border_alpha(alpha=max_alpha)
                self._style(patch).set_border_width(width=max_width)
                self._style(patch).set_border_style(style=max_style)

        return self
