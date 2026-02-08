"""Draw framed numeric data labels and resolve their anchor positions.

Some charts benefit from placing data labels inside a visible frame
(background box). In those cases, label placement needs to be resolved
relative to the frame bounds with padding and alignment rules that are
shared across chart types. This module provides:
- Dataclasses describing label styling, alignment, and padding.
- An anchor resolver that computes the (x, y) position inside a frame.
- A FramedDataLabeler that draws a formatted numeric annotation.
"""

from dataclasses import dataclass
from typing import Literal

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties

from matchart.style.utils.num_formatter import NumberFormatter

from .frame_builder import FDL_FrameAnchor, FDL_FrameDimension

type FDL_Label_HAlign = Literal["left", "center", "right"]
type FDL_Label_VAlign = Literal["top", "center", "bottom", "center_baseline"]


@dataclass(frozen=True)
class FDL_Label_Properties:
    """Store text styling properties for framed data labels.

    Attributes:
        font (FontProperties | None): Optional font configuration.
        size (int): Font size in points.
        color (str): Text color.
    """

    font: FontProperties | None
    size: int
    color: str


@dataclass(frozen=True)
class FDL_Label_AlignProperties:
    """Store alignment selection for labels inside a frame.

    Attributes:
        h_align (FDL_Label_HAlign): Horizontal alignment.
        v_align (FDL_Label_VAlign): Vertical alignment.
    """

    h_align: FDL_Label_HAlign
    v_align: FDL_Label_VAlign


@dataclass(frozen=True)
class FDL_Label_PadProperties:
    """Store padding for labels within a frame.

    Padding values are applied to the frame bounds when resolving the label
    anchor position.

    Attributes:
        left (float): Left padding.
        right (float): Right padding.
        top (float): Top padding.
        bottom (float): Bottom padding.
    """

    left: float
    right: float
    top: float
    bottom: float


class FDL_Label_AnchorResolver:
    """Resolve the label anchor position within a framed label box."""

    def __init__(
        self,
        ax: Axes,
        dimension: FDL_FrameDimension,
        anchor: FDL_FrameAnchor,
        align: FDL_Label_AlignProperties,
        pad: FDL_Label_PadProperties,
    ):
        """
        Args:
            ax (Axes): Target axes (currently unused).
            dimension (FDL_FrameDimension): Frame size (currently unused).
            anchor (FDL_FrameAnchor): Frame bounds in data coordinates.
            align (FDL_Label_AlignProperties): Desired label alignment.
            pad (FDL_Label_PadProperties): Padding applied inside the frame.
        """
        self.ax = ax
        self.dimension = dimension
        self.anchor = anchor
        self.align = align
        self.pad = pad

    def get_x_ha(self, h_align: FDL_Label_HAlign) -> tuple[float, FDL_Label_HAlign]:
        """Compute x position and horizontal alignment for the label.

        Args:
            h_align (FDL_Label_HAlign): Desired horizontal alignment.

        Returns:
            tuple[float, FDL_Label_HAlign]: (x, ha) suitable for annotate().
        """
        x_min = self.anchor.x_min + self.pad.left
        x_max = self.anchor.x_max - self.pad.right

        options: dict[FDL_Label_HAlign, tuple[float, FDL_Label_HAlign]] = {
            "left": (x_min, "left"),
            "right": (x_max, "right"),
            "center": ((x_min + x_max) / 2.0, "center"),
        }
        return options[h_align]

    def get_y_va(self, v_align: FDL_Label_VAlign) -> tuple[float, FDL_Label_VAlign]:
        """Compute y position and vertical alignment for the label.

        Args:
            v_align (FDL_Label_VAlign): Desired vertical alignment.

        Returns:
            tuple[float, FDL_Label_VAlign]: (y, va) suitable for annotate().
        """
        y_min = self.anchor.y_min + self.pad.bottom
        y_max = self.anchor.y_max - self.pad.top

        options: dict[FDL_Label_VAlign, tuple[float, FDL_Label_VAlign]] = {
            "bottom": (y_min, "bottom"),
            "top": (y_max, "top"),
            "center": ((y_min + y_max) / 2.0, "center_baseline"),
        }
        return options[v_align]

    def resolve(self) -> tuple[float, float, FDL_Label_HAlign, FDL_Label_VAlign]:
        """Resolve the final label anchor and alignment.

        Returns:
            tuple[float, float, FDL_Label_HAlign, FDL_Label_VAlign]:
            (x, y, ha, va) suitable for annotate().
        """
        x, h_align = self.get_x_ha(self.align.h_align)
        y, v_align = self.get_y_va(self.align.v_align)
        return x, y, h_align, v_align


class FramedDataLabeler:
    """Add a formatted numeric label annotation inside a frame."""

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
        """
        Args:
            ax (Axes): Target axes to annotate (no figure creation).
            fig (Figure): Figure context (currently unused).
            dimension (FDL_FrameDimension): Frame size (currently unused by
                this implementation).
            anchor (FDL_FrameAnchor): Frame bounds in data coordinates.
            formatter (NumberFormatter): Formatter used to convert numeric
                values into display strings.
            label (FDL_Label_Properties): Text styling properties.
            align (FDL_Label_AlignProperties): Alignment selection.
            pad (FDL_Label_PadProperties): Padding within the frame.
            gid (str | None): Optional Matplotlib artist group id.
        """
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
        """Draw a framed data label annotation.

        Args:
            label (float): Numeric value to format and annotate.

        Returns:
            None: This method adds an annotation artist to the axes.
        """
        x, y, h_align, v_align = FDL_Label_AnchorResolver(
            ax=self.ax,
            anchor=self.anchor,
            dimension=self.dimension,
            pad=self.pad,
            align=self.align,
        ).resolve()

        self.ax.annotate(  # type:ignore
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
