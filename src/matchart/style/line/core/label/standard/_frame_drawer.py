from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.patches import PathPatch

from matchart.style.utils.num_formatter import (
    ScaleType,
    NumberFormat,
    NumberProperties,
    NumberFormatter,
)
from matchart.style.utils.input_converter import PointDataConverter
from matchart.style.utils.data_label.frame_autosizer import FrameAutoSizer
from matchart.style.utils.data_label.frame_builder import (
    FDL_FrameDimension,
    FDL_FrameAnchor,
    FDL_FrameCornerRadii,
    FDL_FrameBuilder,
)
from matchart.style.utils.data_label.frame_labeler import (
    FDL_Label_HAlign,
    FDL_Label_VAlign,
    FDL_Label_Properties,
    FDL_Label_AlignProperties,
    FDL_Label_PadProperties,
    FramedDataLabeler,
)
from matchart.style.utils.data_label.frame_styler import (
    FDL_Frame_Properties,
    FDLFrameStyler,
)
from ..._utils import LineGenerator
from ._frame_anchor import FDL_Line_Anchor


@dataclass(frozen=True)
class FDL_Line_LabelProperties:
    font: FontProperties | None
    size: int
    color: str


@dataclass(frozen=True)
class FDL_Line_Label_AlignProperties:
    h_align: FDL_Label_HAlign
    v_align: FDL_Label_VAlign


@dataclass(frozen=True)
class FDL_Line_Label_PadProperties:
    left: float | None
    right: float | None
    top: float | None
    bottom: float | None


@dataclass(frozen=True)
class FDL_Line_FrameProperties:
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
class FDL_Line_Frame_AlignProperties:
    x_offset: float
    y_offset: float


