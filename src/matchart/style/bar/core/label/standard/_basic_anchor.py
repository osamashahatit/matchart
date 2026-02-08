"""Compute anchor points for bar chart standard basic data labels"""

from dataclasses import dataclass
from typing import Literal

type BDL_HBar_HAlign = Literal["left", "right", "center", "outside"]
type BDL_HBar_VAlign = Literal["top", "bottom", "center"]
type BDL_VBar_HAlign = Literal["left", "right", "center"]
type BDL_VBar_VAlign = Literal["top", "bottom", "center", "outside"]


@dataclass(frozen=True)
class BDL_Bar_Bounds:
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
class BDL_Bar_Anchor:
    """Represent an anchor position and resolved alignment metadata.

    The resolved alignment values may differ from the requested values,
    most notably for the "outside" option which returns an outward-facing
    alignment for downstream text placement.

    Attributes:
        x (float): Anchor x coordinate in data coordinates.
        y (float): Anchor y coordinate in data coordinates.
        h_align (BDL_HBar_HAlign | BDL_VBar_HAlign): Resolved horizontal
            alignment. Options: "left", "right", "center", "outside".
        v_align (BDL_HBar_VAlign | BDL_VBar_VAlign): Resolved vertical
            alignment. Options: "top", "bottom", "center", "outside".
    """

    x: float
    y: float
    h_align: BDL_HBar_HAlign | BDL_VBar_HAlign
    v_align: BDL_HBar_VAlign | BDL_VBar_VAlign


class BDL_HBar_Anchor:
    """Compute label anchors for horizontal bars.

    Horizontal bars are assumed to extend in the +x direction, with
    "outside" interpreted as anchoring at x_max while flipping h_align to
    "left" (outward-facing) for downstream text alignment.
    """

    def __init__(self, bounds: BDL_Bar_Bounds):
        """
        Args:
            bounds (BDL_Bar_Bounds): The bar rectangle bounds in data
                coordinates.
        """
        self.bounds = bounds

    def get_x(self, h_align: BDL_HBar_HAlign) -> tuple[float, BDL_HBar_HAlign]:
        """Return the x coordinate and resolved h_align for a horizontal bar.

        Args:
            h_align (BDL_HBar_HAlign): Horizontal alignment selection.
                Options: "left", "right", "center", "outside".

        Returns:
            tuple[float, BDL_HBar_HAlign]: (x, resolved_h_align).

        Notes:
            The "outside" option anchors at x_max and resolves the alignment
            to "left" so text can be placed outward from the bar edge.
        """
        options: dict[BDL_HBar_HAlign, tuple[float, BDL_HBar_HAlign]] = {
            "left": (self.bounds.x_min, "left"),
            "right": (self.bounds.x_max, "right"),
            "center": (self.bounds.center_x, "center"),
            "outside": (self.bounds.x_max, "left"),
        }
        return options[h_align]

    def get_y(self, v_align: BDL_HBar_VAlign) -> tuple[float, BDL_HBar_VAlign]:
        """Return the y coordinate and resolved v_align for a horizontal bar.

        Args:
            v_align (BDL_HBar_VAlign): Vertical alignment selection.
                Options: "top", "bottom", "center".

        Returns:
            tuple[float, BDL_HBar_VAlign]: (y, resolved_v_align).
        """
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
        """Compute the final anchor and resolved alignments for a bar.

        Args:
            h_align (BDL_HBar_HAlign): Horizontal alignment selection.
                Options: "left", "right", "center", "outside".
            v_align (BDL_HBar_VAlign): Vertical alignment selection.
                Options: "top", "bottom", "center".

        Returns:
            BDL_Bar_Anchor: Anchor coordinate plus resolved alignment values.
        """
        x, h_align = self.get_x(h_align)
        y, v_align = self.get_y(v_align)
        return BDL_Bar_Anchor(x=x, y=y, h_align=h_align, v_align=v_align)


class BDL_VBar_Anchor:
    """Compute label anchors for vertical bars.

    Vertical bars are assumed to extend in the +y direction, with
    "outside" interpreted as anchoring at y_max while flipping v_align to
    "bottom" (outward-facing) for downstream text alignment.
    """

    def __init__(self, bounds: BDL_Bar_Bounds):
        """I
        Args:
            bounds (BDL_Bar_Bounds): The bar rectangle bounds in data
                coordinates.
        """
        self.bounds = bounds

    def get_x(self, h_align: BDL_VBar_HAlign) -> tuple[float, BDL_VBar_HAlign]:
        """Return the x coordinate and resolved h_align for a vertical bar.

        Args:
            h_align (BDL_VBar_HAlign): Horizontal alignment selection.
                Options: "left", "right", "center".

        Returns:
            tuple[float, BDL_VBar_HAlign]: (x, resolved_h_align).
        """
        options: dict[BDL_VBar_HAlign, tuple[float, BDL_VBar_HAlign]] = {
            "left": (self.bounds.x_min, "left"),
            "right": (self.bounds.x_max, "right"),
            "center": (self.bounds.center_x, "center"),
        }
        return options[h_align]

    def get_y(self, v_align: BDL_VBar_VAlign) -> tuple[float, BDL_VBar_VAlign]:
        """Return the y coordinate and resolved v_align for a vertical bar.

        Args:
            v_align (BDL_VBar_VAlign): Vertical alignment selection.
                Options: "top", "bottom", "center", "outside".

        Returns:
            tuple[float, BDL_VBar_VAlign]: (y, resolved_v_align).

        Notes:
            The "outside" option anchors at y_max and resolves the alignment
            to "bottom" so text can be placed outward from the bar edge.
        """
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
        """Compute the final anchor and resolved alignments for a bar.

        Args:
            h_align (BDL_VBar_HAlign): Horizontal alignment selection.
                Options: "left", "right", "center".
            v_align (BDL_VBar_VAlign): Vertical alignment selection.
                Options: "top", "bottom", "center", "outside".

        Returns:
            BDL_Bar_Anchor: Anchor coordinate plus resolved alignment values.
        """
        x, h_align = self.get_x(h_align)
        y, v_align = self.get_y(v_align)
        return BDL_Bar_Anchor(x=x, y=y, h_align=h_align, v_align=v_align)
