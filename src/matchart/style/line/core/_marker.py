"""Style Line2D marker."""

from matplotlib.axes import Axes
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D

from ._utils import LineStyleHelper, LineYielder


class MarkerStyler:
    """Apply marker styling to a single Line2D artist."""

    def __init__(self, line: Line2D):
        """
        Args:
            line (Line2D): Line artist to style.
        """
        self.line = line

    def set_marker(self, marker: str | None) -> None:
        """Set the marker style for the line.

        Args:
            marker (str | None): Matplotlib marker style string. If None, no
                change is applied.

        Notes:
            Matplotlib supports many marker strings; see the Matplotlib marker
            documentation for the full set.
        """
        if marker is not None:
            self.line.set_marker(marker)

    def set_marker_color(self, color: str | None) -> None:
        """Set the marker face color.

        Args:
            color (str | None): Matplotlib-compatible color string. If None, no
                change is applied.

        Notes:
            Resets the global alpha (line.set_alpha(None)) so the alpha channel
            in the RGBA marker face color is respected.
        """
        self.line.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.line.set_markerfacecolor((r, g, b, a))

    def set_marker_alpha(self, alpha: float | None) -> None:
        """Override the alpha channel of the marker face color.

        Args:
            alpha (float | None): Alpha value in [0.0, 1.0]. If None, no change
                is applied.

        Notes:
            Resets the global alpha (line.set_alpha(None)) so the alpha channel
            in the RGBA marker face color is respected.
        """
        self.line.set_alpha(None)
        if alpha is not None:
            r, g, b, _ = to_rgba(self.line.get_markerfacecolor())
            self.line.set_markerfacecolor((r, g, b, alpha))

    def set_marker_size(self, size: int | None) -> None:
        """Set the marker size.

        Args:
            size (int | None): Marker size in points. If None, no change is
                applied.
        """
        if size is not None:
            self.line.set_markersize(size)

    def set_marker_edge_color(self, color: str | None) -> None:
        """Set the marker edge color.

        Args:
            color (str | None): Matplotlib-compatible color string. If None, no
                change is applied.

        Notes:
            Resets the global alpha (line.set_alpha(None)) so the alpha channel
            in the RGBA marker edge color is respected.
        """
        self.line.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.line.set_markeredgecolor((r, g, b, a))

    def set_marker_edge_alpha(self, alpha: float | None) -> None:
        """Override the alpha channel of the marker edge color.

        Args:
            alpha (float | None): Alpha value in [0.0, 1.0]. If None, no change
                is applied.

        Notes:
            Resets the global alpha (line.set_alpha(None)) so the alpha channel
            in the RGBA marker edge color is respected.
        """
        self.line.set_alpha(None)
        if alpha is not None:
            r, g, b, _ = to_rgba(self.line.get_markeredgecolor())
            self.line.set_markeredgecolor((r, g, b, alpha))

    def set_marker_edge_width(self, width: float | None) -> None:
        """Set the marker edge line width.

        Args:
            width (float | None): Marker edge width in points. If None, no
                change is applied.
        """
        if width is not None:
            self.line.set_markeredgewidth(width)


