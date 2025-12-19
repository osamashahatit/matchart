from typing import Iterable, cast, TypeVar
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.collections import FillBetweenPolyCollection

T = TypeVar("T")


class LineStyleHelper:

    def __init__(self, ax: Axes) -> None:
        self.ax = ax

    def get_legend_labels(self) -> list[str]:
        """Get legend labels."""

        legend_labels: list[str] = []
        for line in self.ax.lines:
            legend_labels.append(cast(str, line.get_label()))
        return legend_labels

    def validate_legend_entry(self, dict: dict[str, T]) -> None:
        """Validate that dictionary keys match legend labels."""

        legend_labels = self.get_legend_labels()
        dict_keys = set(dict.keys())
        valid_labels = set(legend_labels)
        invalid_keys = dict_keys - valid_labels
        if invalid_keys:
            raise ValueError(
                f"Invalid legend labels in dictionary keys: {invalid_keys}. "
                f"Available legend labels are: {legend_labels}"
            )


class LineGenerator:

    def __init__(self, ax: Axes) -> None:
        self.ax = ax

    def standard(self) -> Iterable[Line2D]:
        """Generate standard lines without any properties."""

        for line in self.ax.lines:
            yield line

    def map_legend(self, property: dict[str, T]) -> Iterable[tuple[Line2D, T]]:
        """Generate lines with properties mapped to legend labels."""

        for line in self.ax.lines:
            prop = property.get(cast(str, line.get_label()))
            if prop is not None:
                yield line, prop


class AreaGenerator:

    def __init__(self, ax: Axes) -> None:
        self.ax = ax

    def standard(self) -> Iterable[FillBetweenPolyCollection]:
        """Generate area fills without any properties."""

        for area in self.ax.collections:
            if isinstance(area, FillBetweenPolyCollection):
                yield area

    def map_legend(
        self,
        property: dict[str, T],
    ) -> Iterable[tuple[FillBetweenPolyCollection, T]]:
        """Generate area fills with properties mapped to legend labels."""

        for area in self.ax.collections:
            if isinstance(area, FillBetweenPolyCollection):
                legend_label = getattr(area, "_legend_label", None)
                if legend_label is not None:
                    prop = property.get(legend_label)
                    if prop is not None:
                        yield area, prop
