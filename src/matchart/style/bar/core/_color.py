from matplotlib.axes import Axes
from matplotlib.patches import Patch
from matplotlib.colors import to_rgba

from ._utils import BarStyleHelper, BarPatchGenerator


class BarColorStyler:

    def __init__(self, patch: Patch) -> None:
        self.patch = patch

    def set_face_color(self, color: str | None) -> None:

        self.patch.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.patch.set_facecolor((r, g, b, a))

    def set_face_alpha(self, alpha: float | None) -> None:

        self.patch.set_alpha(None)
        if alpha is not None:
            r, g, b, _ = to_rgba(self.patch.get_facecolor())
            self.patch.set_facecolor((r, g, b, alpha))


class BarColorDrawer:

    def __init__(self, ax: Axes, horizontal: bool, legend: str | None) -> None:
        self.ax = ax
        self.horizontal = horizontal
        self.legend = legend
        self.help = BarStyleHelper(ax=self.ax, horizontal=self.horizontal)

    def _style(self, patch: Patch) -> BarColorStyler:
        return BarColorStyler(patch=patch)

    def draw(
        self,
        color: str | list[str] | dict[str, str] | None = None,
        alpha: float | list[float] | dict[str, float] | None = None,
    ) -> "BarColorDrawer":
        """
        Set the bars color properties.

        When legend is set, properties can only be provided as a dictionary mapping
        legend labels to property value.

        Parameters:
        ----------
        color : str | list[str] | dict[str, str] | None. Default is None.
            The color(s) to set for the bars.
            - String: specifying a single color for all bars.
            - List: specifying a list of colors to cycle through for the bars.
            - Dictionary: mapping tick labels or legend labels to colors.
        alpha : float | list[float] | dict[str, float]. Default is None.
            The alpha (transparency) value to set for the bars.
            - Float: specifying a single alpha value for all bars.
            - List: specifying a list of alpha values to cycle through for the bars.
            - Dictionary: mapping tick labels or legend labels to alpha values.

        Returns:
        -------
        BarColorDrawer
            The current instance for method chaining.
        """

        patches = BarPatchGenerator(ax=self.ax, horizontal=self.horizontal)

        if self.legend is not None:
            # Bar color
            if isinstance(color, str):
                raise ValueError("Bar color must be a dictionary when legend is set.")
            if isinstance(color, list):
                raise ValueError("Bar color must be a dictionary when legend is set.")
            if isinstance(color, dict):
                self.help.validate_legend_entry(dict=color)
                for patch, color in patches.map_legend(property=color):
                    self._style(patch).set_face_color(color=color)
            # Bar alpha
            if isinstance(alpha, float):
                raise ValueError("Bar alpha must be a dictionary when legend is set.")
            if isinstance(alpha, list):
                raise ValueError("Bar alpha must be a dictionary when legend is set.")
            if isinstance(alpha, dict):
                self.help.validate_legend_entry(dict=alpha)
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
                self.help.validate_tick_entry(dict=color)
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
                self.help.validate_tick_entry(dict=alpha)
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
        """
        Set the color properties for the extrema bars (minimum and maximum values).

        When legend is set, extrema coloring is not supported.

        Parameters:
        ----------
        min_color : str | None. Default is "#FF0000".
            The color to set for bars with minimum values.
        max_color : str | None. Default is "#00FF00".
            The color to set for bars with maximum values.
        min_alpha : float | None. Default is None.
            The alpha (transparency) value to set for bars with minimum values.
        max_alpha : float | None. Default is None.
            The alpha (transparency) value to set for bars with maximum values.

        Returns:
        -------
        BarColorDrawer
            The current instance for method chaining.
        """

        patches = BarPatchGenerator(ax=self.ax, horizontal=self.horizontal)

        if self.legend is not None:
            raise ValueError("Extrema coloring is not supported when legend is set.")

        if self.legend is None:
            # Min bars
            for patch in patches.extrema(target="min"):
                self._style(patch).set_face_color(color=min_color)
                self._style(patch).set_face_alpha(alpha=min_alpha)
            # Max bars
            for patch in patches.extrema(target="max"):
                self._style(patch).set_face_color(color=max_color)
                self._style(patch).set_face_alpha(alpha=max_alpha)

        return self
