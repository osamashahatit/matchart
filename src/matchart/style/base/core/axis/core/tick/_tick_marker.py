"""Style and format Matplotlib tick markers."""

from dataclasses import dataclass
from typing import Literal

from matplotlib.axis import Axis, XAxis, YAxis
from matplotlib.lines import Line2D
from matplotlib.markers import TICKDOWN, TICKLEFT, TICKRIGHT, TICKUP, MarkerStyle
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, NullLocator
from matplotlib.transforms import Affine2D

type CapStyle = Literal["butt", "round", "projecting"]
type FillStyle = Literal["full", "left", "right", "bottom", "top", "none"]
type LineType = Literal["line_left", "line_right", "line_up", "line_down"]
type MarkerType = MarkerStyle | LineType | str

LINE_MAP: dict[str, int] = {
    "line_left": TICKLEFT,
    "line_right": TICKRIGHT,
    "line_up": TICKUP,
    "line_down": TICKDOWN,
}


@dataclass(frozen=True)
class MarkerProperties:
    """Store styling properties for tick markers."""

    marker: MarkerType | None
    face_color: str | None
    border_color: str | None
    border_width: float | None
    size: float | None
    fill_style: FillStyle
    cap_style: CapStyle
    x_offset: float
    y_offset: float
    rotation: float


@dataclass(frozen=True)
class MarkerSettings:
    """Store resolved tick-side activation and default markers.

    Attributes:
        tick1_active (bool): Whether tick1line is considered active.
        tick2_active (bool): Whether tick2line is considered active.
        tick1_marker (MarkerType): Default marker for tick1line.
        tick2_marker (MarkerType): Default marker for tick2line.
    """

    tick1_active: bool
    tick2_active: bool
    tick1_marker: MarkerType
    tick2_marker: MarkerType


class MarkerResolver:
    """Resolve which tick markers are active and their default marker types."""

    _YAXIS_POSITION_MAP = {
        "left": (True, False),
        "right": (False, True),
        "both": (True, True),
        "none": (False, False),
    }

    _XAXIS_POSITION_MAP = {
        "bottom": (True, False),
        "top": (False, True),
        "both": (True, True),
        "none": (False, False),
    }

    def __init__(self, axis: Axis) -> None:
        """
        Args:
            axis (Axis): Matplotlib axis (XAxis or YAxis) to inspect.
        """
        self.axis = axis

    def get_active_position(self) -> tuple[bool, bool]:
        """Determine which tick sides are active based on axis type.

        Returns:
            tuple[bool, bool]: (tick1_active, tick2_active).
        """
        if isinstance(self.axis, XAxis):
            position_map = self._XAXIS_POSITION_MAP
        elif isinstance(self.axis, YAxis):
            position_map = self._YAXIS_POSITION_MAP
        else:
            return True, True

        position = self.axis.get_ticks_position()
        return position_map.get(position, (True, False))

    def get_default_marker(self) -> tuple[MarkerType, MarkerType]:
        """Return the default tick1 and tick2 markers for the axis type.

        Returns:
            tuple[MarkerType, MarkerType]: (tick1_marker, tick2_marker).
        """
        if isinstance(self.axis, YAxis):
            return "line_left", "line_right"
        if isinstance(self.axis, XAxis):
            return "line_down", "line_up"
        return "line_left", "line_right"

    def resolve(self) -> MarkerSettings:
        """Resolve the full marker settings for the current axis.

        Returns:
            MarkerSettings: Resolved activation and default markers.
        """
        tick1_active, tick2_active = self.get_active_position()
        tick1_marker, tick2_marker = self.get_default_marker()
        return MarkerSettings(
            tick1_active=tick1_active,
            tick2_active=tick2_active,
            tick1_marker=tick1_marker,
            tick2_marker=tick2_marker,
        )


