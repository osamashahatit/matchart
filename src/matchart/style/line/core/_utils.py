from typing import Iterable, TypeVar, cast

import numpy as np
from matplotlib.axes import Axes
from matplotlib.collections import FillBetweenPolyCollection
from matplotlib.lines import Line2D

T = TypeVar("T")


class LineStyleHelper:
    def __init__(self, ax: Axes) -> None:
        self.ax = ax

    def get_tick_labels(self) -> list[str]:
        tick_labels: list[str] = []
        for label in self.ax.get_xticklabels():
            tick_labels.append(label.get_text())
        return tick_labels

    def get_legend_labels(self) -> list[str]:
        legend_labels: list[str] = []
        for line in self.ax.lines:
            legend_labels.append(cast(str, line.get_label()))
        return legend_labels

    def validate_legend_entry(self, mapping: dict[str, T]) -> None:
        legend_labels = self.get_legend_labels()
        dict_keys = set(mapping.keys())
        valid_labels = set(legend_labels)
        invalid_keys = dict_keys - valid_labels
        if invalid_keys:
            raise ValueError(
                f"Invalid legend labels in dictionary keys: {invalid_keys}. "
                f"Available legend labels are: {legend_labels}"
            )

    def get_point_value(self, line: Line2D, tick_label: str) -> float:
        tick_labels = self.get_tick_labels()
        index = tick_labels.index(tick_label)
        y_data = np.asarray(line.get_ydata(), dtype=float)
        return float(y_data[index])


class LineGenerator:
    def __init__(self, ax: Axes) -> None:
        self.ax = ax

    def standard(self) -> Iterable[Line2D]:
        for line in self.ax.lines:
            yield line

    def map_legend(self, property: dict[str, T]) -> Iterable[tuple[Line2D, T]]:
        for line in self.ax.lines:
            prop = property.get(cast(str, line.get_label()))
            if prop is not None:
                yield line, prop


class AreaGenerator:
    def __init__(self, ax: Axes) -> None:
        self.ax = ax

    def standard(self) -> Iterable[FillBetweenPolyCollection]:
        for area in self.ax.collections:
            if isinstance(area, FillBetweenPolyCollection):
                yield area

    def map_legend(
        self,
        property: dict[str, T],
    ) -> Iterable[tuple[FillBetweenPolyCollection, T]]:
        for area in self.ax.collections:
            if isinstance(area, FillBetweenPolyCollection):
                legend_label = getattr(area, "_legend_label", None)
                if legend_label is not None:
                    prop = property.get(legend_label)
                    if prop is not None:
                        yield area, prop