class MarkerDrawer:
    """Apply marker styling across Line2D artists on an Axes."""

    def __init__(self, ax: Axes, legend: str | None) -> None:
        """
        Args:
            ax (Axes): Axes that already contains line artists.
            legend (str | None): When not None, enables legend-based mapping
                behavior (dict-only inputs) for draw(). The value is used as a
                presence flag.
        """
        self.ax = ax
        self.legend = legend
        self.helper = LineStyleHelper(ax=self.ax)

    def _style(self, line: Line2D) -> MarkerStyler:
        """Create a MarkerStyler for a given line artist."""
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
        """Set marker properties using scalar or legend-mapped inputs.

        In legend mode (legend is not None), properties must be provided as
        dictionaries mapping legend labels to values. Otherwise, properties are
        applied uniformly to all lines.

        Args:
            marker (str | dict[str, str] | None): Marker style specification:
              - str: apply one marker to all lines (legend=None only).
              - dict[str, str]: map legend labels to markers (legend mode).
              - Options: "o", "s", "^", "D", ".", "x", "+", "*", "None"
            face_color (str | dict[str, str] | None): Marker face color
                specification:
              - str: apply one color to all lines (legend=None only).
              - dict[str, str]: map legend labels to colors (legend mode).
            face_alpha (float | dict[str, float] | None): Marker face alpha
                specification:
              - float: apply one alpha to all lines (legend=None only).
              - dict[str, float]: map legend labels to alpha values
                (legend mode).
            size (int | dict[str, int] | None): Marker size specification:
              - int: apply one size to all lines (legend=None only).
              - dict[str, int]: map legend labels to sizes (legend mode).
            edge_color (str | dict[str, str] | None): Marker edge color
                specification:
              - str: apply one color to all lines (legend=None only).
              - dict[str, str]: map legend labels to colors (legend mode).
            edge_alpha (float | dict[str, float] | None): Marker edge alpha
                specification:
              - float: apply one alpha to all lines (legend=None only).
              - dict[str, float]: map legend labels to alpha values
                (legend mode).
            edge_width (float | dict[str, float] | None): Marker edge width
                specification:
              - float: apply one width to all lines (legend=None only).
              - dict[str, float]: map legend labels to widths (legend mode).

        Raises:
            TypeError: If legend is set and any property is provided as a scalar
                instead of a dict, or if legend is not set and a dict is
                provided.

        Notes:
            This method mutates Line2D artists in place and does not return self
            (not chainable).
        """
        lines = LineYielder(ax=self.ax)

        if self.legend is not None:
            # Marker (legend-mapped)
            if isinstance(marker, str):
                raise TypeError("Marker must be a dictionary when legend is set.")
            if isinstance(marker, dict):
                self.helper.validate_legend_entry(mapping=marker)
                for line, marker in lines.map_legend(property=marker):
                    self._style(line=line).set_marker(marker=marker)

            # Marker face color (legend-mapped)
            if isinstance(face_color, str):
                raise TypeError(
                    "Marker face color must be a dictionary when legend is set."
                )
            if isinstance(face_color, dict):
                self.helper.validate_legend_entry(mapping=face_color)
                for line, color in lines.map_legend(property=face_color):
                    self._style(line=line).set_marker_color(color=color)

            # Marker face alpha (legend-mapped)
            if isinstance(face_alpha, float):
                raise TypeError(
                    "Marker face alpha must be a dictionary when legend is set."
                )
            if isinstance(face_alpha, dict):
                self.helper.validate_legend_entry(mapping=face_alpha)
                for line, alpha in lines.map_legend(property=face_alpha):
                    self._style(line=line).set_marker_alpha(alpha=alpha)

            # Marker size (legend-mapped)
            if isinstance(size, int):
                raise TypeError("Marker size must be a dictionary when legend is set.")
            if isinstance(size, dict):
                self.helper.validate_legend_entry(mapping=size)
                for line, size in lines.map_legend(property=size):
                    self._style(line=line).set_marker_size(size=size)

            # Marker edge color (legend-mapped)
            if isinstance(edge_color, str):
                raise TypeError(
                    "Marker edge color must be a dictionary when legend is set."
                )
            if isinstance(edge_color, dict):
                self.helper.validate_legend_entry(mapping=edge_color)
                for line, color in lines.map_legend(property=edge_color):
                    self._style(line=line).set_marker_edge_color(color=color)

            # Marker edge alpha (legend-mapped)
            if isinstance(edge_alpha, float):
                raise TypeError(
                    "Marker edge alpha must be a dictionary when legend is set."
                )
            if isinstance(edge_alpha, dict):
                self.helper.validate_legend_entry(mapping=edge_alpha)
                for line, alpha in lines.map_legend(property=edge_alpha):
                    self._style(line=line).set_marker_edge_alpha(alpha=alpha)

            # Marker edge width (legend-mapped)
            if isinstance(edge_width, float):
                raise TypeError(
                    "Marker edge width must be a dictionary when legend is set."
                )
            if isinstance(edge_width, dict):
                self.helper.validate_legend_entry(mapping=edge_width)
                for line, width in lines.map_legend(property=edge_width):
                    self._style(line=line).set_marker_edge_width(width=width)

        if self.legend is None:
            # Marker (uniform)
            if isinstance(marker, dict):
                raise TypeError("Marker must be a string when legend is not set.")
            if isinstance(marker, str):
                for line in lines.standard():
                    self._style(line=line).set_marker(marker=marker)

            # Marker face color (uniform)
            if isinstance(face_color, dict):
                raise TypeError(
                    "Marker face color must be a string when legend is not set."
                )
            if isinstance(face_color, str):
                for line in lines.standard():
                    self._style(line=line).set_marker_color(color=face_color)

            # Marker face alpha (uniform)
            if isinstance(face_alpha, dict):
                raise TypeError(
                    "Marker face alpha must be a float when legend is not set."
                )
            if isinstance(face_alpha, float):
                for line in lines.standard():
                    self._style(line=line).set_marker_alpha(alpha=face_alpha)

            # Marker size (uniform)
            if isinstance(size, dict):
                raise TypeError("Marker size must be an int when legend is not set.")
            if isinstance(size, int):
                for line in lines.standard():
                    self._style(line=line).set_marker_size(size=size)

            # Marker edge color (uniform)
            if isinstance(edge_color, dict):
                raise TypeError(
                    "Marker edge color must be a string when legend is not set."
                )
            if isinstance(edge_color, str):
                for line in lines.standard():
                    self._style(line=line).set_marker_edge_color(color=edge_color)

            # Marker edge alpha (uniform)
            if isinstance(edge_alpha, dict):
                raise TypeError(
                    "Marker edge alpha must be a float when legend is not set."
                )
            if isinstance(edge_alpha, float):
                for line in lines.standard():
                    self._style(line=line).set_marker_edge_alpha(alpha=edge_alpha)

            # Marker edge width (uniform)
            if isinstance(edge_width, dict):
                raise TypeError(
                    "Marker edge width must be a float when legend is not set."
                )
            if isinstance(edge_width, float):
                for line in lines.standard():
                    self._style(line=line).set_marker_edge_width(width=edge_width)