class MarkerStyler:
    """Apply marker styling to a single tick Line2D artist."""

    def __init__(
        self,
        line: Line2D,
        marker: MarkerType,
        properties: MarkerProperties,
    ) -> None:
        """
        Args:
            line (Line2D): Tick line artist to style.
            marker (MarkerType): Marker spec to apply for this tick line.
            properties (MarkerProperties): Style settings to apply.
        """
        self.line = line
        self.properties = properties
        self.marker = marker

    def set_color(self) -> None:
        """Apply face and edge colors to the marker."""
        if self.properties.face_color is not None:
            self.line.set_markerfacecolor(self.properties.face_color)
        if self.properties.border_color is not None:
            self.line.set_markeredgecolor(self.properties.border_color)

    def set_dimension(self) -> None:
        """Apply edge width and marker size."""
        if self.properties.border_width is not None:
            self.line.set_markeredgewidth(self.properties.border_width)
        if self.properties.size is not None:
            self.line.set_markersize(self.properties.size)

    def set_marker(self) -> None:
        """Apply marker geometry with rotation and translation transforms."""
        resolved_marker = (
            LINE_MAP[self.marker]
            if isinstance(self.marker, str) and self.marker in LINE_MAP
            else self.marker
        )
        transform = (
            Affine2D()
            .rotate_deg(self.properties.rotation)
            .translate(self.properties.x_offset, self.properties.y_offset)
        )
        self.line.set_marker(
            MarkerStyle(
                marker=resolved_marker,
                fillstyle=self.properties.fill_style,
                transform=transform,
                capstyle=self.properties.cap_style,
            )
        )

    def style(self) -> None:
        """Apply the full style to the tick marker if the line is visible."""
        if not self.line.get_visible():
            return

        self.set_color()
        self.set_dimension()
        self.set_marker()


class MajorMarkerDrawer:
    """Enable and style major tick markers on a Matplotlib axis."""

    def __init__(self, axis: Axis) -> None:
        """
        Args:
            axis (Axis): Matplotlib axis (XAxis or YAxis) to modify.
        """
        self.axis = axis
        self._resolver = MarkerResolver(axis).resolve()

    def enable(self, show: bool = True) -> "MajorMarkerDrawer":
        """Enable or disable visibility of major tick markers.

        Args:
            show (bool): Whether to show (True) or hide (False) the major tick
                marker lines.

        Returns:
            MajorMarkerDrawer: The current instance for method chaining.
        """
        ticks = self.axis.get_major_ticks()
        for tick in ticks:
            if self._resolver.tick1_active:
                tick.tick1line.set_visible(show)
            if self._resolver.tick2_active:
                tick.tick2line.set_visible(show)
        return self

    def draw(
        self,
        marker: MarkerType | None = None,
        face_color: str | None = None,
        border_color: str | None = None,
        border_width: float | None = None,
        size: float | None = None,
        fill_style: FillStyle = "full",
        cap_style: CapStyle = "butt",
        x_offset: float = 0,
        y_offset: float = 0,
        rotation: float = 0,
        step: int | None = None,
    ) -> "MajorMarkerDrawer":
        """Apply styling to major tick markers.

        Args:
            marker (MarkerType | None): Optional marker override. If a
                LineType string is provided, options are: "line_left",
                "line_right", "line_up", "line_down".
            face_color (str | None): Optional marker fill color.
            border_color (str | None): Optional marker edge color.
            border_width (float | None): Optional marker edge width.
            size (float | None): Optional marker size.
            fill_style (FillStyle): Marker fillstyle.
                Options: "full", "left", "right", "bottom", "top", "none".
            cap_style (CapStyle): Cap style for marker strokes.
                Options: "butt", "round", "projecting".
            x_offset (float): Horizontal marker translation offset.
            y_offset (float): Vertical marker translation offset.
            rotation (float): Marker rotation in degrees.
            step (int | None): Optional interval for major ticks based on axis
                values. When provided, sets MultipleLocator(step).

        Returns:
            MajorMarkerDrawer: The current instance for method chaining.

        Raises:
            ValueError: If the computed tick count exceeds 30 when step is set.
        """
        if step is not None:
            view_min, view_max = self.axis.get_view_interval()
            ticks = MultipleLocator(step).tick_values(view_min, view_max)
            if len(ticks) > 30:
                raise ValueError(f"Tick count:({len(ticks)}), increase step size.")
            self.axis.set_major_locator(MultipleLocator(step))

        properties = MarkerProperties(
            border_color=border_color,
            border_width=border_width,
            face_color=face_color,
            size=size,
            marker=marker,
            fill_style=fill_style,
            cap_style=cap_style,
            x_offset=x_offset,
            y_offset=y_offset,
            rotation=rotation,
        )

        ticks = self.axis.get_major_ticks()
        for tick in ticks:
            tick1_marker = marker if marker is not None else self._resolver.tick1_marker
            tick2_marker = marker if marker is not None else self._resolver.tick2_marker

            MarkerStyler(
                line=tick.tick1line,
                properties=properties,
                marker=tick1_marker,
            ).style()
            MarkerStyler(
                line=tick.tick2line,
                properties=properties,
                marker=tick2_marker,
            ).style()

        return self


