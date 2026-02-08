"""Build rounded frame patches for data labels using Matplotlib paths.

Data labels often use a visible "frame" (background box) to improve
readability against chart elements. Matplotlib provides basic patch
primitives, but creating rounded-rectangle frames positioned in data
coordinates with precise control over corner radii requires explicit
path construction. This module defines a small set of geometry helpers
and builders that produce a PathPatch representing a rectangular frame
with optional rounded corners, suitable for reuse across chart types.
"""

from dataclasses import dataclass
from typing import Any, Callable

from matplotlib.axes import Axes
from matplotlib.patches import Patch, PathPatch
from matplotlib.path import Path

BEZIER_CONSTANT = 0.5522847498


@dataclass(frozen=True)
class FDL_FrameDimension:
    """Represent frame size in data units.

    Attributes:
        width (float): Frame width in data units.
        height (float): Frame height in data units.
    """

    width: float
    height: float


@dataclass(frozen=True)
class FDL_FrameAnchor:
    """Represent the frame position and size in data coordinates.

    Attributes:
        x_min (float): Lower-left x coordinate in data units.
        y_min (float): Lower-left y coordinate in data units.
        dimension (FDL_FrameDimension): Frame width/height in data units.
    """

    x_min: float
    y_min: float
    dimension: FDL_FrameDimension

    @property
    def x_max(self) -> float:
        """Compute the maximum x coordinate (x_min + width)."""
        return self.x_min + self.dimension.width

    @property
    def y_max(self) -> float:
        """Compute the maximum y coordinate (y_min + height)."""
        return self.y_min + self.dimension.height


@dataclass(frozen=True)
class FDL_FrameCornerRadii:
    """Represent corner radii for a frame in data units.

    Attributes:
        rx (float): Horizontal radius in data units.
        ry (float): Vertical radius in data units.
    """

    rx: float
    ry: float

    def clamp(self, max_width: float, max_height: float) -> "FDL_FrameCornerRadii":
        """Clamp radii to not exceed half the frame dimensions.

        Args:
            max_width (float): Frame width in data units.
            max_height (float): Frame height in data units.

        Returns:
            FDL_FrameCornerRadii: A new radii instance with clamped values.
        """
        clamped_rx = max(0.0, min(abs(max_width) / 2.0, abs(self.rx)))
        clamped_ry = max(0.0, min(abs(max_height) / 2.0, abs(self.ry)))
        return FDL_FrameCornerRadii(clamped_rx, clamped_ry)

    @property
    def is_rounded(self) -> bool:
        """Return True if either radius is non-zero."""
        return self.rx > 0.0 or self.ry > 0.0


@dataclass(frozen=True)
class FDL_StraightEdge:
    """Represent a straight edge segment ending at end_point.

    Attributes:
        end_point (tuple[float, float]): Segment endpoint in data units.
    """

    end_point: tuple[float, float]

    def add_to_path(self, verts: list[tuple[float, float]], codes: list[Any]) -> None:
        """Append a straight edge segment to a Path definition.

        Args:
            verts (list[tuple[float, float]]): Path vertices list to mutate.
            codes (list[Any]): Path code list to mutate.
        """
        verts.append(self.end_point)
        codes.append(Path.LINETO)


@dataclass(frozen=True)
class FDL_RoundedCorner:
    """Represent a rounded corner as a cubic Bezier curve.

    Attributes:
        control_point_1 (tuple[float, float]): First Bezier control point.
        control_point_2 (tuple[float, float]): Second Bezier control point.
        end_point (tuple[float, float]): Curve end point.
    """

    control_point_1: tuple[float, float]
    control_point_2: tuple[float, float]
    end_point: tuple[float, float]

    def add_to_path(self, verts: list[tuple[float, float]], codes: list[Any]) -> None:
        """Append a rounded corner segment to a Path definition.

        Args:
            verts (list[tuple[float, float]]): Path vertices list to mutate.
            codes (list[Any]): Path code list to mutate.
        """
        verts.extend([self.control_point_1, self.control_point_2, self.end_point])
        codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])


@dataclass(frozen=True)
class FDL_RoundedEdge:
    """Represent a straight edge followed by a rounded corner.

    Attributes:
        straight_edge (FDL_StraightEdge): Straight segment.
        rounded_corner (FDL_RoundedCorner): Rounded corner segment.
    """

    straight_edge: FDL_StraightEdge
    rounded_corner: FDL_RoundedCorner

    def add_to_path(self, verts: list[tuple[float, float]], codes: list[Any]) -> None:
        """Append this edge (straight + corner) to a Path definition.

        Args:
            verts (list[tuple[float, float]]): Path vertices list to mutate.
            codes (list[Any]): Path code list to mutate.
        """
        self.straight_edge.add_to_path(verts, codes)
        self.rounded_corner.add_to_path(verts, codes)


class FDL_PathBuilder:
    """Build a closed Path for a rectangular frame with rounded corners."""

    def __init__(self, anchor: FDL_FrameAnchor, radii: FDL_FrameCornerRadii):
        """
        Args:
            anchor (FDL_FrameAnchor): Frame placement and size in data units.
            radii (FDL_FrameCornerRadii): Corner radii in data units.
        """
        self.anchor = anchor
        self.radii = radii
        self.control_point_x = radii.rx * BEZIER_CONSTANT
        self.control_point_y = radii.ry * BEZIER_CONSTANT

        # Edge builders are visited in the order used to traverse the frame.
        self.edge_builders: list[Callable[[], FDL_RoundedEdge]] = [
            self.build_bottom_edge,
            self.build_left_edge,
            self.build_top_edge,
            self.build_right_edge,
        ]

    def get_start_point(self) -> tuple[float, float]:
        """Return the path start point (bottom edge, after left radius).

        Returns:
            tuple[float, float]: Starting vertex in data units.
        """
        return (self.anchor.x_min + self.radii.rx, self.anchor.y_min)

    def build_bottom_edge(self) -> FDL_RoundedEdge:
        """Build the bottom edge and bottom-left rounded corner.

        Returns:
            FDL_RoundedEdge: Segment for the bottom edge and corner.
        """
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
        """Build the left edge and top-left rounded corner.

        Returns:
            FDL_RoundedEdge: Segment for the left edge and corner.
        """
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
        """Build the top edge and top-right rounded corner.

        Returns:
            FDL_RoundedEdge: Segment for the top edge and corner.
        """
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
        """Build the right edge and bottom-right rounded corner.

        Returns:
            FDL_RoundedEdge: Segment for the right edge and corner.
        """
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
        """Build and return the closed Path for the frame outline.

        Returns:
            Path: Matplotlib path describing the frame outline.
        """
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
    """Create and add a data-label frame patch to a Matplotlib Axes."""

    def __init__(self, ax: Axes, anchor: FDL_FrameAnchor, radii: FDL_FrameCornerRadii):
        """
        Args:
            ax (Axes): Target axes to add the frame patch to.
            anchor (FDL_FrameAnchor): Frame placement and size in data units.
            radii (FDL_FrameCornerRadii): Corner radii in data units.
        """
        self.ax = ax
        self.anchor = anchor
        self.radii = radii

    def build(self) -> Patch:
        """Build and add the frame patch.

        Returns:
            Patch: The added PathPatch instance (returned by ax.add_patch()).
        """
        clamped_radii = self.radii.clamp(
            max_width=self.anchor.dimension.width,
            max_height=self.anchor.dimension.height,
        )

        path = FDL_PathBuilder(self.anchor, clamped_radii).build()
        frame = PathPatch(path, zorder=3, transform=self.ax.transData)
        return self.ax.add_patch(frame)
