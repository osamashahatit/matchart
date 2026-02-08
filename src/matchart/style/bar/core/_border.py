"""Style bar patch borders."""

from matplotlib.axes import Axes
from matplotlib.colors import to_rgba
from matplotlib.patches import Patch

from ._utils import BarPatchYielder, BarStyleHelper


class BarBorderStyler:
    """Apply border styling to a single bar patch."""

    def __init__(self, patch: Patch) -> None:
        """
        Args:
            patch (Patch): Bar patch to style (typically a Rectangle).
        """
        self.patch = patch

    def set_border_color(self, color: str | None) -> None:
        """Set the border (edge) color of the bar patch.

        Args:
            color (str | None): Matplotlib-compatible color string.
        """
        # Reset global alpha so per-channel RGBA values are respected.
        self.patch.set_alpha(None)

        if color is not None:
            r, g, b, a = to_rgba(color)
            self.patch.set_edgecolor((r, g, b, a))

    def set_border_alpha(self, alpha: float | None) -> None:
        """Override the alpha channel of the patch border color.

        Args:
            alpha (float | None): Alpha value in [0.0, 1.0].
        """
        self.patch.set_alpha(None)

        if alpha is not None:
            r, g, b, _ = to_rgba(self.patch.get_edgecolor())
            self.patch.set_edgecolor((r, g, b, alpha))

    def set_border_style(self, style: str | None) -> None:
        """Set the border line style.

        Args:
            style (str | None): Matplotlib linestyle string (e.g. "-", "--", ":").
        """
        if style is not None:
            self.patch.set_linestyle(style)

    def set_border_width(self, width: float | None) -> None:
        """Set the border line width.

        Args:
            width (float | None): Line width in points.
        """
        if width is not None:
            self.patch.set_linewidth(width)


class BarBorderDrawer:
    """Apply bar border styling across all bar patches on an Axes."""

    def __init__(self, ax: Axes, horizontal: bool, legend: str | None) -> None:
        """
        Args:
            ax (Axes): Axes that already contains bar artists.
            horizontal (bool): Whether the bar chart is horizontal.
            legend (str | None): When not None, enables legend-based mapping
                behavior (dict-only inputs) for draw(). The value is used as
                a presence flag.
        """
        self.ax = ax
        self.horizontal = horizontal
        self.legend = legend
        self.helper = BarStyleHelper(ax=self.ax, horizontal=self.horizontal)

    def _style(self, patch: Patch) -> BarBorderStyler:
        """Create a BarBorderStyler for a given patch."""
        return BarBorderStyler(patch=patch)

    def draw(
        self,
        color: str | list[str] | dict[str, str] | None = None,
        alpha: float | list[float] | dict[str, float] | None = None,
        style: str | list[str] | dict[str, str] | None = None,
        width: float | list[float] | dict[str, float] | None = None,
    ) -> "BarBorderDrawer":
        """Set bar border properties using scalar, list, or mapping inputs.

        In legend mode (legend is not None), properties must be provided as
        dictionaries mapping legend labels to values. Otherwise, mappings
        are interpreted as tick label mappings.

        Args:
            color (str | list[str] | dict[str, str] | None): Border color
                specification:
                  - str: apply one color to all bars.
                  - list[str]: cycle colors across bars.
                  - dict[str, str]: map tick labels (no legend) or legend
                    labels (legend mode) to colors.
            alpha (float | list[float] | dict[str, float] | None): Border
                alpha specification:
                  - float: apply one alpha to all bars.
                  - list[float]: cycle alpha values across bars.
                  - dict[str, float]: map tick labels (no legend) or legend
                    labels (legend mode) to alpha values.
            style (str | list[str] | dict[str, str] | None): Border line
                style specification:
                  - str: apply one linestyle to all bars.
                  - list[str]: cycle linestyles across bars.
                  - dict[str, str]: map tick labels (no legend) or legend
                    labels (legend mode) to linestyles.
            width (float | list[float] | dict[str, float] | None): Border
                width specification:
                  - float: apply one linewidth to all bars.
                  - list[float]: cycle linewidths across bars.
                  - dict[str, float]: map tick labels (no legend) or legend
                    labels (legend mode) to linewidths.

        Returns:
            BarBorderDrawer: The current instance for method chaining.

        Raises:
            ValueError: If legend is set and any property is provided as a
                scalar or list instead of a dict.
            ValueError: If a provided dict contains keys that are not valid
                tick labels (no legend) or legend labels (legend mode).
        """
        patches = BarPatchYielder(ax=self.ax, horizontal=self.horizontal)

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
                self.helper.validate_legend_entry(mapping=color)
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
                self.helper.validate_legend_entry(mapping=alpha)
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
                self.helper.validate_legend_entry(mapping=style)
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
                self.helper.validate_legend_entry(mapping=width)
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
                self.helper.validate_tick_entry(mapping=color)
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
                self.helper.validate_tick_entry(mapping=alpha)
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
                self.helper.validate_tick_entry(mapping=style)
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
                self.helper.validate_tick_entry(mapping=width)
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
        """Set border properties for extrema (minimum and maximum) bars.

        Notes:
            When legend is set (legend is not None), extrema styling is not
            supported and this method raises ValueError.

        Args:
            min_color (str | None): Border color for bars with the minimum
                value.
            max_color (str | None): Border color for bars with the maximum
                value.
            min_alpha (float | None): Border alpha for minimum-value bars.
            max_alpha (float | None): Border alpha for maximum-value bars.
            min_width (float | None): Border width for minimum-value bars.
            max_width (float | None): Border width for maximum-value bars.
            min_style (str | None): Border linestyle for minimum-value bars.
            max_style (str | None): Border linestyle for maximum-value bars.

        Returns:
            BarBorderDrawer: The current instance for method chaining.

        Raises:
            ValueError: If legend is set.
        """
        patches = BarPatchYielder(ax=self.ax, horizontal=self.horizontal)

        if self.legend is not None:
            raise ValueError("Extrema coloring is not supported when legend is set.")

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
