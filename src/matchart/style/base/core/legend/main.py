"""Style and draw Matplotlib legends."""

from typing import Literal

from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D

from .core._frame import FrameDrawer, FrameProperties
from .core._marker import MarkerDrawer, MarkerProperties
from .core._title import TitleDrawer, TitleProperties

type Orientation = Literal["horizontal", "vertical"]
type Alignment = Literal["left", "center", "right"]
type Position = Literal[
    "best",
    "upper right",
    "upper left",
    "lower left",
    "lower right",
    "right",
    "center left",
    "center right",
    "lower center",
    "upper center",
    "center",
]


class LegendStyler:
    """Configure and render a Matplotlib legend."""

    def __init__(self, ax: Axes) -> None:
        """
        Args:
            ax (Axes): Axes on which the legend will be created/styled.
        """
        self.ax = ax

        # Frame properties
        self._frame_show: bool = True
        self._frame_properties: FrameProperties | None = None

        # Label properties
        self._label_font: FontProperties | str | None = None
        self._label_size: int | None = None
        self._label_color: str | None = None

        # Layout properties
        self._marker_first: bool = True
        self._v_pad: float | None = None
        self._h_pad: float | None = None
        self._box_pad: float | None = None
        self._marker_pad: float | None = None
        self._align: Alignment = "left"

        # Marker properties
        self._marker_properties: MarkerProperties | None = None
        self._custom_markers: list[Line2D] | None = None
        self._custom_labels: list[str] | None = None

        # Position properties
        self._position: Position | None = "upper right"
        self._bbox_to_anchor: tuple[float, float] | None = None

        # Title properties
        self._title_text: str | None = None
        self._title_properties: TitleProperties | None = None

    def frame(
        self,
        show: bool = True,
        face_color: str | None = None,
        face_alpha: float | None = None,
        border_color: str | None = None,
        border_alpha: float | None = None,
        border_style: str | None = None,
        border_width: float | None = None,
        border_radius: float | None = None,
    ) -> "LegendStyler":
        """Configure the legend frame appearance.

        Args:
            show (bool): Whether to show the legend frame.
            face_color (str | None): Frame background color.
            face_alpha (float | None): Background alpha in [0.0, 1.0].
            border_color (str | None): Frame border color.
            border_alpha (float | None): Border alpha in [0.0, 1.0].
            border_style (str | None): Border line style (e.g. "-", "--").
            border_width (float | None): Border line width in points.
            border_radius (float | None): Corner radius for rounded frames.

        Returns:
            LegendStyler: The current instance for method chaining.
        """
        self._frame_show = show
        self._frame_properties = FrameProperties(
            face_color=face_color,
            face_alpha=face_alpha,
            border_color=border_color,
            border_alpha=border_alpha,
            border_style=border_style,
            border_width=border_width,
            border_radius=border_radius,
        )
        return self

    def label(
        self,
        font: FontProperties | str | None = None,
        size: int | None = None,
        color: str | None = None,
    ) -> "LegendStyler":
        """Configure legend label text styling.

        Args:
            font (FontProperties | str | None): Label font configuration.
                If a string is provided, it is treated as a font family
                name (e.g., "DejaVu Sans").
            size (int | None): Font size in points.
            color (str | None): Text color for labels.

        Returns:
            LegendStyler: The current instance for method chaining.
        """
        if isinstance(font, str):
            self._label_font = FontProperties(family=font, size=size)
        if isinstance(font, FontProperties):
            self._label_font = FontProperties(fname=str(font.get_file()), size=size)

        self._label_size = size
        self._label_color = color
        return self

    def layout(
        self,
        marker_first: bool = True,
        v_pad: float | None = None,
        h_pad: float | None = None,
        box_pad: float | None = None,
        marker_pad: float | None = None,
        align: Alignment = "left",
    ) -> "LegendStyler":
        """Configure legend layout and spacing.

        Args:
            marker_first (bool): Whether to draw the marker before the label.
            v_pad (float | None): Vertical spacing between legend entries.
            h_pad (float | None): Horizontal spacing between legend columns.
            box_pad (float | None): Padding between legend content and frame.
            marker_pad (float | None): Spacing between marker and text.
            align (Alignment): Alignment of legend entries.
                Options: "left", "center", "right".

        Returns:
            LegendStyler: The current instance for method chaining.
        """
        self._marker_first = marker_first
        self._v_pad = v_pad
        self._h_pad = h_pad
        self._box_pad = box_pad
        self._marker_pad = marker_pad
        self._align = align
        return self

    def marker(
        self,
        marker: str | None = None,
        size: float | None = None,
    ) -> "LegendStyler":
        """Configure custom marker handles for the legend.

        Args:
            marker (str | None): Marker glyph used to represent each handle.
                Common options include "o", "s", "^", "D", "x", and "+".
                When None, axis-specific default legend markers are used.
            size (float | None): Marker size in points.

        Returns:
            LegendStyler: The current instance for method chaining.
        """
        self._marker_properties = MarkerProperties(marker=marker, size=size)
        return self

    def position(
        self,
        position: Position = "upper right",
        x_offset: float | None = None,
        y_offset: float | None = None,
    ) -> "LegendStyler":
        """Configure the legend placement.

        Args:
            position (Position): Legend location.
                Options: "best", "upper right", "upper left", "lower left",
                "lower right", "right", "center left", "center right",
                "lower center", "upper center", "center".
            x_offset (float | None): Optional x offset applied to the anchor
                point when provided (in axes fraction units).
            y_offset (float | None): Optional y offset applied to the anchor
                point when provided (in axes fraction units).

        Returns:
            LegendStyler: The current instance for method chaining.
        """
        _anchor_map = {
            "upper right": (1.0, 1.0),
            "upper left": (0.0, 1.0),
            "lower left": (0.0, 0.0),
            "lower right": (1.0, 0.0),
            "right": (1.0, 0.5),
            "center left": (0.0, 0.5),
            "center right": (1.0, 0.5),
            "lower center": (0.5, 0.0),
            "upper center": (0.5, 1.0),
            "center": (0.5, 0.5),
        }

        self._position = position
        if x_offset is not None or y_offset is not None:
            base_x, base_y = _anchor_map.get(position, (0.5, 0.5))
            self._bbox_to_anchor = (
                base_x + (x_offset or 0.0),
                base_y + (y_offset or 0.0),
            )
        return self

    def title(
        self,
        text: str | None = None,
        font: FontProperties | str | None = None,
        color: str | None = None,
        size: int | None = None,
    ) -> "LegendStyler":
        """Configure the legend title.

        Args:
            text (str | None): Title text to set on the legend.
            font (FontProperties | str | None): Title font configuration.
                If a string is provided, it is treated as a font family
                name (e.g., "DejaVu Sans").
            color (str | None): Title text color.
            size (int | None): Title font size in points.

        Returns:
            LegendStyler: The current instance for method chaining.
        """
        self._title_text = text
        self._title_properties = TitleProperties(font=font, size=size, color=color)
        return self

    def draw(self, orientation: Orientation = "vertical") -> None:
        """Create/update the legend and apply configured styling.

        Before calling draw(), configure the desired appearance using any
        combination of:
          - frame()
          - label()
          - layout()
          - marker()
          - position()
          - title()

        Args:
            orientation (Orientation): Legend entry flow direction.
                Options: "vertical", "horizontal".

        Returns:
            None: The Axes legend is created/updated and styled in place.
        """
        handles, labels = self.ax.get_legend_handles_labels()

        # Merge handles/labels from overlayed axes sharing the same bbox.
        for ax in self.ax.figure.axes:
            if ax != self.ax and (ax.bbox.bounds == self.ax.bbox.bounds):
                handle, label = ax.get_legend_handles_labels()
                handles.extend(handle)
                labels.extend(label)

        if self._marker_properties is not None:
            self._custom_markers = MarkerDrawer(handles).draw(self._marker_properties)
            self._custom_labels = labels

        self.ax.legend(  # type:ignore
            handles=self._custom_markers if self._custom_markers else handles,
            labels=self._custom_labels if self._custom_markers else labels,
            ncol=len(labels) if orientation == "horizontal" else 1,
            loc=self._position,
            markerfirst=self._marker_first,
            prop=self._label_font,
            labelcolor=self._label_color,
            fontsize=self._label_size,
            labelspacing=self._v_pad,
            columnspacing=self._h_pad,
            borderpad=self._box_pad,
            handletextpad=self._marker_pad,
            bbox_to_anchor=self._bbox_to_anchor,
            alignment=self._align,
        )

        legend = self.ax.get_legend()

        if legend is not None:
            if self._frame_show is not False:
                legend.set_frame_on(True)
                if self._frame_properties:
                    FrameDrawer(legend).draw(properties=self._frame_properties)

        if legend is not None:
            if self._title_text is not None:
                legend.set_title(self._title_text)
                if self._title_properties is not None:
                    TitleDrawer(legend).draw(properties=self._title_properties)
