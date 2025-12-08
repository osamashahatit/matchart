from typing import Literal, cast
from dataclasses import dataclass

type HBarBDL_HAlign = Literal["left", "right", "center", "outside"]
type HBarBDL_VAlign = Literal["top", "bottom", "center"]
type VBarBDL_HAlign = Literal["left", "right", "center"]
type VBarBDL_VAlign = Literal["top", "bottom", "center", "outside"]


@dataclass(frozen=True)
class BDL_BarBounds:
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
class BarBDL_Anchor:
    x: float
    y: float
    h_align: HBarBDL_HAlign | VBarBDL_HAlign
    v_align: HBarBDL_VAlign | VBarBDL_VAlign


class HBarBDL_AnchorResolver:
    """Resolver for horizontal bar basic data label anchor point."""

    def __init__(self, bounds: BDL_BarBounds):
        self.bounds = bounds

    def get_x(self, h_align: HBarBDL_HAlign) -> tuple[float, HBarBDL_HAlign]:
        """Get the anchor point X coordinate and horizontal alignment."""

        options: dict[HBarBDL_HAlign, tuple[float, HBarBDL_HAlign]] = {
            "left": (self.bounds.x_min, "left"),
            "right": (self.bounds.x_max, "right"),
            "center": (self.bounds.center_x, "center"),
            "outside": (self.bounds.x_max, "left"),
        }
        return options[h_align]

    def get_y(self, v_align: HBarBDL_VAlign) -> tuple[float, HBarBDL_VAlign]:
        """Get the anchor point Y coordinate and vertical alignment."""

        options: dict[HBarBDL_VAlign, tuple[float, HBarBDL_VAlign]] = {
            "top": (self.bounds.y_max, "top"),
            "bottom": (self.bounds.y_min, "bottom"),
            "center": (self.bounds.center_y, "center"),
        }
        return options[v_align]

    def resolve(
        self,
        h_align: HBarBDL_HAlign,
        v_align: HBarBDL_VAlign,
    ) -> BarBDL_Anchor:
        x, ha = self.get_x(h_align)
        y, va = self.get_y(v_align)
        return BarBDL_Anchor(x=x, y=y, h_align=ha, v_align=va)


class VBarBDL_AnchorResolver:
    """Resolver for vertical bar basic data label anchor point."""

    def __init__(self, bounds: BDL_BarBounds):
        self.bounds = bounds

    def get_x(self, h_align: VBarBDL_HAlign) -> tuple[float, VBarBDL_HAlign]:
        """Get the anchor point X coordinate and horizontal alignment."""

        options: dict[VBarBDL_HAlign, tuple[float, VBarBDL_HAlign]] = {
            "left": (self.bounds.x_min, "left"),
            "right": (self.bounds.x_max, "right"),
            "center": (self.bounds.center_x, "center"),
        }
        return options[h_align]

    def get_y(self, v_align: VBarBDL_VAlign) -> tuple[float, VBarBDL_VAlign]:
        """Get the anchor point Y coordinate and vertical alignment."""

        options: dict[VBarBDL_VAlign, tuple[float, VBarBDL_VAlign]] = {
            "bottom": (self.bounds.y_min, "bottom"),
            "top": (self.bounds.y_max, "top"),
            "center": (self.bounds.center_y, "center"),
            "outside": (self.bounds.y_max, "bottom"),
        }
        return options[v_align]

    def resolve(
        self,
        h_align: VBarBDL_HAlign,
        v_align: VBarBDL_VAlign,
    ) -> BarBDL_Anchor:
        x, ha = self.get_x(h_align)
        y, va = self.get_y(v_align)
        return BarBDL_Anchor(x=x, y=y, h_align=ha, v_align=va)


class BarBDL_AnchorResolver:
    """Resolver for bar basic data label anchor point based on orientation."""

    def __init__(
        self,
        horizontal: bool,
        bounds: BDL_BarBounds,
        h_align: HBarBDL_HAlign | VBarBDL_HAlign,
        v_align: HBarBDL_VAlign | VBarBDL_VAlign,
    ):
        self.horizontal = horizontal
        self.bounds = bounds
        self.h_align = h_align
        self.v_align = v_align

    def resolve(self) -> BarBDL_Anchor:

        if self.horizontal:
            resolver = HBarBDL_AnchorResolver(self.bounds)
            anchor = resolver.resolve(
                h_align=cast(HBarBDL_HAlign, self.h_align),
                v_align=cast(HBarBDL_VAlign, self.v_align),
            )
        else:
            resolver = VBarBDL_AnchorResolver(self.bounds)
            anchor = resolver.resolve(
                h_align=cast(VBarBDL_HAlign, self.h_align),
                v_align=cast(VBarBDL_VAlign, self.v_align),
            )
        return anchor
