from typing import Literal
from dataclasses import dataclass
from matplotlib.axis import Axis, XAxis, YAxis
from matplotlib.markers import MarkerStyle, TICKLEFT, TICKRIGHT, TICKUP, TICKDOWN
from matplotlib.transforms import Affine2D
from matplotlib.lines import Line2D
from matplotlib.ticker import AutoMinorLocator, NullLocator, MultipleLocator

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
    """Encapsulates styling properties for tick markers."""

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
    """Settings for tick markers on an axis."""

    tick1_active: bool
    tick2_active: bool
    tick1_marker: MarkerType
    tick2_marker: MarkerType


class MarkerResolver:
    """Resolves which tick markers are active and their default styles."""

    def __init__(self, axis: Axis) -> None:
        self.axis = axis

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

    def get_active_position(self) -> tuple[bool, bool]:
        """Determine which tick positions are active based on axis type."""

        if isinstance(self.axis, XAxis):
            position_map = self._XAXIS_POSITION_MAP
        elif isinstance(self.axis, YAxis):
            position_map = self._YAXIS_POSITION_MAP
        else:
            return (True, True)
        position = self.axis.get_ticks_position()
        return position_map.get(position, (True, False))

    def get_default_marker(self) -> tuple[MarkerType, MarkerType]:
        """Get default markers based on axis type."""

        if isinstance(self.axis, YAxis):
            return ("line_left", "line_right")
        elif isinstance(self.axis, XAxis):
            return ("line_down", "line_up")
        return ("line_left", "line_right")

    def resolve(self) -> MarkerSettings:
        """Resolve complete tick settings for an axis."""

        tick1_active, tick2_active = self.get_active_position()
        tick1_marker, tick2_marker = self.get_default_marker()
        return MarkerSettings(
            tick1_active=tick1_active,
            tick2_active=tick2_active,
            tick1_marker=tick1_marker,
            tick2_marker=tick2_marker,
        )


class MarkerStyler:
    """Applies styling to tick markers."""

    def __init__(
        self,
        line: Line2D,
        marker: MarkerType,
        properties: MarkerProperties,
    ) -> None:
        self.line = line
        self.properties = properties
        self.marker = marker

    def set_color(self) -> None:
        """Apply color properties to the marker."""

        if self.properties.face_color is not None:
            self.line.set_markerfacecolor(self.properties.face_color)
        if self.properties.border_color is not None:
            self.line.set_markeredgecolor(self.properties.border_color)

    def set_dimension(self) -> None:
        """Apply size and width properties to the marker."""

        if self.properties.border_width is not None:
            self.line.set_markeredgewidth(self.properties.border_width)
        if self.properties.size is not None:
            self.line.set_markersize(self.properties.size)

    def set_marker(self) -> None:
        """Apply marker styling with transformations."""

        resolved_marker = (
            LINE_MAP[self.marker]
            if isinstance(self.marker, str) and self.marker in LINE_MAP
            else self.marker
        )
        transform = (
            Affine2D()
            .rotate_deg(self.properties.rotation)
            .translate(
                self.properties.x_offset,
                self.properties.y_offset,
            )
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
        """Apply styling to a single tick marker."""

        if not self.line.get_visible():
            return
        self.set_color()
        self.set_dimension()
        self.set_marker()


class MajorMarkerDrawer:
    """Drawer for styling major tick markers on matplotlib axes."""

    def __init__(self, axis: Axis) -> None:
        self.axis = axis
        self._resolver = MarkerResolver(axis).resolve()

    def enable(self, show: bool = True) -> "MajorMarkerDrawer":
        """
        Enable or disable visibility of major tick markers.

        Parameters
        ----------
        show : bool, default=True
            Whether to show (`True`) or hide (`False`) the major tick markers.

        Returns
        -------
        MajorMarkerDrawer
            The current instance for method chaining.
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
        """
        Apply styling to major tick markers.

        Parameters
        ----------
        marker : {"line_left", "line_right", "line_up", "line_down"} | MarkerStyle. Default is None.
            Custom marker style. Defaults to axis-specific markers if not given.
        face_color : str. Default is None.
            Fill color of the tick markers.
        border_color : str. Default is None.
            Color of the tick marker border.
        border_width : float. Default is None.
            Width of the tick marker border.
        size : float. Default is None.
            Size of the tick markers.
        fill_style : {"full", "left", "right", "bottom", "top", "none"}. Default is "full".
            Fill style for the marker.
        cap_style : {"butt", "round", "projecting"}. Default is "butt".
            Cap style for marker border.
        x_offset : float. Default is 0.
            Horizontal offset of the marker in display units.
        y_offset : float. Default is 0.
            Vertical offset of the marker in display units.
        rotation : float. Default is 0.
            Rotation angle of the marker in degrees.
        step : int | None. Default is None.
            Interval between major ticks based on the axis tick values.
            If specified, automatically recalculates the major tick
            positions using `MultipleLocator`.

        Returns
        -------
        MajorMarkerDrawer
            The current instance for method chaining.
        """

        if step is not None:
            min, max = self.axis.get_view_interval()
            ticks = MultipleLocator(step).tick_values(min, max)
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
    """Drawer for styling minor tick markers on matplotlib axes."""

    def __init__(
        self,
        axis: Axis,
    ) -> None:
        self.axis = axis
        self._resolver = MarkerResolver(axis).resolve()
        self._show = True

    def enable(self, show: bool = True) -> "MinorMarkerDrawer":
        """
        Enable or disable visibility of minor tick markers.

        Parameters
        ----------
        show : bool, default=True
            Whether to show (`True`) or hide (`False`) the minor tick markers.

        Returns
        -------
        MinorMarkerDrawer
            The current instance for method chaining.
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
        """
        Apply styling to minor tick markers.

        Parameters
        ----------
        marker : {"line_left", "line_right", "line_up", "line_down"} | MarkerStyle. Default is None.
            Custom marker style. Defaults to axis-specific markers if not given.
        face_color : str. Default is None.
            Fill color of the tick markers.
        border_color : str. Default is None.
            Color of the tick marker border.
        border_width : float | None. Default is None.
            Width of the tick marker border.
        size : float | None. Default is None.
            Size of the tick markers.
        fill_style : {"full", "left", "right", "bottom", "top", "none"}. Default is "full".
            Fill style for the marker.
        cap_style : {"butt", "round", "projecting"}. Default is "butt".
            Cap style for marker borders.
        x_offset : float. Default is 0.
            Horizontal offset of the marker in display units.
        y_offset : float. Default is 0.
            Vertical offset of the marker in display units.
        rotation : float. Default is 0.
            Rotation angle of the marker in degrees.
        step : int | None. Default is None.
            Number of subdivisions between major ticks for minor tick placement.

        Returns
        -------
        MinorMarkerDrawer
            The current instance for method chaining.
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
