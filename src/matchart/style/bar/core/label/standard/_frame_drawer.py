"""Draw bar chart standard framed data labels."""

from dataclasses import dataclass
from typing import cast

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.patches import PathPatch, Rectangle

from matchart.style.bar.core._utils import BarPatchYielder, BarStyleHelper
from matchart.style.utils.data_label.frame_autosizer import FrameAutoSizer
from matchart.style.utils.data_label.frame_builder import (
    FDL_FrameAnchor,
    FDL_FrameBuilder,
    FDL_FrameCornerRadii,
    FDL_FrameDimension,
)
from matchart.style.utils.data_label.frame_labeler import (
    FDL_Label_AlignProperties,
    FDL_Label_HAlign,
    FDL_Label_PadProperties,
    FDL_Label_Properties,
    FDL_Label_VAlign,
    FramedDataLabeler,
)
from matchart.style.utils.data_label.frame_styler import (
    FDL_Frame_Properties,
    FDLFrameStyler,
)
from matchart.style.utils.input_converter import PointDataConverter
from matchart.style.utils.num_formatter import (
    NumberFormat,
    NumberFormatter,
    NumberProperties,
    ScaleType,
)

from ._frame_anchor import (
    FDL_Bar_Bounds,
    FDL_Bar_FrameDimension,
    FDL_HBar_Anchor,
    FDL_HBar_HAlign,
    FDL_HBar_VAlign,
    FDL_VBar_Anchor,
    FDL_VBar_HAlign,
    FDL_VBar_VAlign,
)


@dataclass(frozen=True)
class FDL_Bar_LabelProperties:
    """Configure framed bar label font appearance."""

    font: FontProperties | None
    size: int
    color: str


@dataclass(frozen=True)
class FDL_Bar_Label_AlignProperties:
    """Configure text alignment inside the frame."""

    h_align: FDL_Label_HAlign
    v_align: FDL_Label_VAlign


@dataclass(frozen=True)
class FDL_Bar_Label_PadProperties:
    """Configure per-side padding between the frame and the label text."""

    left: float | None
    right: float | None
    top: float | None
    bottom: float | None


@dataclass(frozen=True)
class FDL_Bar_FrameProperties:
    """Configure the framed label background patch appearance."""

    face_color: str | None
    face_alpha: float | None
    border_color: str | None
    border_alpha: float | None
    border_style: str | None
    border_width: float
    border_radius: float
    custom_width: float | None
    custom_height: float | None


@dataclass(frozen=True)
class FDL_Bar_Frame_AlignProperties:
    """Configure how the frame is anchored relative to each bar."""

    h_align: FDL_HBar_HAlign | FDL_VBar_HAlign
    v_align: FDL_HBar_VAlign | FDL_VBar_VAlign
    x_offset: float
    y_offset: float


