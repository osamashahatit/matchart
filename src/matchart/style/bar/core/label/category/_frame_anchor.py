"""Compute anchor points for bar chart category framed data labels"""

from dataclasses import dataclass
from typing import Literal

from matplotlib.axes import Axes

from ._utils import CDL_Bar_Bounds

type CFDL_HBar_VAlign = Literal["top", "bottom", "center"]
type CFDL_VBar_HAlign = Literal["left", "right", "center"]


@dataclass(frozen=True)
class CFDL_Bar_FrameDimension:
    """Describe the framed category label's size and border thickness.

    The half-border properties (border_x/border_y) are used to offset the
    frame so its stroke is accounted for when aligning to plot edges.

    Attributes:
        width (float): Frame width in the target coordinate system.
        height (float): Frame height in the target coordinate system.
        border_width_x (float): Border width contribution in the x direction.
        border_width_y (float): Border width contribution in the y direction.
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
class CFDL_Bar_Anchor:
    """Represent an anchor position for a framed category label.

    Attributes:
        x (float): Anchor x coordinate.
        y (float): Anchor y coordinate.
    """

    x: float
    y: float


class CFDL_HBar_Anchor:
    """Compute framed category label anchors for horizontal bar charts."""

    def __init__(
        self,
        ax: Axes,
        bounds: CDL_Bar_Bounds,
        dimension: CFDL_Bar_FrameDimension,
    ):
        """
        Args:
            ax (Axes): Target axes used to read view limits.
            bounds (CDL_Bar_Bounds): Aggregate category span used for y
                positioning.
            dimension (CFDL_Bar_FrameDimension): Frame size and border widths.
        """
        self.ax = ax
        self.bounds = bounds
        self.dimension = dimension

    def get_x(self) -> float:
        """Return the x coordinate for the frame at the right plot edge.

        Returns:
            float: ax.get_xlim()[1] - width - half_border_x.

        Notes:
            The subtraction by width ensures the frame is placed fully inside
            the view bounds.
        """
        return self.ax.get_xlim()[1] - self.dimension.width - self.dimension.border_x

    def get_y(self, v_align: CFDL_HBar_VAlign) -> float:
        """Return the y coordinate for the framed category label anchor.

        Args:
            v_align (CFDL_HBar_VAlign): Vertical alignment selection.
                Options: "top", "bottom", "center".

        Returns:
            float: Computed anchor y coordinate.

        Notes:
            For "top", the returned y is shifted down by the frame height so
            the frame's top edge aligns with the category max (minus border).
        """
        options: dict[CFDL_HBar_VAlign, float] = {
            "top": self.bounds.max - self.dimension.height - self.dimension.border_y,
            "bottom": self.bounds.min + self.dimension.border_y,
            "center": self.bounds.center - (self.dimension.height / 2),
        }
        return options[v_align]

    def anchor(self, v_align: CFDL_HBar_VAlign) -> CFDL_Bar_Anchor:
        """Compute the framed category label anchor for a horizontal bar chart.

        Args:
            v_align (CFDL_HBar_VAlign): Vertical alignment selection.
                Options: "top", "bottom", "center".

        Returns:
            CFDL_Bar_Anchor: Anchor coordinate for framed label placement.
        """
        return CFDL_Bar_Anchor(x=self.get_x(), y=self.get_y(v_align))


class CFDL_VBar_Anchor:
    """Compute framed category label anchors for vertical bar charts."""

    def __init__(
        self,
        ax: Axes,
        bounds: CDL_Bar_Bounds,
        dimension: CFDL_Bar_FrameDimension,
    ):
        """
        Args:
            ax (Axes): Target axes used to read view limits.
            bounds (CDL_Bar_Bounds): Aggregate category span used for x
                positioning.
            dimension (CFDL_Bar_FrameDimension): Frame size and border widths.
        """
        self.ax = ax
        self.bounds = bounds
        self.dimension = dimension

    def get_x(self, h_align: CFDL_VBar_HAlign) -> float:
        """Return the x coordinate for the framed category label anchor.

        Args:
            h_align (CFDL_VBar_HAlign): Horizontal alignment selection.
                Options: "left", "right", "center".

        Returns:
            float: Computed anchor x coordinate.

        Notes:
            For "right", the returned x is shifted left by the frame width so
            the frame's right edge aligns with the category max (minus border).
        """
        options: dict[CFDL_VBar_HAlign, float] = {
            "left": self.bounds.min + self.dimension.border_x,
            "right": self.bounds.max - self.dimension.width - self.dimension.border_x,
            "center": self.bounds.center - (self.dimension.width / 2),
        }
        return options[h_align]

    def get_y(self) -> float:
        """Return the y coordinate for the frame at the top plot edge.

        Returns:
            float: ax.get_ylim()[1] - height - half_border_y.

        Notes:
            The subtraction by height ensures the frame is placed fully inside
            the view bounds.
        """
        return self.ax.get_ylim()[1] - self.dimension.height - self.dimension.border_y

    def anchor(self, h_align: CFDL_VBar_HAlign) -> CFDL_Bar_Anchor:
        """Compute the framed category label anchor for a vertical bar chart.

        Args:
            h_align (CFDL_VBar_HAlign): Horizontal alignment selection.
                Options: "left", "right", "center".

        Returns:
            CFDL_Bar_Anchor: Anchor coordinate for framed label placement.
        """
        return CFDL_Bar_Anchor(x=self.get_x(h_align), y=self.get_y())
