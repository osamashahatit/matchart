from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.colors import to_rgba

from ._utils import LineStyleHelper, LineGenerator


class MarkerStyler:

    def __init__(self, line: Line2D):
        self.line = line

    def set_marker(self, marker: str | None) -> None:

        if marker is not None:
            self.line.set_marker(marker)

    def set_marker_color(self, color: str | None) -> None:

        self.line.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.line.set_markerfacecolor((r, g, b, a))

    def set_marker_alpha(self, alpha: float | None) -> None:

        self.line.set_alpha(None)
        if alpha is not None:
            r, g, b, _ = to_rgba(self.line.get_markerfacecolor())
            self.line.set_markerfacecolor((r, g, b, alpha))

    def set_marker_size(self, size: int | None) -> None:

        if size is not None:
            self.line.set_markersize(size)

    def set_marker_edge_color(self, color: str | None) -> None:

        self.line.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.line.set_markeredgecolor((r, g, b, a))

    def set_marker_edge_alpha(self, alpha: float | None) -> None:

        self.line.set_alpha(None)
        if alpha is not None:
            r, g, b, _ = to_rgba(self.line.get_markeredgecolor())
            self.line.set_markeredgecolor((r, g, b, alpha))

    def set_marker_edge_width(self, width: float | None) -> None:

        if width is not None:
            self.line.set_markeredgewidth(width)


class MarkerDrawer:

    def __init__(self, ax: Axes, legend: str | None) -> None:
        self.ax = ax
        self.legend = legend
        self.help = LineStyleHelper(ax=self.ax)

    def _style(self, line: Line2D) -> MarkerStyler:
        return MarkerStyler(line=line)

    def draw(
        self,
        marker: str | dict[str, str] | None = "o",
        face_color: str | dict[str, str] | None = None,
        face_alpha: float | dict[str, float] | None = None,
        size: int | dict[str, int] | None = None,
        edge_color: str | dict[str, str] | None = None,
        edge_alpha: float | dict[str, float] | None = None,
        edge_width: float | dict[str, float] | None = None,
    ) -> None:
        """
        Set marker properties.

        Parameters
        ----------
        marker : str | dict[str, str] | None. Default is None.
            Marker style as a string or a dictionary mapping legend labels to marker styles.
        face_color : str | dict[str, str] | None. Default is None.
            Marker face color as a single string or a dictionary mapping legend labels to colors.
        face_alpha : float | dict[str, float] | None. Default is None.
            Marker face alpha as a single float or a dictionary mapping legend labels to alpha values.
        size : int | dict[str, int] | None. Default is None.
            Marker size as a single int or a dictionary mapping legend labels to sizes.
        edge_color : str | dict[str, str] | None. Default is None.
            Marker edge color as a single string or a dictionary mapping legend labels to colors.
        edge_alpha : float | dict[str, float] | None. Default is None.
            Marker edge alpha as a single float or a dictionary mapping legend labels to alpha values.
        edge_width : float | dict[str, float] | None. Default is None.
            Marker edge width as a single float or a dictionary mapping legend labels to widths.
        """

        lines = LineGenerator(ax=self.ax)

        if self.legend is not None:
            # Marker
            if isinstance(marker, str):
                raise TypeError("Marker must be a dictionary when legend is set.")
            if isinstance(marker, dict):
                self.help.validate_legend_entry(dict=marker)
                for line, marker in lines.map_legend(property=marker):
                    self._style(line=line).set_marker(marker=marker)
            # Marker face color
            if isinstance(face_color, str):
                raise TypeError(
                    "Marker face color must be a dictionary when legend is set."
                )
            if isinstance(face_color, dict):
                self.help.validate_legend_entry(dict=face_color)
                for line, color in lines.map_legend(property=face_color):
                    self._style(line=line).set_marker_color(color=color)
            # Marker face alpha
            if isinstance(face_alpha, float):
                raise TypeError(
                    "Marker face alpha must be a dictionary when legend is set."
                )
            if isinstance(face_alpha, dict):
                self.help.validate_legend_entry(dict=face_alpha)
                for line, alpha in lines.map_legend(property=face_alpha):
                    self._style(line=line).set_marker_alpha(alpha=alpha)
            # Marker size
            if isinstance(size, int):
                raise TypeError("Marker size must be a dictionary when legend is set.")
            if isinstance(size, dict):
                self.help.validate_legend_entry(dict=size)
                for line, size in lines.map_legend(property=size):
                    self._style(line=line).set_marker_size(size=size)
            # Marker edge color
            if isinstance(edge_color, str):
                raise TypeError(
                    "Marker edge color must be a dictionary when legend is set."
                )
            if isinstance(edge_color, dict):
                self.help.validate_legend_entry(dict=edge_color)
                for line, color in lines.map_legend(property=edge_color):
                    self._style(line=line).set_marker_edge_color(color=color)
            # Marker edge alpha
            if isinstance(edge_alpha, float):
                raise TypeError(
                    "Marker edge alpha must be a dictionary when legend is set."
                )
            if isinstance(edge_alpha, dict):
                self.help.validate_legend_entry(dict=edge_alpha)
                for line, alpha in lines.map_legend(property=edge_alpha):
                    self._style(line=line).set_marker_edge_alpha(alpha=alpha)
            # Marker edge width
            if isinstance(edge_width, float):
                raise TypeError(
                    "Marker edge width must be a dictionary when legend is set."
                )
            if isinstance(edge_width, dict):
                self.help.validate_legend_entry(dict=edge_width)
                for line, width in lines.map_legend(property=edge_width):
                    self._style(line=line).set_marker_edge_width(width=width)

        if self.legend is None:
            # Marker
            if isinstance(marker, dict):
                raise TypeError("Marker must be a string when legend is not set.")
            if isinstance(marker, str):
                for line in lines.standard():
                    self._style(line=line).set_marker(marker=marker)
            # Marker face color
            if isinstance(face_color, dict):
                raise TypeError(
                    "Marker face color must be a string when legend is not set."
                )
            if isinstance(face_color, str):
                for line in lines.standard():
                    self._style(line=line).set_marker_color(color=face_color)
            # Marker face alpha
            if isinstance(face_alpha, dict):
                raise TypeError(
                    "Marker face alpha must be a float when legend is not set."
                )
            if isinstance(face_alpha, float):
                for line in lines.standard():
                    self._style(line=line).set_marker_alpha(alpha=face_alpha)
            # Marker size
            if isinstance(size, dict):
                raise TypeError("Marker size must be an int when legend is not set.")
            if isinstance(size, int):
                for line in lines.standard():
                    self._style(line=line).set_marker_size(size=size)
            # Marker edge color
            if isinstance(edge_color, dict):
                raise TypeError(
                    "Marker edge color must be a string when legend is not set."
                )
            if isinstance(edge_color, str):
                for line in lines.standard():
                    self._style(line=line).set_marker_edge_color(color=edge_color)
            # Marker edge alpha
            if isinstance(edge_alpha, dict):
                raise TypeError(
                    "Marker edge alpha must be a float when legend is not set."
                )
            if isinstance(edge_alpha, float):
                for line in lines.standard():
                    self._style(line=line).set_marker_edge_alpha(alpha=edge_alpha)
            # Marker edge width
            if isinstance(edge_width, dict):
                raise TypeError(
                    "Marker edge width must be a float when legend is not set."
                )
            if isinstance(edge_width, float):
                for line in lines.standard():
                    self._style(line=line).set_marker_edge_width(width=edge_width)
