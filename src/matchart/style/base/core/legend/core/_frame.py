from dataclasses import dataclass
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.legend import Legend
from matplotlib.colors import to_rgba


@dataclass
class FrameProperties:
    """Encapsulates properties for styling a legend frame."""

    face_color: str | None
    face_alpha: float | None
    border_color: str | None
    border_alpha: float | None
    border_style: str | None
    border_width: float | None
    border_radius: float | None


class FrameStyler:
    """Applies styling properties to a legend frame."""

    def __init__(self, frame: Rectangle) -> None:
        self.frame = frame

    def set_face_color(self, color: str | None) -> None:
        """Set the face (background) color of a legend frame."""

        self.frame.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.frame.set_facecolor((r, g, b, a))

    def set_face_alpha(self, alpha: float | None) -> None:
        """Set the face (background) alpha of a legend frame."""

        self.frame.set_alpha(None)
        if alpha is not None:
            r, g, b, _ = to_rgba(self.frame.get_facecolor())
            self.frame.set_facecolor((r, g, b, alpha))

    def set_border_color(self, color: str | None) -> None:
        """Set the border color of a legend frame."""

        self.frame.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.frame.set_edgecolor((r, g, b, a))

    def set_border_alpha(self, alpha: float | None) -> None:
        """Set the border alpha of a legend frame."""

        self.frame.set_alpha(None)
        if alpha is not None:
            r, g, b, _ = to_rgba(self.frame.get_edgecolor())
            self.frame.set_edgecolor((r, g, b, alpha))

    def set_border_style(self, style: str | None) -> None:
        """Set the border line style of a legend frame."""

        if style is not None:
            self.frame.set_linestyle(style)

    def set_border_width(self, width: float | None) -> None:
        """Set the border line width of a legend frame."""

        if width is not None:
            self.frame.set_linewidth(width)

    def set_border_radius(self, radius: float | None) -> None:
        """Set the corner radius of a legend frame for rounded borders."""

        if radius is not None and isinstance(self.frame, FancyBboxPatch):
            self.frame.set_boxstyle("round", rounding_size=radius)

    def style(self, properties: FrameProperties) -> None:
        """Apply the given frame properties to the legend frame."""

        self.set_face_color(color=properties.face_color)
        self.set_face_alpha(alpha=properties.face_alpha)
        self.set_border_color(color=properties.border_color)
        self.set_border_alpha(alpha=properties.border_alpha)
        self.set_border_style(style=properties.border_style)
        self.set_border_width(width=properties.border_width)
        self.set_border_radius(radius=properties.border_radius)


class FrameDrawer:
    """Draws and styles the legend frame."""

    def __init__(self, legend: Legend) -> None:
        self.legend = legend

    def draw(self, properties: FrameProperties) -> None:
        """Draw and style the legend frame."""

        frame = self.legend.get_frame()
        FrameStyler(frame=frame).style(properties=properties)
