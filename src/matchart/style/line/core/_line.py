"""Style Line2D."""

from matplotlib.axes import Axes
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D

from ._utils import LineStyleHelper, LineYielder


class LineStyler:
    """Apply styling to a single Line2D artist."""

    def __init__(self, line: Line2D) -> None:
        """
        Args:
            line (Line2D): Line artist to style.
        """
        self.line = line

    def set_line_color(self, color: str | None) -> None:
        """Set the line color.

        Args:
            color (str | None): Matplotlib-compatible color string. If None, no
                change is applied.

        Notes:
            Resets the global alpha (line.set_alpha(None)) so the alpha channel
            in the RGBA color is respected.
        """
        self.line.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.line.set_color((r, g, b, a))

    def set_line_alpha(self, alpha: float | None) -> None:
        """Override the alpha channel of the line's current color.

        Args:
            alpha (float | None): Alpha value in [0.0, 1.0]. If None, no change
                is applied.

        Notes:
            Resets the global alpha (line.set_alpha(None)) so the alpha channel
            in the RGBA color is respected.
        """
        self.line.set_alpha(None)
        if alpha is not None:
            r, g, b, _ = to_rgba(self.line.get_color())
            self.line.set_color((r, g, b, alpha))

    def set_line_style(self, style: str | None) -> None:
        """Set the line style.

        Args:
            style (str | None): Matplotlib linestyle string. If None, no change
                is applied.
        """
        if style is not None:
            self.line.set_linestyle(style)


class LineDrawer:
    """Apply styling across Line2D artists on an Axes."""

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

    def _style(self, line: Line2D) -> LineStyler:
        """Create a LineStyler for a given line artist."""
        return LineStyler(line=line)

    def draw(
        self,
        color: str | dict[str, str] | None = None,
        alpha: float | dict[str, float] | None = None,
        style: str | dict[str, str] | None = None,
    ) -> None:
        """Set line properties using scalar or legend-mapped inputs.

        In legend mode (legend is not None), properties must be provided as
        dictionaries mapping legend labels to values. Otherwise, properties are
        applied uniformly to all lines.

        Args:
            color (str | dict[str, str] | None): Line color specification:
              - str: apply one color to all lines (legend=None only).
              - dict[str, str]: map legend labels to colors (legend mode).
            alpha (float | dict[str, float] | None): Line alpha specification:
              - float: apply one alpha to all lines (legend=None only).
              - dict[str, float]: map legend labels to alpha values
                (legend mode).
            style (str | dict[str, str] | None): Line style specification:
              - str: apply one style to all lines (legend=None only).
              - dict[str, str]: map legend labels to styles (legend mode).
              - Options: "-", "--", "-.", ":", "None"

        Raises:
            TypeError: If legend is set and a scalar is provided instead of a
                dict, or if legend is not set and a dict is provided.

        Notes:
            This method mutates Line2D artists in place and does not return self
            (not chainable).
        """
        lines = LineYielder(ax=self.ax)

        if self.legend is not None:
            # Line color (legend-mapped)
            if isinstance(color, str):
                raise TypeError("Line color must be a dictionary when legend is set.")
            if isinstance(color, dict):
                self.helper.validate_legend_entry(mapping=color)
                for line, color in lines.map_legend(property=color):
                    self._style(line).set_line_color(color=color)

            # Line alpha (legend-mapped)
            if isinstance(alpha, float):
                raise TypeError("Line alpha must be a dictionary when legend is set.")
            if isinstance(alpha, dict):
                self.helper.validate_legend_entry(mapping=alpha)
                for line, alpha in lines.map_legend(property=alpha):
                    self._style(line).set_line_alpha(alpha=alpha)

            # Line style (legend-mapped)
            if isinstance(style, str):
                raise TypeError("Line style must be a dictionary when legend is set.")
            if isinstance(style, dict):
                self.helper.validate_legend_entry(mapping=style)
                for line, style in lines.map_legend(property=style):
                    self._style(line).set_line_style(style=style)

        if self.legend is None:
            # Line color (uniform)
            if isinstance(color, dict):
                raise TypeError("Line color must be a string when legend is not set.")
            if isinstance(color, str):
                for line in lines.standard():
                    self._style(line).set_line_color(color=color)

            # Line alpha (uniform)
            if isinstance(alpha, dict):
                raise TypeError("Line alpha must be a float when legend is not set.")
            if isinstance(alpha, float):
                for line in lines.standard():
                    self._style(line).set_line_alpha(alpha=alpha)

            # Line style (uniform)
            if isinstance(style, dict):
                raise TypeError("Line style must be a string when legend is not set.")
            if isinstance(style, str):
                for line in lines.standard():
                    self._style(line).set_line_style(style=style)