class FDL_Bar:
    """Iterate bar patches on an Axes and draw framed numeric labels."""

    def __init__(
        self,
        ax: Axes,
        fig: Figure,
        horizontal: bool,
        patches: BarPatchYielder,
        helper: BarStyleHelper,
        threshold: float,
        formatter: NumberFormatter,
        label: FDL_Bar_LabelProperties,
        label_align: FDL_Bar_Label_AlignProperties,
        label_pad: FDL_Bar_Label_PadProperties,
        frame: FDL_Bar_FrameProperties,
        frame_align: FDL_Bar_Frame_AlignProperties,
    ):
        """
        Args:
            ax (Axes): Target axes that already contains bar artists.
            fig (Figure): Figure used for text measurements and conversions.
            horizontal (bool): Whether the bar chart is horizontal.
            patches (BarPatchYielder): Patch yielder for bar patches.
            helper (BarStyleHelper): Helper class.
            threshold (float): Minimum absolute bar value required for a label
                to be drawn. A label is drawn only when abs(value) > threshold.
            formatter (NumberFormatter): Number formatter.
            label (FDL_Bar_LabelProperties): Label appearance configuration.
            label_align (FDL_Bar_Label_AlignProperties): Label alignment inside
                the frame.
            label_pad (FDL_Bar_Label_PadProperties): Padding between frame and
                text (points).
            frame (FDL_Bar_FrameProperties): Frame appearance configuration.
            frame_align (FDL_Bar_Frame_AlignProperties): Frame anchor alignment
                and offsets (points).
        """
        self.ax = ax
        self.fig = fig
        self.horizontal = horizontal
        self.patches = patches.standard()
        self.helper = helper
        self.threshold = threshold
        self.formatter = formatter
        self.label = label
        self.label_align = label_align
        self.label_pad = label_pad
        self.frame = frame
        self.frame_align = frame_align

    def draw(self, default_pad: float) -> None:
        """Draw framed labels for bars that exceed the configured threshold.

        Args:
            default_pad (float): Default padding in points used when a specific
                pad side is not provided.

        Notes:
            This method mutates the Axes by adding frame patches and Text
            artists. It does not return self (not chainable).
        """
        for patch in self.patches:
            if isinstance(patch, Rectangle):
                patch_value = self.helper.get_patch_value(patch=patch)

                # Skip small bars using absolute-value thresholding.
                if abs(patch_value) > self.threshold:
                    bbox = patch.get_bbox()
                    bounds = FDL_Bar_Bounds(
                        bbox.x0,
                        bbox.y0,
                        bbox.x1,
                        bbox.y1,
                    )

                    # Measure the frame in points based on the formatted label.
                    frame = FrameAutoSizer(
                        fig=self.fig,
                        pad=default_pad,
                        font=self.label.font,
                        size=self.label.size,
                        formatter=self.formatter,
                    ).measure_frame(
                        label=patch_value,
                        custom_width=self.frame.custom_width,
                        custom_height=self.frame.custom_height,
                    )

                    width = frame.width
                    height = frame.height

                    # Convert all point-based properties into data units for
                    # correct positioning on the current Axes scale.
                    converter = PointDataConverter(ax=self.ax, fig=self.fig)

                    frame_x, frame_y = (
                        converter.convert("x", width),
                        converter.convert("y", height),
                    )
                    offset_x, offset_y = (
                        converter.convert("x", self.frame_align.x_offset),
                        converter.convert("y", self.frame_align.y_offset),
                    )
                    border_x, border_y = (
                        converter.convert("x", self.frame.border_width),
                        converter.convert("y", self.frame.border_width),
                    )
                    radius_x, radius_y = (
                        converter.convert("x", self.frame.border_radius),
                        converter.convert("y", self.frame.border_radius),
                    )

                    # Per-side padding, defaulting to default_pad when None.
                    pad_left_data = (
                        converter.convert(axis="x", points=self.label_pad.left)
                        if self.label_pad.left is not None
                        else converter.convert(axis="x", points=default_pad)
                    )
                    pad_right_data = (
                        converter.convert(axis="x", points=self.label_pad.right)
                        if self.label_pad.right is not None
                        else converter.convert(axis="x", points=default_pad)
                    )
                    pad_top_data = (
                        converter.convert(axis="y", points=self.label_pad.top)
                        if self.label_pad.top is not None
                        else converter.convert(axis="y", points=default_pad)
                    )
                    pad_bottom_data = (
                        converter.convert(axis="y", points=self.label_pad.bottom)
                        if self.label_pad.bottom is not None
                        else converter.convert(axis="y", points=default_pad)
                    )

                    dimension = FDL_Bar_FrameDimension(
                        width=frame_x,
                        height=frame_y,
                        border_width_x=border_x,
                        border_width_y=border_y,
                    )

                    # Compute frame anchor differently for horizontal vs.
                    # vertical bars so alignment literals stay correct.
                    if self.horizontal:
                        anchor = FDL_HBar_Anchor(
                            bounds=bounds,
                            dimension=dimension,
                        ).anchor(
                            h_align=self.frame_align.h_align,
                            v_align=cast(FDL_HBar_VAlign, self.frame_align.v_align),
                        )
                    else:
                        anchor = FDL_VBar_Anchor(
                            bounds=bounds,
                            dimension=dimension,
                        ).anchor(
                            h_align=cast(FDL_VBar_HAlign, self.frame_align.h_align),
                            v_align=self.frame_align.v_align,
                        )

                    # Build the frame patch at the anchored + offset position.
                    frame = FDL_FrameBuilder(
                        ax=self.ax,
                        anchor=FDL_FrameAnchor(
                            x_min=anchor.x + offset_x,
                            y_min=anchor.y + offset_y,
                            dimension=FDL_FrameDimension(width=frame_x, height=frame_y),
                        ),
                        radii=FDL_FrameCornerRadii(rx=radius_x, ry=radius_y),
                    ).build()

                    # Apply frame styling and tag it for cleanup.
                    FDLFrameStyler(frame=frame).style(
                        properties=FDL_Frame_Properties(
                            face_color=self.frame.face_color,
                            face_alpha=self.frame.face_alpha,
                            border_color=self.frame.border_color,
                            border_alpha=self.frame.border_alpha,
                            border_width=self.frame.border_width,
                            border_style=self.frame.border_style,
                            border_radius=self.frame.border_radius,
                        ),
                        gid="BarFramedDataLabel_Frame",
                    )

                    # Draw the label text inside the frame.
                    FramedDataLabeler(
                        ax=self.ax,
                        fig=self.fig,
                        dimension=FDL_FrameDimension(width=frame_x, height=frame_y),
                        anchor=FDL_FrameAnchor(
                            x_min=anchor.x + offset_x,
                            y_min=anchor.y + offset_y,
                            dimension=FDL_FrameDimension(width=frame_x, height=frame_y),
                        ),
                        formatter=self.formatter,
                        label=FDL_Label_Properties(
                            font=self.label.font,
                            size=self.label.size,
                            color=self.label.color,
                        ),
                        align=FDL_Label_AlignProperties(
                            h_align=self.label_align.h_align,
                            v_align=self.label_align.v_align,
                        ),
                        pad=FDL_Label_PadProperties(
                            left=pad_left_data,
                            right=pad_right_data,
                            top=pad_top_data,
                            bottom=pad_bottom_data,
                        ),
                        gid="BarFramedDataLabel_Label",
                    ).draw(label=patch_value)


