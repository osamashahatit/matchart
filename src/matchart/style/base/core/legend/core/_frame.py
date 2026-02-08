"""Style legend frame."""

from dataclasses import dataclass

from matplotlib.colors import to_rgba
from matplotlib.legend import Legend
from matplotlib.patches import FancyBboxPatch, Rectangle


@dataclass
class FrameProperties:
    """Store styling properties for a legend frame.

    Attributes:
        face_color (str | None): Background color for the legend frame.
        face_alpha (float | None): Alpha override for the frame background.
        border_color (str | None): Border (edge) color for the frame.
        border_alpha (float | None): Alpha override for the frame border.
        border_style (str | None): Line style for the border (e.g. "-", "--").
        border_width (float | None): Line width for the border, in points.
        border_radius (float | None): Corner radius for rounded frames.
    """

    face_color: str | None
    face_alpha: float | None
    border_color: str | None
    border_alpha: float | None
    border_style: str | None
    border_width: float | None
    border_radius: float | None


class FrameStyler:
    """Apply FrameProperties to a legend frame patch."""

    def __init__(self, frame: Rectangle) -> None:
        """
        Args:
            frame (Rectangle): Legend frame patch retrieved from
                Legend.get_frame(). (Often a FancyBboxPatch at runtime.)
        """
        self.frame = frame

    def set_face_color(self, color: str | None) -> None:
        """Set the background color of the legend frame.

        Args:
            color (str | None): Matplotlib-compatible color string.
        """
        # Reset global alpha so per-channel RGBA values are respected.
        self.frame.set_alpha(None)

        if color is not None:
            r, g, b, a = to_rgba(color)
            self.frame.set_facecolor((r, g, b, a))

    def set_face_alpha(self, alpha: float | None) -> None:
        """Override the alpha channel of the legend frame background.

        Args:
            alpha (float | None): Alpha value in [0, 1].
        """
        self.frame.set_alpha(None)

        if alpha is not None:
            r, g, b, _ = to_rgba(self.frame.get_facecolor())
            self.frame.set_facecolor((r, g, b, alpha))

    def set_border_color(self, color: str | None) -> None:
        """Set the border color of the legend frame.

        Args:
            color (str | None): Matplotlib-compatible color string.
        """
        self.frame.set_alpha(None)

        if color is not None:
            r, g, b, a = to_rgba(color)
            self.frame.set_edgecolor((r, g, b, a))

    def set_border_alpha(self, alpha: float | None) -> None:
        """Override the alpha channel of the legend frame border.

        Args:
            alpha (float | None): Alpha value in [0, 1].
        """
        self.frame.set_alpha(None)

        if alpha is not None:
            r, g, b, _ = to_rgba(self.frame.get_edgecolor())
            self.frame.set_edgecolor((r, g, b, alpha))

    def set_border_style(self, style: str | None) -> None:
        """Set the border line style.

        Args:
            style (str | None): Matplotlib linestyle string (e.g. "-", "--", ":").
        """
        if style is not None:
            self.frame.set_linestyle(style)

    def set_border_width(self, width: float | None) -> None:
        """Set the border line width.

        Args:
            width (float | None): Line width in points.
        """
        if width is not None:
            self.frame.set_linewidth(width)

    def set_border_radius(self, radius: float | None) -> None:
        """Set the corner radius for rounded legend frames.

        Args:
            radius (float | None): Corner radius in points. Applied only
                when the frame patch is a FancyBboxPatch.
        """
        if radius is not None and isinstance(self.frame, FancyBboxPatch):
            self.frame.set_boxstyle("round", rounding_size=radius)  # type:ignore

    def style(self, properties: FrameProperties) -> None:
        """Apply the given frame properties to the legend frame.

        Args:
            properties (FrameProperties): Frame styling configuration.

        Returns:
            None: The legend frame patch is modified in place.
        """
        self.set_face_color(color=properties.face_color)
        self.set_face_alpha(alpha=properties.face_alpha)
        self.set_border_color(color=properties.border_color)
        self.set_border_alpha(alpha=properties.border_alpha)
        self.set_border_style(style=properties.border_style)
        self.set_border_width(width=properties.border_width)
        self.set_border_radius(radius=properties.border_radius)


class FrameDrawer:
    """Fetch and style a legend frame from a Legend object."""

    def __init__(self, legend: Legend) -> None:
        """
        Args:
            legend (Legend): Matplotlib legend whose frame will be styled.
        """
        self.legend = legend

    def draw(self, properties: FrameProperties) -> None:
        """Draw and style the legend frame.

        Args:
            properties (FrameProperties): Frame styling configuration.

        Returns:
            None: The legend frame patch is modified in place.
        """
        frame = self.legend.get_frame()
        FrameStyler(frame=frame).style(properties=properties)
