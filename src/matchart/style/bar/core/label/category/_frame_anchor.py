from typing import Literal
from dataclasses import dataclass
from matplotlib.axes import Axes

from ._utils import CDL_Bar_Bounds


type CFDL_HBar_VAlign = Literal["top", "bottom", "center"]
type CFDL_VBar_HAlign = Literal["left", "right", "center"]


@dataclass(frozen=True)
class CFDL_Bar_Dimension:
    width: float
    height: float
    border_width_x: float
    border_width_y: float

    @property
    def border_x(self) -> float:
        return self.border_width_x / 2

    @property
    def border_y(self) -> float:
        return self.border_width_y / 2


@dataclass(frozen=True)
class CFDL_Bar_Anchor:
    x: float
    y: float


class CFDL_HBar_Anchor:

    def __init__(
        self,
        ax: Axes,
        bounds: CDL_Bar_Bounds,
        dimension: CFDL_Bar_Dimension,
    ):
        self.ax = ax
        self.bounds = bounds
        self.dimension = dimension

    def get_x(self) -> float:
        """Get the anchor point X max limit coordinate."""

        xlim_max = (
            self.ax.get_xlim()[1] - self.dimension.width - self.dimension.border_x
        )
        return xlim_max

    def get_y(self, v_align: CFDL_HBar_VAlign) -> float:
        """Get the anchor point Y coordinate and vertical alignment."""

        options: dict[CFDL_HBar_VAlign, float] = {
            "top": self.bounds.max - self.dimension.height - self.dimension.border_y,
            "bottom": self.bounds.min + self.dimension.border_y,
            "center": self.bounds.center - (self.dimension.height / 2),
        }
        return options[v_align]

    def anchor(self, v_align: CFDL_HBar_VAlign) -> CFDL_Bar_Anchor:
        return CFDL_Bar_Anchor(x=self.get_x(), y=self.get_y(v_align))


class CFDL_VBar_Anchor:

    def __init__(
        self,
        ax: Axes,
        bounds: CDL_Bar_Bounds,
        dimension: CFDL_Bar_Dimension,
    ):
        self.ax = ax
        self.bounds = bounds
        self.dimension = dimension

    def get_x(self, h_align: CFDL_VBar_HAlign) -> float:
        """Get the anchor point X coordinate and horizontal alignment."""

        options: dict[CFDL_VBar_HAlign, float] = {
            "left": self.bounds.min + self.dimension.border_x,
            "right": self.bounds.max - self.dimension.width - self.dimension.border_x,
            "center": self.bounds.center - (self.dimension.width / 2),
        }
        return options[h_align]

    def get_y(self) -> float:
        """Get the anchor point Y max limit coordinate."""

        ylim_max = (
            self.ax.get_ylim()[1] - self.dimension.height - self.dimension.border_y
        )
        return ylim_max

    def anchor(self, h_align: CFDL_VBar_HAlign) -> CFDL_Bar_Anchor:
        return CFDL_Bar_Anchor(x=self.get_x(h_align), y=self.get_y())
