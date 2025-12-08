from typing import Any, Callable
from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Patch

BEZIER_CONSTANT = 0.5522847498


@dataclass(frozen=True)
class FDL_FrameDimension:
    width: float
    height: float


@dataclass(frozen=True)
class FDL_FrameAnchor:
    x_min: float
    y_min: float
    dimension: FDL_FrameDimension

    @property
    def x_max(self) -> float:
        return self.x_min + self.dimension.width

    @property
    def y_max(self) -> float:
        return self.y_min + self.dimension.height


@dataclass(frozen=True)
class FDL_FrameCornerRadii:
    rx: float
    ry: float

    def clamp(self, max_width: float, max_height: float) -> "FDL_FrameCornerRadii":
        """Clamp corner radii to not exceed half of the frame dimension."""

        clamped_rx = max(0.0, min(abs(max_width) / 2.0, abs(self.rx)))
        clamped_ry = max(0.0, min(abs(max_height) / 2.0, abs(self.ry)))
        return FDL_FrameCornerRadii(clamped_rx, clamped_ry)

    @property
    def is_rounded(self) -> bool:
        return self.rx > 0.0 or self.ry > 0.0


@dataclass(frozen=True)
class FDL_StraightEdge:
    end_point: tuple[float, float]

    def add_to_path(self, verts: list[tuple[float, float]], codes: list[Any]) -> None:
        """Add straight edge to path vertices and codes."""

        verts.append(self.end_point)
        codes.append(Path.LINETO)


@dataclass(frozen=True)
class FDL_RoundedCorner:
    control_point_1: tuple[float, float]
    control_point_2: tuple[float, float]
    end_point: tuple[float, float]

    def add_to_path(self, verts: list[tuple[float, float]], codes: list[Any]) -> None:
        """Add rounded corner to path vertices and codes."""

        verts.extend([self.control_point_1, self.control_point_2, self.end_point])
        codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])


@dataclass(frozen=True)
class FDL_RoundedEdge:
    straight_edge: FDL_StraightEdge
    rounded_corner: FDL_RoundedCorner

    def add_to_path(self, verts: list[tuple[float, float]], codes: list[Any]) -> None:
        """Add rounded edge (straight edge + rounded corner) to path."""

        self.straight_edge.add_to_path(verts, codes)
        self.rounded_corner.add_to_path(verts, codes)


class FDL_PathBuilder:
    """Builder for frame path with rounded corners."""

    def __init__(self, anchor: FDL_FrameAnchor, radii: FDL_FrameCornerRadii):
        self.anchor = anchor
        self.radii = radii
        self.control_point_x = radii.rx * BEZIER_CONSTANT
        self.control_point_y = radii.ry * BEZIER_CONSTANT
        self.edge_builders: list[Callable[[], FDL_RoundedEdge]] = [
            self.build_bottom_edge,
            self.build_left_edge,
            self.build_top_edge,
            self.build_right_edge,
        ]

    def get_start_point(self) -> tuple[float, float]:
        """Get the starting point for the path (left-bottom anchor point after radius)."""

        return (
            self.anchor.x_min + self.radii.rx,
            self.anchor.y_min,
        )

    def build_bottom_edge(self) -> FDL_RoundedEdge:
        """Build the bottom horizontal edge with bottom-left rounded corner path."""

        x_min = self.anchor.x_min
        y_min = self.anchor.y_min
        rx, ry = self.radii.rx, self.radii.ry
        cpx, cpy = self.control_point_x, self.control_point_y

        edge = FDL_StraightEdge(end_point=(x_min + rx, y_min))
        corner = FDL_RoundedCorner(
            control_point_1=(x_min + rx - cpx, y_min),
            control_point_2=(x_min, y_min + ry - cpy),
            end_point=(x_min, y_min + ry),
        )
        return FDL_RoundedEdge(straight_edge=edge, rounded_corner=corner)

    def build_left_edge(self) -> FDL_RoundedEdge:
        """Build the left vertical edge with top-left rounded corner path."""

        x_min = self.anchor.x_min
        y_max = self.anchor.y_max
        rx, ry = self.radii.rx, self.radii.ry
        cpx, cpy = self.control_point_x, self.control_point_y

        edge = FDL_StraightEdge(end_point=(x_min, y_max - ry))
        corner = FDL_RoundedCorner(
            control_point_1=(x_min, y_max - ry + cpy),
            control_point_2=(x_min + rx - cpx, y_max),
            end_point=(x_min + rx, y_max),
        )
        return FDL_RoundedEdge(straight_edge=edge, rounded_corner=corner)

    def build_top_edge(self) -> FDL_RoundedEdge:
        """Build the top horizontal edge with top-right rounded corner path."""

        x_max = self.anchor.x_max
        y_max = self.anchor.y_max
        rx, ry = self.radii.rx, self.radii.ry
        cpx, cpy = self.control_point_x, self.control_point_y

        edge = FDL_StraightEdge(end_point=(x_max - rx, y_max))
        corner = FDL_RoundedCorner(
            control_point_1=(x_max - rx + cpx, y_max),
            control_point_2=(x_max, y_max - ry + cpy),
            end_point=(x_max, y_max - ry),
        )
        return FDL_RoundedEdge(straight_edge=edge, rounded_corner=corner)

    def build_right_edge(self) -> FDL_RoundedEdge:
        """Build the right vertical edge with bottom-right rounded corner path."""

        x_max = self.anchor.x_max
        y_min = self.anchor.y_min
        rx, ry = self.radii.rx, self.radii.ry
        cpx, cpy = self.control_point_x, self.control_point_y

        edge = FDL_StraightEdge(end_point=(x_max, y_min + ry))
        corner = FDL_RoundedCorner(
            control_point_1=(x_max, y_min + ry - cpy),
            control_point_2=(x_max - rx + cpx, y_min),
            end_point=(x_max - rx, y_min),
        )
        return FDL_RoundedEdge(straight_edge=edge, rounded_corner=corner)

    def build(self) -> Path:

        verts: list[tuple[float, float]] = []
        codes: list[Any] = []

        start_point = self.get_start_point()

        verts.append(start_point)
        codes.append(Path.MOVETO)
        for edge_builder in self.edge_builders:
            edge_builder().add_to_path(verts, codes)
        verts.append(start_point)
        codes.append(Path.CLOSEPOLY)

        return Path(verts, codes)


class FDL_FrameBuilder:
    """Builder for data label frame with rounded corners."""

    def __init__(self, ax: Axes, anchor: FDL_FrameAnchor, radii: FDL_FrameCornerRadii):
        self.ax = ax
        self.anchor = anchor
        self.radii = radii

    def build(self) -> Patch:

        clamped_radii = self.radii.clamp(
            max_width=self.anchor.dimension.width,
            max_height=self.anchor.dimension.height,
        )

        path = FDL_PathBuilder(self.anchor, clamped_radii).build()
        frame = PathPatch(path, zorder=3, transform=self.ax.transData)
        return self.ax.add_patch(frame)
