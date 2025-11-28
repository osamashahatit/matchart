from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.patches import Patch
from matplotlib.colors import to_rgba

from ._utils import BarStyleHelper, BarPatchGenerator


@dataclass
class BarColorProperties:
    """Encapsulates properties for bar coloring."""

    color: str | list[str] | dict[str, str] | None
    alpha: float | None


@dataclass
class BarColorExtremaProperties:
    """Encapsulates properties for extrema bar coloring."""

    min_color: str | None
    max_color: str | None
    alpha: float | None


class BarColorStyler:

    def __init__(self, patch: Patch) -> None:
        self.patch = patch

    def set_face_color(self, color: str | None) -> None:
        """Set the face (background) color of a patch."""

        self.patch.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.patch.set_facecolor((r, g, b, a))

    def set_face_alpha(self, alpha: float | None) -> None:
        """Set the face (background) alpha of a patch."""

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
        alpha: float | None = None,
    ) -> "BarColorDrawer":
        """
        Set the color of bars.

        When legend is set, color can only be provided as a dictionary mapping
        legend labels to colors.

        Parameters:
        ----------
        color : str | list[str] | dict[str, str] | None. Default is None.
            The color(s) to set for the bars.
            - String: specifying a single color for all bars.
            - List: specifying a list of color strings to cycle through for the bars.
            - Dictionary: mapping tick labels or legend labels to colors.
        alpha : float | None. Default is None.
            The alpha (transparency) value to set for the bars.

        Returns:
        -------
        BarColorDrawer
            The current instance for method chaining.

        Raises:
        ------
        ValueError
            If color is a string or list while legend is set.
            If color is a dictionary but does not match tick or legend entries.
        """

        properties = BarColorProperties(color=color, alpha=alpha)
        patches = BarPatchGenerator(ax=self.ax, horizontal=self.horizontal)

        if self.legend is not None:
            if isinstance(color, str):
                raise ValueError("Color by string is not supported when legend is set.")
            if isinstance(color, list):
                raise ValueError("Color by list is not supported when legend is set.")
            if isinstance(color, dict):
                self.help.validate_legend_entry(dict=color)
                for patch, color in patches.map_legend(property=color):
                    self._style(patch).set_face_color(color=color)
                    self._style(patch).set_face_alpha(alpha=properties.alpha)

        if self.legend is None:
            if isinstance(color, str):
                for patch in patches.standard():
                    self._style(patch).set_face_color(color=color)
                    self._style(patch).set_face_alpha(alpha=properties.alpha)
            if isinstance(color, list):
                for patch, color in patches.cycle(property=color):
                    self._style(patch).set_face_color(color=color)
                    self._style(patch).set_face_alpha(alpha=properties.alpha)
            if isinstance(color, dict):
                self.help.validate_tick_entry(dict=color)
                for patch, color in patches.map_tick(property=color):
                    self._style(patch).set_face_color(color=color)
                    self._style(patch).set_face_alpha(alpha=properties.alpha)

        return self

    def extrema(
        self,
        min_color: str | None = "#FF0000",
        max_color: str | None = "#00FF00",
        alpha: float | None = None,
    ) -> "BarColorDrawer":
        """
        Set the color of bars corresponding to extrema (min and/or max) values.

        When legend is set, extrema coloring is not supported.

        Parameters:
        ----------
        min_color : str | None. Default is "#FF0000".
            The color to set for bars with minimum values.
        max_color : str | None. Default is "#00FF00".
            The color to set for bars with maximum values.
        alpha : float | None. Default is None.
            The alpha (transparency) value to set for the extrema bars.

        Returns:
        -------
        BarColorDrawer
            The current instance for method chaining.

        Raises:
        ------
        ValueError
            If legend is set, as extrema coloring is not supported in that case.
        """

        properties = BarColorExtremaProperties(
            min_color=min_color,
            max_color=max_color,
            alpha=alpha,
        )
        patches = BarPatchGenerator(ax=self.ax, horizontal=self.horizontal)

        if self.legend is not None:
            raise ValueError("Extrema coloring is not supported when legend is active.")

        if properties.min_color is not None:
            for patch in patches.extrema(target="min"):
                self._style(patch).set_face_color(color=properties.min_color)
                self._style(patch).set_face_alpha(alpha=properties.alpha)

        if properties.max_color is not None:
            for patch in patches.extrema(target="max"):
                self._style(patch).set_face_color(color=properties.max_color)
                self._style(patch).set_face_alpha(alpha=properties.alpha)

        return self
