"""Style framed data-label patches with face and border properties."""

from dataclasses import dataclass

from matplotlib.colors import to_rgba
from matplotlib.patches import Patch


@dataclass(frozen=True)
class FDL_Frame_Properties:
    """Store visual styling properties for a framed data label.

    Attributes:
        face_color (str | None): Background color for the frame.
        face_alpha (float | None): Alpha override for the frame background.
        border_color (str | None): Border (edge) color for the frame.
        border_alpha (float | None): Alpha override for the frame border.
        border_style (str | None): Line style for the border.
        border_width (float | None): Line width for the border.
        border_radius (float | None): Desired corner radius (currently
            unused by this styler).
    """

    face_color: str | None
    face_alpha: float | None
    border_color: str | None
    border_alpha: float | None
    border_style: str | None
    border_width: float | None
    border_radius: float | None


class FDLFrameStyler:
    """Apply visual styling to a framed data-label Patch."""

    def __init__(self, frame: Patch) -> None:
        """
        Args:
            frame (Patch): Matplotlib patch representing the frame.
        """
        self.frame = frame

    def set_face_color(self, color: str | None) -> None:
        """Set the frame background color.

        Args:
            color (str | None): Matplotlib-compatible color string.
        """
        # Reset global alpha to ensure RGBA values are respected.
        self.frame.set_alpha(None)

        if color is not None:
            r, g, b, a = to_rgba(color)
            self.frame.set_facecolor((r, g, b, a))

    def set_face_alpha(self, alpha: float | None) -> None:
        """Override the alpha channel of the frame background.

        Args:
            alpha (float | None): Alpha value in [0, 1].
        """
        self.frame.set_alpha(None)

        if alpha is not None:
            r, g, b, _ = to_rgba(self.frame.get_facecolor())
            self.frame.set_facecolor((r, g, b, alpha))

    def set_border_color(self, color: str | None) -> None:
        """Set the frame border color.

        Args:
            color (str | None): Matplotlib-compatible color string.
        """
        self.frame.set_alpha(None)

        if color is not None:
            r, g, b, a = to_rgba(color)
            self.frame.set_edgecolor((r, g, b, a))

    def set_border_alpha(self, alpha: float | None) -> None:
        """Override the alpha channel of the frame border.

        Args:
            alpha (float | None): Alpha value in [0, 1].
        """
        self.frame.set_alpha(None)

        if alpha is not None:
            r, g, b, _ = to_rgba(self.frame.get_edgecolor())
            self.frame.set_edgecolor((r, g, b, alpha))

    def set_border_style(self, style: str | None) -> None:
        """Set the frame border line style.

        Args:
            style (str | None): Matplotlib line style string.
        """
        if style is not None:
            self.frame.set_linestyle(style)

    def set_border_width(self, width: float | None) -> None:
        """Set the frame border line width.

        Args:
            width (float | None): Line width in points.
        """
        if width is not None:
            self.frame.set_linewidth(width)

    def style(self, properties: FDL_Frame_Properties, gid: str | None = None) -> None:
        """Apply all frame styling properties.

        Args:
            properties (FDL_Frame_Properties): Styling configuration.
            gid (str | None): Optional Matplotlib artist group id.

        Returns:
            None: The frame patch is modified in place.
        """
        self.set_face_color(color=properties.face_color)
        self.set_face_alpha(alpha=properties.face_alpha)
        self.set_border_color(color=properties.border_color)
        self.set_border_alpha(alpha=properties.border_alpha)
        self.set_border_style(style=properties.border_style)
        self.set_border_width(width=properties.border_width)

        if gid is not None:
            self.frame.set_gid(gid)
