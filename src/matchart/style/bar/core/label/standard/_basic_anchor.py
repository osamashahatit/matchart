from typing import Literal
from dataclasses import dataclass

type BDL_HBar_HAlign = Literal["left", "right", "center", "outside"]
type BDL_HBar_VAlign = Literal["top", "bottom", "center"]
type BDL_VBar_HAlign = Literal["left", "right", "center"]
type BDL_VBar_VAlign = Literal["top", "bottom", "center", "outside"]


@dataclass(frozen=True)
class BDL_Bar_Bounds:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    @property
    def center_x(self) -> float:
        return (self.x_min + self.x_max) / 2

    @property
    def center_y(self) -> float:
        return (self.y_min + self.y_max) / 2


@dataclass(frozen=True)
class BDL_Bar_Anchor:
    x: float
    y: float
    h_align: BDL_HBar_HAlign | BDL_VBar_HAlign
    v_align: BDL_HBar_VAlign | BDL_VBar_VAlign


class BDL_HBar_Anchor:

    def __init__(self, bounds: BDL_Bar_Bounds):
        self.bounds = bounds

    def get_x(self, h_align: BDL_HBar_HAlign) -> tuple[float, BDL_HBar_HAlign]:
        """Get the anchor point X coordinate and horizontal alignment."""

        options: dict[BDL_HBar_HAlign, tuple[float, BDL_HBar_HAlign]] = {
            "left": (self.bounds.x_min, "left"),
            "right": (self.bounds.x_max, "right"),
            "center": (self.bounds.center_x, "center"),
            "outside": (self.bounds.x_max, "left"),
        }
        return options[h_align]

    def get_y(self, v_align: BDL_HBar_VAlign) -> tuple[float, BDL_HBar_VAlign]:
        """Get the anchor point Y coordinate and vertical alignment."""

        options: dict[BDL_HBar_VAlign, tuple[float, BDL_HBar_VAlign]] = {
            "top": (self.bounds.y_max, "top"),
            "bottom": (self.bounds.y_min, "bottom"),
            "center": (self.bounds.center_y, "center"),
        }
        return options[v_align]

    def anchor(
        self,
        h_align: BDL_HBar_HAlign,
        v_align: BDL_HBar_VAlign,
    ) -> BDL_Bar_Anchor:

        x, ha = self.get_x(h_align)
        y, va = self.get_y(v_align)
        return BDL_Bar_Anchor(x=x, y=y, h_align=ha, v_align=va)


class BDL_VBar_Anchor:

    def __init__(self, bounds: BDL_Bar_Bounds):
        self.bounds = bounds

    def get_x(self, h_align: BDL_VBar_HAlign) -> tuple[float, BDL_VBar_HAlign]:
        """Get the anchor point X coordinate and horizontal alignment."""

        options: dict[BDL_VBar_HAlign, tuple[float, BDL_VBar_HAlign]] = {
            "left": (self.bounds.x_min, "left"),
            "right": (self.bounds.x_max, "right"),
            "center": (self.bounds.center_x, "center"),
        }
        return options[h_align]

    def get_y(self, v_align: BDL_VBar_VAlign) -> tuple[float, BDL_VBar_VAlign]:
        """Get the anchor point Y coordinate and vertical alignment."""

        options: dict[BDL_VBar_VAlign, tuple[float, BDL_VBar_VAlign]] = {
            "bottom": (self.bounds.y_min, "bottom"),
            "top": (self.bounds.y_max, "top"),
            "center": (self.bounds.center_y, "center"),
            "outside": (self.bounds.y_max, "bottom"),
        }
        return options[v_align]

    def anchor(
        self,
        h_align: BDL_VBar_HAlign,
        v_align: BDL_VBar_VAlign,
    ) -> BDL_Bar_Anchor:

        x, ha = self.get_x(h_align)
        y, va = self.get_y(v_align)
        return BDL_Bar_Anchor(x=x, y=y, h_align=ha, v_align=va)
