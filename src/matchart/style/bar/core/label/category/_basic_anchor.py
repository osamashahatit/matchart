"""Compute anchor points for bar chart category basic data labels"""

from dataclasses import dataclass
from typing import Literal

from matplotlib.axes import Axes

from ._utils import CDL_Bar_Bounds

type CBDL_HBar_VAlign = Literal["top", "bottom", "center"]
type CBDL_VBar_HAlign = Literal["left", "right", "center"]


@dataclass(frozen=True)
class CBDL_Bar_Anchor:
    """Represent a category label anchor and resolved alignments."""

    x: float
    y: float
    h_align: CBDL_VBar_HAlign
    v_align: CBDL_HBar_VAlign


class CBDL_HBar_Anchor:
    """Compute category label anchors for horizontal bar charts."""

    def __init__(self, ax: Axes, bounds: CDL_Bar_Bounds):
        """
        Args:
            ax (Axes): Target axes used to read view limits.
            bounds (CDL_Bar_Bounds): Aggregate category span used for y
                positioning.
        """
        self.ax = ax
        self.bounds = bounds

    def get_x(self) -> float:
        """Return the x coordinate at the right edge of the current view.

        Returns:
            float: ax.get_xlim()[1].
        """
        return self.ax.get_xlim()[1]

    def get_y(self, v_align: CBDL_HBar_VAlign) -> tuple[float, CBDL_HBar_VAlign]:
        """Return the y coordinate and resolved v_align for the category.

        Args:
            v_align (CBDL_HBar_VAlign): Vertical alignment selection.
                Options: "top", "bottom", "center".

        Returns:
            tuple[float, CBDL_HBar_VAlign]: (y, resolved_v_align).
        """
        options: dict[CBDL_HBar_VAlign, tuple[float, CBDL_HBar_VAlign]] = {
            "top": (self.bounds.max, "top"),
            "bottom": (self.bounds.min, "bottom"),
            "center": (self.bounds.center, "center"),
        }
        return options[v_align]

    def anchor(self, v_align: CBDL_HBar_VAlign) -> CBDL_Bar_Anchor:
        """Compute the category label anchor for a horizontal bar chart.

        Args:
            v_align (CBDL_HBar_VAlign): Vertical alignment selection.
                Options: "top", "bottom", "center".

        Returns:
            CBDL_Bar_Anchor: Anchor coordinate plus alignment metadata.

        Notes:
            Horizontal category anchors always use h_align="right" to align
            labels against the right plot edge.
        """
        x_max = self.get_x()
        y, v_align = self.get_y(v_align)
        return CBDL_Bar_Anchor(x=x_max, y=y, h_align="right", v_align=v_align)


class CBDL_VBar_Anchor:
    """Compute category label anchors for vertical bar charts."""

    def __init__(self, ax: Axes, bounds: CDL_Bar_Bounds):
        """
        Args:
            ax (Axes): Target axes used to read view limits.
            bounds (CDL_Bar_Bounds): Aggregate category span used for x
                positioning.
        """
        self.ax = ax
        self.bounds = bounds

    def get_x(self, h_align: CBDL_VBar_HAlign) -> tuple[float, CBDL_VBar_HAlign]:
        """Return the x coordinate and resolved h_align for the category.

        Args:
            h_align (CBDL_VBar_HAlign): Horizontal alignment selection.
                Options: "left", "right", "center".

        Returns:
            tuple[float, CBDL_VBar_HAlign]: (x, resolved_h_align).
        """
        options: dict[CBDL_VBar_HAlign, tuple[float, CBDL_VBar_HAlign]] = {
            "left": (self.bounds.min, "left"),
            "right": (self.bounds.max, "right"),
            "center": (self.bounds.center, "center"),
        }
        return options[h_align]

    def get_y(self) -> float:
        """Return the y coordinate at the top edge of the current view.

        Returns:
            float: ax.get_ylim()[1].
        """
        return self.ax.get_ylim()[1]

    def anchor(self, h_align: CBDL_VBar_HAlign) -> CBDL_Bar_Anchor:
        """Compute the category label anchor for a vertical bar chart.

        Args:
            h_align (CBDL_VBar_HAlign): Horizontal alignment selection.
                Options: "left", "right", "center".

        Returns:
            CBDL_Bar_Anchor: Anchor coordinate plus alignment metadata.

        Notes:
            Vertical category anchors always use v_align="top" to align labels
            against the top plot edge.
        """
        x, h_align = self.get_x(h_align)
        y_max = self.get_y()
        return CBDL_Bar_Anchor(x=x, y=y_max, h_align=h_align, v_align="top")
