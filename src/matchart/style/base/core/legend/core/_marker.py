"""Style legend marker."""

from dataclasses import dataclass

from matplotlib.artist import Artist
from matplotlib.container import BarContainer
from matplotlib.lines import Line2D
from matplotlib.typing import ColorType


@dataclass
class MarkerProperties:
    """Store properties used to construct custom legend marker handles.

    Attributes:
        marker (str | None): Marker glyph used for legend handles. This is
            passed through to Line2D(marker=...). Common options include
            "o", "s", "^", "D", "x", and "+".
        size (float | None): Marker size in points.
    """

    marker: str | None
    size: float | None


class MarkerStyler:
    """Convert plot handles into styled Line2D marker handles."""

    def __init__(self, handles: list[Artist]) -> None:
        """
        Args:
            handles (list[Artist]): Original legend handles whose colors
                should be reflected in the generated marker handles.
        """
        self.handles = handles

    def get_color(self, handle: Artist) -> ColorType | None:
        """Extract a representative color from a legend handle.

        Args:
            handle (Artist): Matplotlib artist or container.

        Returns:
            ColorType | None: Color value to use for markerfacecolor, or
            None when the handle type is unsupported.
        """
        if isinstance(handle, BarContainer) and handle.patches:
            return handle.patches[0].get_facecolor()

        if isinstance(handle, Line2D):
            return handle.get_color()

        return None

    def style(self, properties: MarkerProperties) -> list[Line2D]:
        """Create styled Line2D marker handles from the input handles.

        Args:
            properties (MarkerProperties): Marker glyph and size settings.

        Returns:
            list[Line2D]: New legend handles suitable for passing to
            ax.legend(handles=...).
        """
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
    """Facade for building custom legend marker handles."""

    def __init__(self, handles: list[Artist]) -> None:
        """
        Args:
            handles (list[Artist]): Original legend handles to convert.
        """
        self.handles = handles

    def draw(self, properties: MarkerProperties) -> list[Line2D]:
        """Build and return custom legend marker handles.

        Args:
            properties (MarkerProperties): Marker glyph and size settings.

        Returns:
            list[Line2D]: New Line2D handles for use in a legend.
        """
        return MarkerStyler(handles=self.handles).style(properties=properties)
