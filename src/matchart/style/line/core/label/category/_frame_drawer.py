from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.patches import PathPatch

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

from ..._utils import LineStyleHelper
from ._frame_anchor import CFDL_Line_Anchor, CFDL_Line_FrameDimension
from ._utils import CDL_Line_Totals


@dataclass(frozen=True)
class CFDL_Line_LabelProperties:
    font: FontProperties | None
    size: int
    color: str


@dataclass(frozen=True)
class CFDL_Line_Label_AlignProperties:
    h_align: FDL_Label_HAlign
    v_align: FDL_Label_VAlign


@dataclass(frozen=True)
class CFDL_Line_Label_PadProperties:
    left: float | None
    right: float | None
    top: float | None
    bottom: float | None


@dataclass(frozen=True)
class CFDL_Line_FrameProperties:
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
class CFDL_Line_Frame_AlignProperties:
    x_offset: float
    y_offset: float


class CFDL_Line:
    def __init__(
        self,
        ax: Axes,
        fig: Figure,
        helper: LineStyleHelper,
        formatter: NumberFormatter,
        label: CFDL_Line_LabelProperties,
        label_align: CFDL_Line_Label_AlignProperties,
        label_pad: CFDL_Line_Label_PadProperties,
        frame: CFDL_Line_FrameProperties,
        frame_align: CFDL_Line_Frame_AlignProperties,
        custom_label: dict[str, float] | None,
    ):
        self.ax = ax
        self.fig = fig
        self.helper = helper
        self.formatter = formatter
        self.label = label
        self.label_align = label_align
        self.label_pad = label_pad
        self.frame = frame
        self.frame_align = frame_align
        self.custom_label = custom_label

    def draw(self, default_pad: float) -> None:
        tick_labels = self.helper.get_tick_labels()

        for tick_label in tick_labels:
            if self.custom_label is None:
                label = CDL_Line_Totals.compute_total(
                    ax=self.ax,
                    tick_label=tick_label,
                ).total
            else:
                label = self.custom_label[tick_label]

            frame = FrameAutoSizer(
                fig=self.fig,
                pad=default_pad,
                font=self.label.font,
                size=self.label.size,
                formatter=self.formatter,
            ).compute_dimension(
                label=label,
                custom_width=self.frame.custom_width,
                custom_height=self.frame.custom_height,
            )

            width = frame.width
            height = frame.height

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

            dimension = CFDL_Line_FrameDimension(
                width=frame_x,
                height=frame_y,
                border_width_x=border_x,
                border_width_y=border_y,
            )

            anchor = CFDL_Line_Anchor(
                ax=self.ax,
                dimension=dimension,
                tick_label=tick_label,
            )

            frame = FDL_FrameBuilder(
                ax=self.ax,
                anchor=FDL_FrameAnchor(
                    x_min=anchor.x + offset_x,
                    y_min=anchor.y + offset_y,
                    dimension=FDL_FrameDimension(
                        width=frame_x,
                        height=frame_y,
                    ),
                ),
                radii=FDL_FrameCornerRadii(
                    rx=radius_x,
                    ry=radius_y,
                ),
            ).build()

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
                gid="LineCategoryFramedDataLabel_Frame",
            )

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
                gid="LineCategoryFramedDataLabel_Label",
            ).draw(label=label)


class CFDL_Line_Drawer:
    def __init__(self, ax: Axes, fig: Figure):
        self.ax = ax
        self.fig = fig

        # Label properties
        self._label_font: FontProperties | None = None
        self._label_size: int = 10
        self._label_color: str = "#000000"

        # Label align properties
        self._label_h_align: FDL_Label_HAlign = "center"
        self._label_v_align: FDL_Label_VAlign = "center"

        # Label pad properties
        self._pad_left: float | None = None
        self._pad_right: float | None = None
        self._pad_top: float | None = None
        self._pad_bottom: float | None = None

        # Frame properties
        self._frame_face_color: str | None = "#FFFFFF"
        self._frame_face_alpha: float = 1.0
        self._frame_border_color: str = "#000000"
        self._frame_border_alpha: float = 1.0
        self._frame_border_style: str = "solid"
        self._frame_border_width: float = 1.0
        self._frame_border_radius: float = 0.0
        self._frame_custom_width: float | None = None
        self._frame_custom_height: float | None = None

        # Frame align properties
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
    ) -> "CFDL_Line_Drawer":
        self._label_font = font
        self._label_size = size
        self._label_color = color
        return self

    def label_align(
        self,
        h_align: FDL_Label_HAlign = "center",
        v_align: FDL_Label_VAlign = "center",
    ) -> "CFDL_Line_Drawer":
        self._label_h_align = h_align
        self._label_v_align = v_align
        return self

    def label_pad(
        self,
        left: float | None = None,
        right: float | None = None,
        top: float | None = None,
        bottom: float | None = None,
    ) -> "CFDL_Line_Drawer":
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
    ) -> "CFDL_Line_Drawer":
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
        x_offset: float = 0.0,
        y_offset: float = 0.0,
    ) -> "CFDL_Line_Drawer":
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
    ) -> "CFDL_Line_Drawer":
        self._format_type = format_type
        self._decimals = decimals
        self._separator = separator
        self._currency = currency
        self._scale = scale
        return self

    def draw(
        self,
        custom_label: dict[str, float] | None = None,
        clear: bool = True,
    ) -> None:
        helper = LineStyleHelper(ax=self.ax)
        if clear:
            for label in self.ax.texts[:]:
                if label.get_gid() == "LineCategoryFramedDataLabel_Label":
                    label.remove()

            for patch in self.ax.patches[:]:
                if (
                    isinstance(patch, PathPatch)
                    and patch.get_gid() == "LineCategoryFramedDataLabel_Frame"
                ):
                    patch.remove()

        formatter = NumberFormatter(
            properties=NumberProperties(
                format_type=self._format_type,
                decimals=self._decimals,
                separator=self._separator,
                currency=self._currency,
                scale=self._scale,
            )
        )

        CFDL_Line(
            ax=self.ax,
            fig=self.fig,
            helper=helper,
            formatter=formatter,
            label=CFDL_Line_LabelProperties(
                font=self._label_font,
                size=self._label_size,
                color=self._label_color,
            ),
            label_align=CFDL_Line_Label_AlignProperties(
                h_align=self._label_h_align,
                v_align=self._label_v_align,
            ),
            label_pad=CFDL_Line_Label_PadProperties(
                left=self._pad_left,
                right=self._pad_right,
                top=self._pad_top,
                bottom=self._pad_bottom,
            ),
            frame=CFDL_Line_FrameProperties(
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
            frame_align=CFDL_Line_Frame_AlignProperties(
                x_offset=self._frame_x_offset,
                y_offset=self._frame_y_offset,
            ),
            custom_label=custom_label,
        ).draw(default_pad=5.0)
