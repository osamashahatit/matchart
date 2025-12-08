from typing import Literal
from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties

from ..num_formatter import NumberFormatter
from .frame_builder import FDL_FrameDimension, FDL_FrameAnchor

type FDL_Label_HAlign = Literal["left", "center", "right"]
type FDL_Label_VAlign = Literal["top", "center", "bottom", "center_baseline"]


@dataclass(frozen=True)
class FDL_Label_Properties:
    font: FontProperties | None
    size: int
    color: str


@dataclass(frozen=True)
class FDL_Label_AlignProperties:
    h_align: FDL_Label_HAlign
    v_align: FDL_Label_VAlign


@dataclass(frozen=True)
class FDL_Label_PadProperties:
    left: float
    right: float
    top: float
    bottom: float


class FDL_Label_AnchorResolver:
    """Resolves the anchor position for framed data labels."""

    def __init__(
        self,
        ax: Axes,
        dimension: FDL_FrameDimension,
        anchor: FDL_FrameAnchor,
        align: FDL_Label_AlignProperties,
        pad: FDL_Label_PadProperties,
    ):
        self.ax = ax
        self.dimension = dimension
        self.anchor = anchor
        self.align = align
        self.pad = pad

    def get_x_ha(self, h_align: FDL_Label_HAlign) -> tuple[float, FDL_Label_HAlign]:

        x_min = self.anchor.x_min + self.pad.left
        x_max = self.anchor.x_max - self.pad.right

        options: dict[FDL_Label_HAlign, tuple[float, FDL_Label_HAlign]] = {
            "left": (x_min, "left"),
            "right": (x_max, "right"),
            "center": ((x_min + x_max) / 2.0, "center"),
        }
        return options[h_align]

    def get_y_va(self, v_align: FDL_Label_VAlign) -> tuple[float, FDL_Label_VAlign]:

        y_min = self.anchor.y_min + self.pad.bottom
        y_max = self.anchor.y_max - self.pad.top

        options: dict[FDL_Label_VAlign, tuple[float, FDL_Label_VAlign]] = {
            "bottom": (y_min, "bottom"),
            "top": (y_max, "top"),
            "center": ((y_min + y_max) / 2.0, "center_baseline"),
        }
        return options[v_align]

    def resolve(self) -> tuple[float, float, FDL_Label_HAlign, FDL_Label_VAlign]:

        x, h_align = self.get_x_ha(self.align.h_align)
        y, v_align = self.get_y_va(self.align.v_align)
        return x, y, h_align, v_align


class FramedDataLabeler:
    """Adds chart framed data labels."""

    def __init__(
        self,
        ax: Axes,
        fig: Figure,
        dimension: FDL_FrameDimension,
        anchor: FDL_FrameAnchor,
        formatter: NumberFormatter,
        label: FDL_Label_Properties,
        align: FDL_Label_AlignProperties,
        pad: FDL_Label_PadProperties,
        gid: str | None = None,
    ):
        self.ax = ax
        self.fig = fig
        self.dimension = dimension
        self.anchor = anchor
        self.formatter = formatter
        self.label = label
        self.align = align
        self.pad = pad
        self.gid = gid

    def draw(self, label: float) -> None:

        x, y, h_align, v_align = FDL_Label_AnchorResolver(
            ax=self.ax,
            anchor=self.anchor,
            dimension=self.dimension,
            pad=self.pad,
            align=self.align,
        ).resolve()

        self.ax.annotate(
            text=self.formatter.format(label),
            xy=(x, y),
            fontproperties=self.label.font,
            fontsize=self.label.size,
            color=self.label.color,
            ha=h_align,
            va=v_align,
            xytext=(0.0, 0.0),
            xycoords="data",
            textcoords="offset points",
            gid=self.gid,
        )
