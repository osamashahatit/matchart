from dataclasses import dataclass
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
from matplotlib.container import BarContainer


@dataclass
class MarkerProperties:
    """Encapsulates properties for styling a legend marker."""

    marker: str | None
    size: float | None


class MarkerStyler:
    """Applies styling properties to custom legend markers."""

    def __init__(self, handles: list[Artist]) -> None:
        self.handles = handles

    def get_color(self, handle: Artist) -> str | tuple | None:
        """Extract color from different handle types."""

        if isinstance(handle, BarContainer) and handle.patches:
            return handle.patches[0].get_facecolor()
        if isinstance(handle, Line2D):
            return handle.get_color()
        return None

    def style(self, properties: MarkerProperties) -> list[Line2D]:
        """Apply the given marker properties to custom legend markers."""

        return [
            Line2D(
                [],
                [],
                marker=properties.marker,
                color="none",
                markerfacecolor=self.get_color(handle),
                markeredgecolor="none",
                markersize=properties.size,
            )
            for handle in self.handles
        ]


class MarkerDrawer:
    """Draws and styles custom legend markers."""

    def __init__(self, handles: list[Artist]) -> None:
        self.handles = handles

    def draw(self, properties: MarkerProperties) -> list[Line2D]:
        """Draw and style custom legend markers."""

        return MarkerStyler(handles=self.handles).style(properties=properties)
