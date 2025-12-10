from typing import Literal
from dataclasses import dataclass
from matplotlib.axes import Axes

from ._utils import CDL_Bar_Bounds


type CBDL_HBar_VAlign = Literal["top", "bottom", "center"]
type CBDL_VBar_HAlign = Literal["left", "right", "center"]


@dataclass(frozen=True)
class CBDL_Bar_Anchor:
    x: float
    y: float
    h_align: CBDL_VBar_HAlign
    v_align: CBDL_HBar_VAlign


class CBDL_HBar_Anchor:

    def __init__(self, ax: Axes, bounds: CDL_Bar_Bounds):
        self.ax = ax
        self.bounds = bounds

    def get_x(self) -> float:
        """Get the anchor point X max limit coordinate."""

        xlim_max = self.ax.get_xlim()[1]
        return xlim_max

    def get_y(self, v_align: CBDL_HBar_VAlign) -> tuple[float, CBDL_HBar_VAlign]:
        """Get the anchor point Y coordinate and vertical alignment."""

        options: dict[CBDL_HBar_VAlign, tuple[float, CBDL_HBar_VAlign]] = {
            "top": (self.bounds.max, "top"),
            "bottom": (self.bounds.min, "bottom"),
            "center": (self.bounds.center, "center"),
        }
        return options[v_align]

    def anchor(self, v_align: CBDL_HBar_VAlign) -> CBDL_Bar_Anchor:

        xlim_max = self.get_x()
        y, va = self.get_y(v_align)
        return CBDL_Bar_Anchor(x=xlim_max, y=y, h_align="right", v_align=va)


class CBDL_VBar_Anchor:

    def __init__(self, ax: Axes, bounds: CDL_Bar_Bounds):
        self.ax = ax
        self.bounds = bounds

    def get_x(self, h_align: CBDL_VBar_HAlign) -> tuple[float, CBDL_VBar_HAlign]:
        """Get the anchor point X coordinate and horizontal alignment."""

        options: dict[CBDL_VBar_HAlign, tuple[float, CBDL_VBar_HAlign]] = {
            "left": (self.bounds.min, "left"),
            "right": (self.bounds.max, "right"),
            "center": (self.bounds.center, "center"),
        }
        return options[h_align]

    def get_y(self) -> float:
        """Get the anchor point Y max limit coordinate."""

        ylim_max = self.ax.get_ylim()[1]
        return ylim_max

    def anchor(self, h_align: CBDL_VBar_HAlign) -> CBDL_Bar_Anchor:

        x, ha = self.get_x(h_align)
        ylim_max = self.get_y()
        return CBDL_Bar_Anchor(x=x, y=ylim_max, h_align=ha, v_align="top")
