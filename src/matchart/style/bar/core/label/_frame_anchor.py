from typing import Literal, cast
from dataclasses import dataclass

type HBarFDL_HAlign = Literal["left", "right", "center", "outside"]
type HBarFDL_VAlign = Literal["top", "bottom", "center"]
type VBarFDL_HAlign = Literal["left", "right", "center"]
type VBarFDL_VAlign = Literal["top", "bottom", "center", "outside"]


@dataclass(frozen=True)
class FDL_BarBounds:
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
class BarFDL_Dimension:
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
class BarFDL_Anchor:
    x: float
    y: float


class HBarFDL_AnchorResolver:
    """Resolver for horizontal bar framed data label anchor point."""

    def __init__(self, bounds: FDL_BarBounds, dimension: BarFDL_Dimension):
        self.bounds = bounds
        self.dimension = dimension

    def get_x(self, h_align: HBarFDL_HAlign) -> float:
        """Get the anchor point X coordinate."""

        options: dict[HBarFDL_HAlign, float] = {
            "left": self.bounds.x_min + self.dimension.border_x,
            "right": self.bounds.x_max - self.dimension.width - self.dimension.border_x,
            "center": self.bounds.center_x - (self.dimension.width / 2),
            "outside": self.bounds.x_max + self.dimension.border_x,
        }
        return options[h_align]

    def get_y(self, v_align: HBarFDL_VAlign) -> float:
        """Get the anchor point Y coordinate."""

        options: dict[HBarFDL_VAlign, float] = {
            "top": self.bounds.y_max - self.dimension.height - self.dimension.border_y,
            "bottom": self.bounds.y_min + self.dimension.border_y,
            "center": self.bounds.center_y - (self.dimension.height / 2),
        }
        return options[v_align]

    def resolve(
        self,
        h_align: HBarFDL_HAlign,
        v_align: HBarFDL_VAlign,
    ) -> BarFDL_Anchor:
        return BarFDL_Anchor(
            x=self.get_x(h_align),
            y=self.get_y(v_align),
        )


class VBarFDL_AnchorResolver:
    """Resolver for vertical bar framed data label anchor point."""

    def __init__(self, bounds: FDL_BarBounds, dimension: BarFDL_Dimension):
        self.bounds = bounds
        self.dimension = dimension

    def get_x(self, h_align: VBarFDL_HAlign) -> float:
        """Get the anchor point X coordinate."""

        options: dict[VBarFDL_HAlign, float] = {
            "left": self.bounds.x_min + self.dimension.border_x,
            "right": self.bounds.x_max - self.dimension.width - self.dimension.border_x,
            "center": self.bounds.center_x - (self.dimension.width / 2),
        }
        return options[h_align]

    def get_y(self, v_align: VBarFDL_VAlign) -> float:
        """Get the anchor point Y coordinate."""

        options: dict[VBarFDL_VAlign, float] = {
            "bottom": self.bounds.y_min + self.dimension.border_y,
            "top": self.bounds.y_max - self.dimension.height - self.dimension.border_y,
            "center": self.bounds.center_y - (self.dimension.height / 2),
            "outside": self.bounds.y_max + self.dimension.border_y,
        }
        return options[v_align]

    def resolve(
        self,
        h_align: VBarFDL_HAlign,
        v_align: VBarFDL_VAlign,
    ) -> BarFDL_Anchor:
        return BarFDL_Anchor(
            x=self.get_x(h_align),
            y=self.get_y(v_align),
        )


class BarFDL_AnchorResolver:
    """Resolver for bar framed data label anchor point based on orientation."""

    def __init__(
        self,
        horizontal: bool,
        bounds: tuple[float, float, float, float],
        dimension: BarFDL_Dimension,
        h_align: HBarFDL_HAlign | VBarFDL_HAlign,
        v_align: HBarFDL_VAlign | VBarFDL_VAlign,
        x_offset: float,
        y_offset: float,
    ):
        self.horizontal = horizontal
        self.bounds = FDL_BarBounds(*bounds)
        self.dimension = dimension
        self.h_align = h_align
        self.v_align = v_align
        self.x_offset = x_offset
        self.y_offset = y_offset

    def resolve(self) -> BarFDL_Anchor:

        if self.horizontal:
            resolver = HBarFDL_AnchorResolver(
                bounds=self.bounds, dimension=self.dimension
            )
            anchor = resolver.resolve(
                h_align=cast(HBarFDL_HAlign, self.h_align),
                v_align=cast(HBarFDL_VAlign, self.v_align),
            )
        else:
            resolver = VBarFDL_AnchorResolver(
                bounds=self.bounds, dimension=self.dimension
            )
            anchor = resolver.resolve(
                h_align=cast(VBarFDL_HAlign, self.h_align),
                v_align=cast(VBarFDL_VAlign, self.v_align),
            )
        return anchor
