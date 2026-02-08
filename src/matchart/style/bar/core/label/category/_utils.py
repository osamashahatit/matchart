"""Utilities for bar charts category data labels."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.container import BarContainer

from matchart.style.bar.core._utils import BarStyleHelper


@dataclass(frozen=True)
class CDL_Bar_Bounds:
    """Represent the aggregate span for a tick label across bar containers.

    Attributes:
        min (float): Minimum bound across all matching bar patches.
        max (float): Maximum bound across all matching bar patches.
    """

    min: float
    max: float

    @property
    def center(self) -> float:
        """Return the midpoint of the aggregate bounds.

        Returns:
            float: (min + max) / 2.
        """
        return (self.min + self.max) / 2

    @classmethod
    def bounds(
        cls,
        ax: Axes,
        helper: BarStyleHelper,
        horizontal: bool,
        tick_label: str,
    ) -> "CDL_Bar_Bounds":
        """Compute aggregate bounds for a tick label across all bar containers.

        Args:
            ax (Axes): Axes that already contains bar artists.
            helper (BarStyleHelper): Helper providing tick label text lookup.
            horizontal (bool): Whether the bar chart is horizontal.
            tick_label (str): Tick label to match against.

        Returns:
            CDL_Bar_Bounds: The aggregate min/max bounds.

        Notes:
            - For horizontal bars, this aggregates y0/y1 (the bar thickness
              direction).
            - For vertical bars, this aggregates x0/x1 (the bar thickness
              direction).
            - If tick_label is not found, returns min=inf and max=-inf.
        """
        min_bound = "y0" if horizontal else "x0"
        max_bound = "y1" if horizontal else "x1"
        min_value = float("inf")
        max_value = float("-inf")

        for container in ax.containers:
            if isinstance(container, BarContainer):
                for index, patch in enumerate(container.patches):
                    if helper.get_tick_labels()[index] == tick_label:
                        bbox = patch.get_bbox()
                        min_value = min(min_value, getattr(bbox, min_bound))
                        max_value = max(max_value, getattr(bbox, max_bound))

        return cls(min=min_value, max=max_value)


@dataclass(frozen=True)
class CDL_Bar_Totals:
    """Represent the aggregate total value for a tick label.

    Attributes:
        total (float): Sum of values across all matching bar patches.
    """

    total: float

    @classmethod
    def compute_total(
        cls,
        ax: Axes,
        helper: BarStyleHelper,
        horizontal: bool,
        tick_label: str,
    ) -> "CDL_Bar_Totals":
        """Sum bar values for a tick label across all bar containers.

        Args:
            ax (Axes): Axes that already contains bar artists.
            helper (BarStyleHelper): Helper providing tick label text lookup.
            horizontal (bool): Whether the bar chart is horizontal.
            tick_label (str): Tick label to match against.

        Returns:
            CDL_Bar_Totals: Total value across matching patches.

        Notes:
            - For horizontal bars, sums Rectangle.get_width().
            - For vertical bars, sums Rectangle.get_height().
            - If tick_label is not found, returns total=0.0.
        """
        patch_value = "width" if horizontal else "height"
        total = 0.0

        for container in ax.containers:
            if isinstance(container, BarContainer):
                for index, patch in enumerate(container.patches):
                    if helper.get_tick_labels()[index] == tick_label:
                        total += getattr(patch, f"get_{patch_value}")()

        return cls(total=total)
