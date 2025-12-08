from dataclasses import dataclass
from matplotlib.patches import Patch
from matplotlib.colors import to_rgba


@dataclass(frozen=True)
class FDL_Frame_Properties:
    face_color: str | None
    face_alpha: float | None
    border_color: str | None
    border_alpha: float | None
    border_style: str | None
    border_width: float | None
    border_radius: float | None


class FDLFrameStyler:

    def __init__(self, frame: Patch) -> None:
        self.frame = frame

    def set_face_color(self, color: str | None) -> None:

        self.frame.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.frame.set_facecolor((r, g, b, a))

    def set_face_alpha(self, alpha: float | None) -> None:

        self.frame.set_alpha(None)
        if alpha is not None:
            r, g, b, _ = to_rgba(self.frame.get_facecolor())
            self.frame.set_facecolor((r, g, b, alpha))

    def set_border_color(self, color: str | None) -> None:

        self.frame.set_alpha(None)
        if color is not None:
            r, g, b, a = to_rgba(color)
            self.frame.set_edgecolor((r, g, b, a))

    def set_border_alpha(self, alpha: float | None) -> None:

        self.frame.set_alpha(None)
        if alpha is not None:
            r, g, b, _ = to_rgba(self.frame.get_edgecolor())
            self.frame.set_edgecolor((r, g, b, alpha))

    def set_border_style(self, style: str | None) -> None:

        if style is not None:
            self.frame.set_linestyle(style)

    def set_border_width(self, width: float | None) -> None:

        if width is not None:
            self.frame.set_linewidth(width)

    def style(self, properties: FDL_Frame_Properties, gid: str | None = None) -> None:

        self.set_face_color(color=properties.face_color)
        self.set_face_alpha(alpha=properties.face_alpha)
        self.set_border_color(color=properties.border_color)
        self.set_border_alpha(alpha=properties.border_alpha)
        self.set_border_style(style=properties.border_style)
        self.set_border_width(width=properties.border_width)

        if gid is not None:
            self.frame.set_gid(gid)
