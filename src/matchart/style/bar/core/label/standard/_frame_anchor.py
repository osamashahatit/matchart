"""Compute anchor points for bar chart standard framed data labels"""

from dataclasses import dataclass
from typing import Literal

type FDL_HBar_HAlign = Literal["left", "right", "center", "outside"]
type FDL_HBar_VAlign = Literal["top", "bottom", "center"]
type FDL_VBar_HAlign = Literal["left", "right", "center"]
type FDL_VBar_VAlign = Literal["top", "bottom", "center", "outside"]


@dataclass(frozen=True)
class FDL_Bar_Bounds:
    """Store bar rectangle bounds in data coordinates.

    Attributes:
        x_min (float): Minimum x coordinate of the bar rectangle.
        y_min (float): Minimum y coordinate of the bar rectangle.
        x_max (float): Maximum x coordinate of the bar rectangle.
        y_max (float): Maximum y coordinate of the bar rectangle.
    """

    x_min: float
    y_min: float
    x_max: float
    y_max: float

    @property
    def center_x(self) -> float:
        """Return the horizontal center of the bounds.

        Returns:
            float: (x_min + x_max) / 2.
        """
        return (self.x_min + self.x_max) / 2

    @property
    def center_y(self) -> float:
        """Return the vertical center of the bounds.

        Returns:
            float: (y_min + y_max) / 2.
        """
        return (self.y_min + self.y_max) / 2


@dataclass(frozen=True)
class FDL_Bar_FrameDimension:
    """Describe the framed label's size and border thickness.

    The half-border properties (border_x/border_y) are used to offset
    anchors so the frame is positioned accounting for stroke width.

    Attributes:
        width (float): Frame width.
        height (float): Frame height.
        border_width_x (float): Border width contribution in x direction.
        border_width_y (float): Border width contribution in y direction.
    """

    width: float
    height: float
    border_width_x: float
    border_width_y: float

    @property
    def border_x(self) -> float:
        """Return half the x border width.

        Returns:
            float: border_width_x / 2.
        """
        return self.border_width_x / 2

    @property
    def border_y(self) -> float:
        """Return half the y border width.

        Returns:
            float: border_width_y / 2.
        """
        return self.border_width_y / 2


@dataclass(frozen=True)
class FDL_Bar_Anchor:
    """Represent an anchor position for a framed label.

    Attributes:
        x (float): Anchor x coordinate in the target coordinate system.
        y (float): Anchor y coordinate in the target coordinate system.
    """

    x: float
    y: float


class FDL_HBar_Anchor:
    """Compute framed-label anchors for horizontal bars."""

    def __init__(self, bounds: FDL_Bar_Bounds, dimension: FDL_Bar_FrameDimension):
        """
        Args:
            bounds (FDL_Bar_Bounds): The bar rectangle bounds.
            dimension (FDL_Bar_FrameDimension): Frame size and border widths.
        """
        self.bounds = bounds
        self.dimension = dimension

    def get_x(self, h_align: FDL_HBar_HAlign) -> float:
        """Return the x coordinate for the framed label anchor.

        Args:
            h_align (FDL_HBar_HAlign): Horizontal alignment selection.
                Options: "left", "right", "center", "outside".

        Returns:
            float: Computed anchor x coordinate.

        Notes:
            For "right", the returned x is shifted left by the frame width so
            the frame's right edge aligns with the bar edge (minus border).
        """
        options: dict[FDL_HBar_HAlign, float] = {
            "left": self.bounds.x_min + self.dimension.border_x,
            "right": self.bounds.x_max - self.dimension.width - self.dimension.border_x,
            "center": self.bounds.center_x - (self.dimension.width / 2),
            "outside": self.bounds.x_max + self.dimension.border_x,
        }
        return options[h_align]

    def get_y(self, v_align: FDL_HBar_VAlign) -> float:
        """Return the y coordinate for the framed label anchor.

        Args:
            v_align (FDL_HBar_VAlign): Vertical alignment selection.
                Options: "top", "bottom", "center".

        Returns:
            float: Computed anchor y coordinate.

        Notes:
            For "top", the returned y is shifted down by the frame height so
            the frame's top edge aligns with the bar edge (minus border).
        """
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
        """Compute the framed label anchor for a horizontal bar.

        Args:
            h_align (FDL_HBar_HAlign): Horizontal alignment selection.
                Options: "left", "right", "center", "outside".
            v_align (FDL_HBar_VAlign): Vertical alignment selection.
                Options: "top", "bottom", "center".

        Returns:
            FDL_Bar_Anchor: Anchor coordinate for framed label placement.
        """
        return FDL_Bar_Anchor(x=self.get_x(h_align), y=self.get_y(v_align))


class FDL_VBar_Anchor:
    """Compute framed-label anchors for vertical bars."""

    def __init__(self, bounds: FDL_Bar_Bounds, dimension: FDL_Bar_FrameDimension):
        """
        Args:
            bounds (FDL_Bar_Bounds): The bar rectangle bounds.
            dimension (FDL_Bar_FrameDimension): Frame size and border widths.
        """
        self.bounds = bounds
        self.dimension = dimension

    def get_x(self, h_align: FDL_VBar_HAlign) -> float:
        """Return the x coordinate for the framed label anchor.

        Args:
            h_align (FDL_VBar_HAlign): Horizontal alignment selection.
                Options: "left", "right", "center".

        Returns:
            float: Computed anchor x coordinate.
        """
        options: dict[FDL_VBar_HAlign, float] = {
            "left": self.bounds.x_min + self.dimension.border_x,
            "right": self.bounds.x_max - self.dimension.width - self.dimension.border_x,
            "center": self.bounds.center_x - (self.dimension.width / 2),
        }
        return options[h_align]

    def get_y(self, v_align: FDL_VBar_VAlign) -> float:
        """Return the y coordinate for the framed label anchor.

        Args:
            v_align (FDL_VBar_VAlign): Vertical alignment selection.
                Options: "top", "bottom", "center", "outside".

        Returns:
            float: Computed anchor y coordinate.

        Notes:
            For "top", the returned y is shifted down by the frame height so
            the frame's top edge aligns with the bar edge (minus border).
        """
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
        """Compute the framed label anchor for a vertical bar.

        Args:
            h_align (FDL_VBar_HAlign): Horizontal alignment selection.
                Options: "left", "right", "center".
            v_align (FDL_VBar_VAlign): Vertical alignment selection.
                Options: "top", "bottom", "center", "outside".

        Returns:
            FDL_Bar_Anchor: Anchor coordinate for framed label placement.
        """
        return FDL_Bar_Anchor(x=self.get_x(h_align), y=self.get_y(v_align))
