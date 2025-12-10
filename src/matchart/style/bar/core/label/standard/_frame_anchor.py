from typing import Literal
from dataclasses import dataclass

type FDL_HBar_HAlign = Literal["left", "right", "center", "outside"]
type FDL_HBar_VAlign = Literal["top", "bottom", "center"]
type FDL_VBar_HAlign = Literal["left", "right", "center"]
type FDL_VBar_VAlign = Literal["top", "bottom", "center", "outside"]


@dataclass(frozen=True)
class FDL_Bar_Bounds:
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
class FDL_Bar_Dimension:
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
class FDL_Bar_Anchor:
    x: float
    y: float


class FDL_HBar_Anchor:

    def __init__(self, bounds: FDL_Bar_Bounds, dimension: FDL_Bar_Dimension):
        self.bounds = bounds
        self.dimension = dimension

    def get_x(self, h_align: FDL_HBar_HAlign) -> float:
        """Get the anchor point X coordinate."""

        options: dict[FDL_HBar_HAlign, float] = {
            "left": self.bounds.x_min + self.dimension.border_x,
            "right": self.bounds.x_max - self.dimension.width - self.dimension.border_x,
            "center": self.bounds.center_x - (self.dimension.width / 2),
            "outside": self.bounds.x_max + self.dimension.border_x,
        }
        return options[h_align]

    def get_y(self, v_align: FDL_HBar_VAlign) -> float:
        """Get the anchor point Y coordinate."""

        options: dict[FDL_HBar_VAlign, float] = {
            "top": self.bounds.y_max - self.dimension.height - self.dimension.border_y,
            "bottom": self.bounds.y_min + self.dimension.border_y,
            "center": self.bounds.center_y - (self.dimension.height / 2),
        }
        return options[v_align]

    def anchor(
        self,
        h_align: FDL_HBar_HAlign,
        v_align: FDL_HBar_VAlign,
    ) -> FDL_Bar_Anchor:
        return FDL_Bar_Anchor(x=self.get_x(h_align), y=self.get_y(v_align))


class FDL_VBar_Anchor:

    def __init__(self, bounds: FDL_Bar_Bounds, dimension: FDL_Bar_Dimension):
        self.bounds = bounds
        self.dimension = dimension

    def get_x(self, h_align: FDL_VBar_HAlign) -> float:
        """Get the anchor point X coordinate."""

        options: dict[FDL_VBar_HAlign, float] = {
            "left": self.bounds.x_min + self.dimension.border_x,
            "right": self.bounds.x_max - self.dimension.width - self.dimension.border_x,
            "center": self.bounds.center_x - (self.dimension.width / 2),
        }
        return options[h_align]

    def get_y(self, v_align: FDL_VBar_VAlign) -> float:
        """Get the anchor point Y coordinate."""

        options: dict[FDL_VBar_VAlign, float] = {
            "bottom": self.bounds.y_min + self.dimension.border_y,
            "top": self.bounds.y_max - self.dimension.height - self.dimension.border_y,
            "center": self.bounds.center_y - (self.dimension.height / 2),
            "outside": self.bounds.y_max + self.dimension.border_y,
        }
        return options[v_align]

    def anchor(
        self,
        h_align: FDL_VBar_HAlign,
        v_align: FDL_VBar_VAlign,
    ) -> FDL_Bar_Anchor:
        return FDL_Bar_Anchor(x=self.get_x(h_align), y=self.get_y(v_align))