class FDL_Bar_Drawer:
    """Configure and draw framed data labels for bar charts."""

    def __init__(self, ax: Axes, fig: Figure, horizontal: bool):
        """
        Args:
            ax (Axes): Target axes that already contains bar artists.
            fig (Figure): Figure used for measurement and conversion.
            horizontal (bool): Whether the bar chart is horizontal.
        """
        self.ax = ax
        self.fig = fig
        self.horizontal = horizontal

        # Label properties
        self._label_font: FontProperties | None = None
        self._label_size: int = 10
        self._label_color: str = "#000000"

        # Label align properties
        self._label_h_align: FDL_Label_HAlign = "center"
        self._label_v_align: FDL_Label_VAlign = "center"

        # Label pad properties (points)
        self._pad_left: float | None = None
        self._pad_right: float | None = None
        self._pad_top: float | None = None
        self._pad_bottom: float | None = None

        # Frame properties (units are points where applicable)
        self._frame_face_color: str | None = "#FFFFFF"
        self._frame_face_alpha: float = 1.0
        self._frame_border_color: str = "#000000"
        self._frame_border_alpha: float = 1.0
        self._frame_border_style: str = "solid"
        self._frame_border_width: float = 1.0
        self._frame_border_radius: float = 0.0
        self._frame_custom_width: float | None = None
        self._frame_custom_height: float | None = None

        # Frame align properties (offsets are points)
        self._frame_h_align: FDL_HBar_HAlign | FDL_VBar_HAlign = "center"
        self._frame_v_align: FDL_HBar_VAlign | FDL_VBar_VAlign = "center"
        self._frame_x_offset: float = 0.0
        self._frame_y_offset: float = 0.0

        # Format properties
        self._format_type: NumberFormat = "number"
        self._decimals: int = 0
        self._separator: bool = False
        self._currency: str | None = None
        self._scale: ScaleType = "full"

    def label(
        self,
        font: FontProperties | None = None,
        size: int = 10,
        color: str = "#000000",
    ) -> "FDL_Bar_Drawer":
        """Set label font properties.

        Args:
            font (FontProperties | None): Font style. If None, Matplotlib
                defaults are used.
            size (int | None): Font size. If None, Matplotlib defaults
                are used.
            color (str | None): Font color. If None, Matplotlib defaults
                are used.

        Returns:
            FDL_Bar_Drawer: The current instance for method chaining.
        """
        self._label_font = font
        self._label_size = size
        self._label_color = color
        return self

    def label_align(
        self,
        h_align: FDL_Label_HAlign = "center",
        v_align: FDL_Label_VAlign = "center",
    ) -> "FDL_Bar_Drawer":
        """Set text alignment inside the frame.

        Args:
            h_align (FDL_Label_HAlign): Horizontal alignment inside the frame.
                Options: "left", "right", "center".
            v_align (FDL_Label_VAlign): Vertical alignment inside the frame.
                Options: "top", "bottom", "center".

        Returns:
            FDL_Bar_Drawer: The current instance for method chaining.
        """
        self._label_h_align = h_align
        self._label_v_align = v_align
        return self

    def label_pad(
        self,
        left: float | None = None,
        right: float | None = None,
        top: float | None = None,
        bottom: float | None = None,
    ) -> "FDL_Bar_Drawer":
        """Set padding between the frame and the label text.

        All padding values are interpreted as points and converted into data
        units at draw time.

        Args:
            left (float | None): Left padding.
            right (float | None): Right padding.
            top (float | None): Top padding.
            bottom (float | None): Bottom padding.

        Returns:
            FDL_Bar_Drawer: The current instance for method chaining.
        """
        self._pad_left = left
        self._pad_right = right
        self._pad_top = top
        self._pad_bottom = bottom
        return self

    def frame(
        self,
        face_color: str = "#FFFFFF",
        face_alpha: float = 1.0,
        border_color: str = "#000000",
        border_alpha: float = 1.0,
        border_style: str = "solid",
        border_width: float = 1.0,
        border_radius: float = 0.0,
        custom_width: float | None = None,
        custom_height: float | None = None,
    ) -> "FDL_Bar_Drawer":
        """Set framed label background properties.

        Args:
            face_color (str): Fill color for the frame.
            face_alpha (float): Fill alpha in [0.0, 1.0].
            border_color (str): Border color for the frame.
            border_alpha (float): Border alpha in [0.0, 1.0].
            border_style (str): Border linestyle string (e.g. "-", "--", ":").
            border_width (float): Border width.
            border_radius (float): Corner radius.
            custom_width (float | None): Optional override for auto width.
            custom_height (float | None): Optional override for auto height.

        Returns:
            FDL_Bar_Drawer: The current instance for method chaining.
        """
        self._frame_face_color = face_color
        self._frame_face_alpha = face_alpha
        self._frame_border_color = border_color
        self._frame_border_alpha = border_alpha
        self._frame_border_style = border_style
        self._frame_border_width = border_width
        self._frame_border_radius = border_radius
        self._frame_custom_width = custom_width
        self._frame_custom_height = custom_height
        return self

    def frame_align(
        self,
        h_align: FDL_HBar_HAlign | FDL_VBar_HAlign = "center",
        v_align: FDL_HBar_VAlign | FDL_VBar_VAlign = "center",
        x_offset: float = 0.0,
        y_offset: float = 0.0,
    ) -> "FDL_Bar_Drawer":
        """Set how the frame is anchored relative to each bar.

        Args:
            h_align (FDL_HBar_HAlign | FDL_VBar_HAlign): Frame horizontal anchor
                selection. Options: "left", "right", "center", "outside".
            v_align (FDL_HBar_VAlign | FDL_VBar_VAlign): Frame vertical anchor
                selection. Options: "top", "bottom", "center", "outside".
            x_offset (float): Offset applied from anchor x coordinate.
            y_offset (float): Offset applied from anchor y coordinate.

        Returns:
            FDL_Bar_Drawer: The current instance for method chaining.
        """
        self._frame_h_align = h_align
        self._frame_v_align = v_align
        self._frame_x_offset = x_offset
        self._frame_y_offset = y_offset
        return self

    def format(
        self,
        format_type: NumberFormat = "number",
        decimals: int = 0,
        separator: bool = False,
        currency: str | None = None,
        scale: ScaleType = "full",
    ) -> "FDL_Bar_Drawer":
        """Configure numeric formatting for bar labels.

        Args:
            format_type (NumberFormat): Numeric formatting mode.
                Options: "number", "percent".
            decimals (int): Number of decimal places to display.
            separator (bool): Whether to use thousands separators.
            currency (str | None): Optional currency symbol/code.
            scale (ScaleType): Scaling mode for large numbers.
                Options: "k", "m", "b", "t", "full", "auto".

        Returns:
            FDL_Bar_Drawer: The current instance for method chaining.
        """
        self._format_type = format_type
        self._decimals = decimals
        self._separator = separator
        self._currency = currency
        self._scale = scale
        return self

    def draw(self, hide_smallest: int = 0, clear: bool = True) -> None:
        """Draw framed bar value labels onto the Axes.

        Args:
            hide_smallest (int): Number of smallest bars (by absolute value)
                to omit labels for. If 0, no bars are omitted.
            clear (bool): If True, remove existing labels previously drawn by
                this drawer (identified by gid "BarFramedDataLabel_Label"
                and "BarFramedDataLabel_Frame").

        Notes:
            This method mutates the Axes by removing and adding artists. It
            does not return self (not chainable).
        """
        helper = BarStyleHelper(ax=self.ax, horizontal=self.horizontal)
        patch_yielder = BarPatchYielder(ax=self.ax, horizontal=self.horizontal)

        if clear:
            # Remove prior framed labels created by this module.
            for label in self.ax.texts[:]:
                if label.get_gid() == "BarFramedDataLabel_Label":
                    label.remove()

            for patch in self.ax.patches[:]:
                if (
                    isinstance(patch, PathPatch)
                    and patch.get_gid() == "BarFramedDataLabel_Frame"
                ):
                    patch.remove()

        patches = list(patch_yielder.standard())

        # Determine the absolute-value threshold implied by hide_smallest.
        sorted_values: list[float] = []
        for patch in patches:
            value = helper.get_patch_value(patch)
            abs_value = abs(value)
            sorted_values.append(abs_value)
        sorted_values.sort()

        n_smallest = min(hide_smallest, len(patches))
        if n_smallest >= len(patches):
            threshold = float("inf")
        elif n_smallest == 0:
            threshold = 0
        else:
            threshold = sorted_values[n_smallest - 1]

        formatter = NumberFormatter(
            properties=NumberProperties(
                format_type=self._format_type,
                decimals=self._decimals,
                separator=self._separator,
                currency=self._currency,
                scale=self._scale,
            )
        )

        FDL_Bar(
            ax=self.ax,
            fig=self.fig,
            horizontal=self.horizontal,
            patches=patch_yielder,
            helper=helper,
            threshold=threshold,
            formatter=formatter,
            label=FDL_Bar_LabelProperties(
                font=self._label_font,
                size=self._label_size,
                color=self._label_color,
            ),
            label_align=FDL_Bar_Label_AlignProperties(
                h_align=self._label_h_align,
                v_align=self._label_v_align,
            ),
            label_pad=FDL_Bar_Label_PadProperties(
                left=self._pad_left,
                right=self._pad_right,
                top=self._pad_top,
                bottom=self._pad_bottom,
            ),
            frame=FDL_Bar_FrameProperties(
                face_color=self._frame_face_color,
                face_alpha=self._frame_face_alpha,
                border_color=self._frame_border_color,
                border_alpha=self._frame_border_alpha,
                border_style=self._frame_border_style,
                border_width=self._frame_border_width,
                border_radius=self._frame_border_radius,
                custom_width=self._frame_custom_width,
                custom_height=self._frame_custom_height,
            ),
            frame_align=FDL_Bar_Frame_AlignProperties(
                h_align=self._frame_h_align,
                v_align=self._frame_v_align,
                x_offset=self._frame_x_offset,
                y_offset=self._frame_y_offset,
            ),
        ).draw(default_pad=5.0)
