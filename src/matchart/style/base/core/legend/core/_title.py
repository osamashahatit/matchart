"""Style legend title."""

from dataclasses import dataclass

from matplotlib.font_manager import FontProperties
from matplotlib.legend import Legend
from matplotlib.text import Text


@dataclass
class TitleProperties:
    """Store styling properties for a legend title.

    Attributes:
        font (FontProperties | str | None): Title font configuration. When
            provided as a string, it is passed through to
            Text.set_fontproperties(). Common usage is a font family name
            (e.g., "DejaVu Sans").
        size (int | None): Font size in points.
        color (str | None): Text color.
    """

    font: FontProperties | str | None
    size: int | None
    color: str | None


class TitleStyler:
    """Apply TitleProperties to a legend title Text artist."""

    def __init__(self, title: Text) -> None:
        """
        Args:
            title (Text): Legend title Text artist to style.
        """
        self.title = title

    def set_font(self, font: FontProperties | str | None) -> None:
        """Set the font of the legend title.

        Args:
            font (FontProperties | str | None): Font configuration to apply.
        """
        if font is not None:
            self.title.set_fontproperties(font)

    def set_size(self, size: int | None) -> None:
        """Set the font size of the legend title.

        Args:
            size (int | None): Font size in points.
        """
        if size is not None:
            self.title.set_fontsize(size)

    def set_color(self, color: str | None) -> None:
        """Set the color of the legend title.

        Args:
            color (str | None): Matplotlib-compatible color string.
        """
        if color is not None:
            self.title.set_color(color)

    def style(self, properties: TitleProperties) -> None:
        """Apply title styling properties to the legend title.

        Args:
            properties (TitleProperties): Title styling configuration.

        Returns:
            None: The title Text artist is modified in place.
        """
        self.set_font(properties.font)
        self.set_size(properties.size)
        self.set_color(properties.color)


class TitleDrawer:
    """Fetch and style a legend title from a Legend object."""

    def __init__(self, legend: Legend) -> None:
        """
        Args:
            legend (Legend): Matplotlib legend whose title will be styled.
        """
        self.legend = legend

    def draw(self, properties: TitleProperties) -> None:
        """Draw and style the legend title.

        Args:
            properties (TitleProperties): Title styling configuration.

        Returns:
            None: The legend title Text artist is modified in place.
        """
        title = self.legend.get_title()
        TitleStyler(title=title).style(properties=properties)
