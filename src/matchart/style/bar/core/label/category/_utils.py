from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.container import BarContainer

from ..._utils import BarStyleHelper


@dataclass(frozen=True)
class CDL_Bar_Bounds:
    min: float
    max: float

    @property
    def center(self) -> float:
        return (self.min + self.max) / 2

    @classmethod
    def bounds(
        cls,
        ax: Axes,
        help: BarStyleHelper,
        horizontal: bool,
        category_index: str,
    ) -> "CDL_Bar_Bounds":
        """Get spatial bounds for bar chart category basic data labeler based on orientation."""

        category_labels: list[str] = help.get_tick_labels()
        attr_min = "y0" if horizontal else "x0"
        attr_max = "y1" if horizontal else "x1"
        min_val = float("inf")
        max_val = float("-inf")

        for container in ax.containers:
            if isinstance(container, BarContainer):
                for patch_index, patch in enumerate(container.patches):
                    if category_labels[patch_index] == category_index:
                        min_val = min(min_val, getattr(patch.get_bbox(), attr_min))
                        max_val = max(max_val, getattr(patch.get_bbox(), attr_max))

        return cls(min=min_val, max=max_val)


@dataclass(frozen=True)
class CDL_Bar_Totals:
    value: float

    @classmethod
    def totals(
        cls,
        ax: Axes,
        help: BarStyleHelper,
        horizontal: bool,
        category_index: str,
    ) -> "CDL_Bar_Totals":
        """Get total value for bar chart category basic data labeler based on orientation."""

        category_labels: list[str] = help.get_tick_labels()
        attr_value = "width" if horizontal else "height"
        total_val = 0.0

        for container in ax.containers:
            if isinstance(container, BarContainer):
                for patch_index, patch in enumerate(container.patches):
                    if category_labels[patch_index] == category_index:
                        total_val += getattr(patch, f"get_{attr_value}")()

        return cls(value=total_val)