class FDL_Line:
    def __init__(
        self,
        ax: Axes,
        fig: Figure,
        lines: LineGenerator,
        formatter: NumberFormatter,
        label: FDL_Line_LabelProperties,
        label_align: FDL_Line_Label_AlignProperties,
        label_pad: FDL_Line_Label_PadProperties,
        frame: FDL_Line_FrameProperties,
        frame_align: FDL_Line_Frame_AlignProperties,
        select: list[str] | None,
    ):
        self.ax = ax
        self.fig = fig
        self.lines = lines.standard()
        self.formatter = formatter
        self.label = label
        self.label_align = label_align
        self.label_pad = label_pad
        self.frame = frame
        self.frame_align = frame_align
        self.select = select

    def draw(self, default_pad: float) -> None:
        for line in self.lines:
            line_label = line.get_label()
            if self.select is not None:
                if line_label not in self.select:
                    continue
            anchor = FDL_Line_Anchor(line=line).anchor()
            for point in anchor:
                x, y = point
                frame = FrameAutoSizer(
                    fig=self.fig,
                    pad=default_pad,
                    font=self.label.font,
                    size=self.label.size,
                    formatter=self.formatter,
                ).compute_dimension(
                    label=y,
                    custom_width=self.frame.custom_width,
                    custom_height=self.frame.custom_height,
                )

                width = frame.width
                height = frame.height

                data_coords = PointDataConverter(ax=self.ax, fig=self.fig)
                frame_x, frame_y = (
                    data_coords.convert("x", width),
                    data_coords.convert("y", height),
                )
                offset_x, offset_y = (
                    data_coords.convert("x", self.frame_align.x_offset),
                    data_coords.convert("y", self.frame_align.y_offset),
                )
                border_x = data_coords.convert("x", self.frame.border_width)
                radius_x, radius_y = (
                    data_coords.convert("x", self.frame.border_radius),
                    data_coords.convert("y", self.frame.border_radius),
                )

                pad_left_data = (
                    data_coords.convert(axis="x", points=self.label_pad.left)
                    if self.label_pad.left is not None
                    else data_coords.convert(axis="x", points=default_pad)
                )
                pad_right_data = (
                    data_coords.convert(axis="x", points=self.label_pad.right)
                    if self.label_pad.right is not None
                    else data_coords.convert(axis="x", points=default_pad)
                )
                pad_top_data = (
                    data_coords.convert(axis="y", points=self.label_pad.top)
                    if self.label_pad.top is not None
                    else data_coords.convert(axis="y", points=default_pad)
                )
                pad_bottom_data = (
                    data_coords.convert(axis="y", points=self.label_pad.bottom)
                    if self.label_pad.bottom is not None
                    else data_coords.convert(axis="y", points=default_pad)
                )

                x_anchor = x - (frame_x / 2) - (border_x / 2)
                frame = FDL_FrameBuilder(
                    ax=self.ax,
                    anchor=FDL_FrameAnchor(
                        x_min=x_anchor + offset_x,
                        y_min=y + offset_y,
                        dimension=FDL_FrameDimension(width=frame_x, height=frame_y),
                    ),
                    radii=FDL_FrameCornerRadii(rx=radius_x, ry=radius_y),
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
                    gid="LineFramedDataLabel_Frame",
                )

                FramedDataLabeler(
                    ax=self.ax,
                    fig=self.fig,
                    dimension=FDL_FrameDimension(width=frame_x, height=frame_y),
                    anchor=FDL_FrameAnchor(
                        x_min=x_anchor + offset_x,
                        y_min=y + offset_y,
                        dimension=FDL_FrameDimension(
                            width=frame_x,
                            height=frame_y,
                        ),
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
                    gid="LineFramedDataLabel_Label",
                ).draw(label=y)


class FDL_Line_Drawer:
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
        self._frame_y_offset: float = 5.0

        # Format properties
        self._type: NumberFormat = "number"
        self._decimals: int = 0
        self._separator: bool = False
        self._currency: str | None = None
        self._scale: ScaleType = "full"

    def label(
        self,
        font: FontProperties | None = None,
        size: int = 10,
        color: str = "#000000",
    ) -> "FDL_Line_Drawer":
        """
        Set the data label properties.

        Parameters
        ----------
        font : FontProperties | None. Default is None.
            The font for the data label.
        size : int. Default is 10.
            The font size for the data label.
        color : str. Default is "#000000".
            The font color for the data label.

        Returns
        -------
        FDL_Line_Drawer
            The current instance for method chaining.
        """

        self._label_font = font
        self._label_size = size
        self._label_color = color
        return self

    def label_align(
        self,
        h_align: FDL_Label_HAlign = "center",
        v_align: FDL_Label_VAlign = "center",
    ) -> "FDL_Line_Drawer":
        """
        Set the data label alignment properties.

        Parameters
        ----------
        h_align : {"left", "right", "center"}. Default is "center".
            The horizontal alignment for the data label.
        v_align : {"top", "bottom", "center"}. Default is "center".
            The vertical alignment for the data label.

        Returns
        -------
        FDL_Line_Drawer
            The current instance for method chaining.
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
    ) -> "FDL_Line_Drawer":
        """
        Set the data label padding properties.

        Parameters
        ----------
        left : float | None. Default is None.
            The left padding for the data label in points. If None, default padding will be used.
        right : float | None. Default is None.
            The right padding for the data label in points. If None, default padding will be used.
        top : float | None. Default is None.
            The top padding for the data label in points. If None, default padding will be used.
        bottom : float | None. Default is None.
            The bottom padding for the data label in points. If None, default padding will be used

        Returns
        -------
        FDL_Line_Drawer
            The current instance for method chaining.
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
    ) -> "FDL_Line_Drawer":
        """
        Set the data label frame properties.

        Parameters
        ----------
        face_color : str. Default is "#FFFFFF".
            The face color for the data label frame.
        face_alpha : float. Default is 1.0.
            The face alpha for the data label frame.
        border_color : str. Default is "#000000".
            The border color for the data label frame.
        border_alpha : float. Default is 1.0.
            The border alpha for the data label frame.
        border_style : str. Default is "solid".
            The border style for the data label frame.
        border_width : float. Default is 1.0.
            The border width for the data label frame.
        border_radius : float. Default is 0.0.
            The border radius for the data label frame.
        custom_width : float | None. Default is None.
            The custom width for the data label frame in data units. If None, auto size will be used.
        custom_height : float | None. Default is None.
            The custom height for the data label frame in data units. If None, auto size will be used.

        Returns
        -------
        FDL_Line_Drawer
            The current instance for method chaining.
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
        x_offset: float = 0.0,
        y_offset: float = 0.0,
    ) -> "FDL_Line_Drawer":
        """
        Set the data label frame alignment properties.

        Parameters
        ----------
        x_offset : float. Default is 0.0.
            The horizontal offset for the data label frame.
        y_offset : float. Default is 0.0.
            The vertical offset for the data label frame.

        Returns
        -------
        FDL_Line_Drawer
            The current instance for method chaining.
        """

        self._frame_x_offset = x_offset
        self._frame_y_offset = y_offset
        return self

    def format(
        self,
        type: NumberFormat = "number",
        decimals: int = 0,
        separator: bool = False,
        currency: str | None = None,
        scale: ScaleType = "full",
    ) -> "FDL_Line_Drawer":
        """
        Set the data label number format properties.

        Parameters
        ----------
        type : {"number", "percent"}. Default is "number".
            The number format type for the data label.
        decimals : int. Default is 0.
            The number of decimal places for the data label.
        separator : bool. Default is False.
            Whether to use a thousands separator for the data label.
        currency : str | None. Default is None.
            The currency symbol for the data label. Only used if type is "currency".
        scale : {"k", "m", "b", "t", "full", "auto"}. Default is "full".
            The scale for the data label.

        Returns
        -------
        FDL_Line_Drawer
            The current instance for method chaining.
        """

        self._type = type
        self._decimals = decimals
        self._separator = separator
        self._currency = currency
        self._scale = scale
        return self

    def draw(self, select: list[str] | None = None, clear: bool = True) -> None:
        """
        Draw the framed data labels on the lines. Before calling draw(), ensure that all desired
        styling methods have been called to set up the data label appearance.

        Parameters
        ----------
        select : list[str] | None. Default is None.
            A list of line labels to draw data labels for. If None, data labels will be drawn.
        clear : bool. Default is True.
            Clear existing framed data labels before drawing new ones.
        """

        line_generator = LineGenerator(ax=self.ax)

        if clear:
            for label in self.ax.texts[:]:
                if label.get_gid() == "LineFramedDataLabel_Label":
                    label.remove()

            for patch in self.ax.patches[:]:
                if (
                    isinstance(patch, PathPatch)
                    and patch.get_gid() == "LineFramedDataLabel_Frame"
                ):
                    patch.remove()

        formatter = NumberFormatter(
            properties=NumberProperties(
                type=self._type,
                decimals=self._decimals,
                separator=self._separator,
                currency=self._currency,
                scale=self._scale,
            )
        )

        FDL_Line(
            ax=self.ax,
            fig=self.fig,
            lines=line_generator,
            formatter=formatter,
            label=FDL_Line_LabelProperties(
                font=self._label_font,
                size=self._label_size,
                color=self._label_color,
            ),
            label_align=FDL_Line_Label_AlignProperties(
                h_align=self._label_h_align,
                v_align=self._label_v_align,
            ),
            label_pad=FDL_Line_Label_PadProperties(
                left=self._pad_left,
                right=self._pad_right,
                top=self._pad_top,
                bottom=self._pad_bottom,
            ),
            frame=FDL_Line_FrameProperties(
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
            frame_align=FDL_Line_Frame_AlignProperties(
                x_offset=self._frame_x_offset,
                y_offset=self._frame_y_offset,
            ),
            select=select,
        ).draw(default_pad=5.0)
