"""Style bar patch face colors."""

from matplotlib.axes import Axes
from matplotlib.colors import to_rgba
from matplotlib.patches import Patch

from ._utils import BarPatchYielder, BarStyleHelper


class BarColorStyler:
    """Apply face (fill) styling to a single bar patch."""

    def __init__(self, patch: Patch) -> None:
        """
        Args:
            patch (Patch): Bar patch to style (typically a Rectangle).
        """
        self.patch = patch

    def set_face_color(self, color: str | None) -> None:
        """Set the face (fill) color of the bar patch.

        Args:
            color (str | None): Matplotlib-compatible color string.
        """
        # Reset global alpha so per-channel RGBA values are respected.
        self.patch.set_alpha(None)

        if color is not None:
            r, g, b, a = to_rgba(color)
            self.patch.set_facecolor((r, g, b, a))

    def set_face_alpha(self, alpha: float | None) -> None:
        """Override the alpha channel of the patch face color.

        Args:
            alpha (float | None): Alpha value in [0.0, 1.0].
        """
        self.patch.set_alpha(None)

        if alpha is not None:
            r, g, b, _ = to_rgba(self.patch.get_facecolor())
            self.patch.set_facecolor((r, g, b, alpha))


class BarColorDrawer:
    """Apply bar face styling across all bar patches on an Axes."""

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

    def _style(self, patch: Patch) -> BarColorStyler:
        """Create a BarColorStyler for a given patch."""
        return BarColorStyler(patch=patch)

    def draw(
        self,
        color: str | list[str] | dict[str, str] | None = None,
        alpha: float | list[float] | dict[str, float] | None = None,
    ) -> "BarColorDrawer":
        """Set bar face color and alpha using scalar, list, or mapping inputs.

        In legend mode (legend is not None), properties must be provided as
        dictionaries mapping legend labels to values. Otherwise, mappings
        are interpreted as tick label mappings.

        Args:
            color (str | list[str] | dict[str, str] | None): Face color
                specification:
                  - str: apply one color to all bars.
                  - list[str]: cycle colors across bars.
                  - dict[str, str]: map tick labels (no legend) or legend
                    labels (legend mode) to colors.
            alpha (float | list[float] | dict[str, float] | None): Face alpha
                specification:
                  - float: apply one alpha to all bars.
                  - list[float]: cycle alpha values across bars.
                  - dict[str, float]: map tick labels (no legend) or legend
                    labels (legend mode) to alpha values.

        Returns:
            BarColorDrawer: The current instance for method chaining.

        Raises:
            ValueError: If legend is set and any property is provided as a
                scalar or list instead of a dict.
            ValueError: If a provided dict contains keys that are not valid
                tick labels (no legend) or legend labels (legend mode).
        """
        patches = BarPatchYielder(ax=self.ax, horizontal=self.horizontal)

        if self.legend is not None:
            # Bar color
            if isinstance(color, str):
                raise ValueError("Bar color must be a dictionary when legend is set.")
            if isinstance(color, list):
                raise ValueError("Bar color must be a dictionary when legend is set.")
            if isinstance(color, dict):
                self.helper.validate_legend_entry(mapping=color)
                for patch, color in patches.map_legend(property=color):
                    self._style(patch).set_face_color(color=color)

            # Bar alpha
            if isinstance(alpha, float):
                raise ValueError("Bar alpha must be a dictionary when legend is set.")
            if isinstance(alpha, list):
                raise ValueError("Bar alpha must be a dictionary when legend is set.")
            if isinstance(alpha, dict):
                self.helper.validate_legend_entry(mapping=alpha)
                for patch, alpha in patches.map_legend(property=alpha):
                    self._style(patch).set_face_alpha(alpha=alpha)

        if self.legend is None:
            # Bar color
            if isinstance(color, str):
                for patch in patches.standard():
                    self._style(patch).set_face_color(color=color)
            if isinstance(color, list):
                for patch, color in patches.cycle(property=color):
                    self._style(patch).set_face_color(color=color)
            if isinstance(color, dict):
                self.helper.validate_tick_entry(mapping=color)
                for patch, color in patches.map_tick(property=color):
                    self._style(patch).set_face_color(color=color)

            # Bar alpha
            if isinstance(alpha, float):
                for patch in patches.standard():
                    self._style(patch).set_face_alpha(alpha=alpha)
            if isinstance(alpha, list):
                for patch, alpha in patches.cycle(property=alpha):
                    self._style(patch).set_face_alpha(alpha=alpha)
            if isinstance(alpha, dict):
                self.helper.validate_tick_entry(mapping=alpha)
                for patch, alpha in patches.map_tick(property=alpha):
                    self._style(patch).set_face_alpha(alpha=alpha)

        return self

    def extrema(
        self,
        min_color: str | None = "#FF0000",
        max_color: str | None = "#00FF00",
        min_alpha: float | None = None,
        max_alpha: float | None = None,
    ) -> "BarColorDrawer":
        """Set face styling for extrema (minimum and maximum) bars.

        Notes:
            When legend is set (legend is not None), extrema styling is not
            supported and this method raises ValueError.

        Args:
            min_color (str | None): Face color for bars with the minimum
                value.
            max_color (str | None): Face color for bars with the maximum
                value.
            min_alpha (float | None): Face alpha for minimum-value bars.
            max_alpha (float | None): Face alpha for maximum-value bars.

        Returns:
            BarColorDrawer: The current instance for method chaining.

        Raises:
            ValueError: If legend is set.
        """
        patches = BarPatchYielder(ax=self.ax, horizontal=self.horizontal)

        if self.legend is not None:
            raise ValueError("Extrema coloring is not supported when legend is set.")

        # Min bars
        for patch in patches.extrema(target="min"):
            self._style(patch).set_face_color(color=min_color)
            self._style(patch).set_face_alpha(alpha=min_alpha)

        # Max bars
        for patch in patches.extrema(target="max"):
            self._style(patch).set_face_color(color=max_color)
            self._style(patch).set_face_alpha(alpha=max_alpha)

        return self