class MinorMarkerDrawer:
    """Enable and style minor tick markers on a Matplotlib axis."""

    def __init__(self, axis: Axis) -> None:
        """
        Args:
            axis (Axis): Matplotlib axis (XAxis or YAxis) to modify.
        """
        self.axis = axis
        self._resolver = MarkerResolver(axis).resolve()
        self._show = True

    def enable(self, show: bool = True) -> "MinorMarkerDrawer":
        """Enable or disable visibility of minor tick markers.

        Args:
            show (bool): Whether to show (True) or hide (False) minor tick
                markers. When False, a NullLocator is set for minor ticks.

        Returns:
            MinorMarkerDrawer: The current instance for method chaining.
        """
        if not show:
            self.axis.set_minor_locator(NullLocator())
        else:
            self.axis.set_minor_locator(AutoMinorLocator(6))

        self._show = show
        return self

    def draw(
        self,
        marker: MarkerType | None = None,
        face_color: str | None = None,
        border_color: str | None = None,
        border_width: float | None = None,
        size: float | None = None,
        fill_style: FillStyle = "full",
        cap_style: CapStyle = "butt",
        x_offset: float = 0,
        y_offset: float = 0,
        rotation: float = 0,
        step: int = 5,
    ) -> "MinorMarkerDrawer":
        """Apply styling to minor tick markers.

        Args:
            marker (MarkerType | None): Optional marker override. If a
                LineType string is provided, options are: "line_left",
                "line_right", "line_up", "line_down".
            face_color (str | None): Optional marker fill color.
            border_color (str | None): Optional marker edge color.
            border_width (float | None): Optional marker edge width.
            size (float | None): Optional marker size.
            fill_style (FillStyle): Marker fillstyle.
                Options: "full", "left", "right", "bottom", "top", "none".
            cap_style (CapStyle): Cap style for marker strokes.
                Options: "butt", "round", "projecting".
            x_offset (float): Horizontal marker translation offset.
            y_offset (float): Vertical marker translation offset.
            rotation (float): Marker rotation in degrees.
            step (int): Number of subdivisions between major ticks.
                Used as AutoMinorLocator(step + 1).

        Returns:
            MinorMarkerDrawer: The current instance for method chaining.
        """
        if self._show:
            self.axis.set_minor_locator(AutoMinorLocator(step + 1))

        properties = MarkerProperties(
            border_color=border_color,
            border_width=border_width,
            face_color=face_color,
            size=size,
            marker=marker,
            fill_style=fill_style,
            cap_style=cap_style,
            x_offset=x_offset,
            y_offset=y_offset,
            rotation=rotation,
        )

        ticks = self.axis.get_minor_ticks()
        for tick in ticks:
            tick1_marker = marker if marker is not None else self._resolver.tick1_marker
            tick2_marker = marker if marker is not None else self._resolver.tick2_marker

            MarkerStyler(
                line=tick.tick1line,
                properties=properties,
                marker=tick1_marker,
            ).style()
            MarkerStyler(
                line=tick.tick2line,
                properties=properties,
                marker=tick2_marker,
            ).style()

        return self
