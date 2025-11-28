from dataclasses import dataclass
from matplotlib.font_manager import FontProperties
from matplotlib.legend import Legend
from matplotlib.text import Text


@dataclass
class TitleProperties:
    """Encapsulates properties for styling a legend title."""

    font: FontProperties | str | None
    size: int | None
    color: str | None


class TitleStyler:
    """Applies styling properties to a legend title."""

    def __init__(self, title: Text) -> None:
        self.title = title

    def set_font(self, font: FontProperties | str | None) -> None:
        """Set the font of a legend title."""

        if font is not None:
            self.title.set_fontproperties(font)

    def set_size(self, size: int | None) -> None:
        """Set the font size of a legend title."""

        if size is not None:
            self.title.set_fontsize(size)

    def set_color(self, color: str | None) -> None:
        """Set the font color of a legend title."""

        if color is not None:
            self.title.set_color(color)

    def style(self, properties: TitleProperties) -> None:
        """Apply the given title properties to the legend title."""

        self.set_font(properties.font)
        self.set_size(properties.size)
        self.set_color(properties.color)


class TitleDrawer:
    """Draws and styles the legend title."""

    def __init__(self, legend: Legend) -> None:
        self.legend = legend

    def draw(self, properties: TitleProperties) -> None:
        """Draw and style the legend title."""

        title = self.legend.get_title()
        TitleStyler(title=title).style(properties=properties)
