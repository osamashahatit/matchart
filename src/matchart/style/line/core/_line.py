from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.colors import to_rgba

from ._utils import LineStyleHelper, LineGenerator


class LineStyler:

    def __init__(self, line: Line2D) -> None:
        self.line = line

    def set_line_color(self, color: str | None) -> None:

        self.line.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.line.set_color((r, g, b, a))

    def set_line_alpha(self, alpha: float | None) -> None:

        self.line.set_alpha(None)
        if alpha is not None:
            r, g, b, _ = to_rgba(self.line.get_color())
            self.line.set_color((r, g, b, alpha))

    def set_line_style(self, style: str | None) -> None:

        if style is not None:
            self.line.set_linestyle(style)


class LineDrawer:

    def __init__(self, ax: Axes, legend: str | None) -> None:
        self.ax = ax
        self.legend = legend
        self.help = LineStyleHelper(ax=self.ax)

    def _style(self, line: Line2D) -> LineStyler:
        return LineStyler(line=line)

    def draw(
        self,
        color: str | dict[str, str] | None = None,
        alpha: float | dict[str, float] | None = None,
        style: str | dict[str, str] | None = None,
    ) -> None:
        """
        Set line properties.

        Parameters
        ----------
        color : str | dict[str, str] | None. Default is None.
            Line color as a single string or a dictionary mapping legend labels to colors.
        alpha : float | dict[str, float] | None. Default is None.
            Line alpha as a single float or a dictionary mapping legend labels to alpha values.
        style : str | dict[str, str] | None. Default is None.
            Line style as a single string or a dictionary mapping legend labels to styles.
        """

        lines = LineGenerator(ax=self.ax)

        if self.legend is not None:
            # Line color
            if isinstance(color, str):
                raise TypeError("Line color must be a dictionary when legend is set.")
            if isinstance(color, dict):
                self.help.validate_legend_entry(dict=color)
                for line, color in lines.map_legend(property=color):
                    self._style(line).set_line_color(color=color)
            # Line alpha
            if isinstance(alpha, float):
                raise TypeError("Line alpha must be a dictionary when legend is set.")
            if isinstance(alpha, dict):
                self.help.validate_legend_entry(dict=alpha)
                for line, alpha in lines.map_legend(property=alpha):
                    self._style(line).set_line_alpha(alpha=alpha)
            # Line style
            if isinstance(style, str):
                raise TypeError("Line style must be a dictionary when legend is set.")
            if isinstance(style, dict):
                self.help.validate_legend_entry(dict=style)
                for line, style in lines.map_legend(property=style):
                    self._style(line).set_line_style(style=style)

        if self.legend is None:
            # Line color
            if isinstance(color, dict):
                raise TypeError("Line color must be a string when legend is not set.")
            if isinstance(color, str):
                for line in lines.standard():
                    self._style(line).set_line_color(color=color)
            # Line alpha
            if isinstance(alpha, dict):
                raise TypeError("Line alpha must be a float when legend is not set.")
            if isinstance(alpha, float):
                for line in lines.standard():
                    self._style(line).set_line_alpha(alpha=alpha)
            # Line style
            if isinstance(style, dict):
                raise TypeError("Line style must be a string when legend is not set.")
            if isinstance(style, str):
                for line in lines.standard():
                    self._style(line).set_line_style(style=style)
