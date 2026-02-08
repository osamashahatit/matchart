"""Utilities for line chart stylers."""

from typing import Iterable, TypeVar, cast

import numpy as np
from matplotlib.axes import Axes
from matplotlib.collections import FillBetweenPolyCollection
from matplotlib.lines import Line2D

T = TypeVar("T")


class LineStyleHelper:
    """Inspect line-chart artists and metadata on an Axes.

    This helper supports common matchart operations such as:
    - Addressing points by x tick label.
    - Mapping legend labels to per-line style values.
    """

    def __init__(self, ax: Axes) -> None:
        """
        Args:
            ax (Axes): Axes that already contains line/area artists.
        """
        self.ax = ax

    def get_tick_labels(self) -> list[str]:
        """Return x-axis tick label texts in display order.

        Returns:
            list[str]: Tick label text from ax.get_xticklabels().
        """
        tick_labels: list[str] = []
        for label in self.ax.get_xticklabels():
            tick_labels.append(label.get_text())
        return tick_labels

    def get_legend_labels(self) -> list[str]:
        """Return legend labels for lines on the Axes.

        Returns:
            list[str]: Labels from each Line2D.get_label() in ax.lines.

        Notes:
            This method does not filter out sentinel labels (e.g. "_nolegend_")
            or empty strings.
        """
        legend_labels: list[str] = []
        for line in self.ax.lines:
            legend_labels.append(cast(str, line.get_label()))
        return legend_labels

    def validate_legend_entry(self, mapping: dict[str, T]) -> None:
        """Validate that mapping keys match available line legend labels.

        Args:
            mapping (dict[str, T]): Mapping from legend label text to a property
                value.

        Raises:
            ValueError: If any mapping keys are not present in the Axes line
                legend labels. The error message includes the available labels.
        """
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
        """Return the line's y-value at the index corresponding to tick_label.

        Args:
            line (Line2D): Line artist whose y-data is queried.
            tick_label (str): X-axis tick label identifying which point to read.

        Returns:
            float: The y-value from the line's y-data corresponding to the tick.

        Raises:
            ValueError: If tick_label is not present in the Axes tick labels.
            IndexError: If the line has fewer y-data points than tick labels.

        Notes:
            This method assumes that tick label ordering corresponds to the
            ordering of line y-data indices.
        """
        tick_labels = self.get_tick_labels()
        index = tick_labels.index(tick_label)
        y_data = np.asarray(line.get_ydata(), dtype=float)
        return float(y_data[index])


class LineYielder:
    """Yield Line2D artists from an Axes, optionally paired with mapped values."""

    def __init__(self, ax: Axes) -> None:
        """
        Args:
            ax (Axes): Axes that already contains line artists.
        """
        self.ax = ax

    def standard(self) -> Iterable[Line2D]:
        """Yield all Line2D objects on the Axes.

        Yields:
            Line2D: Each line in ax.lines.
        """
        for line in self.ax.lines:
            yield line

    def map_legend(self, property: dict[str, T]) -> Iterable[tuple[Line2D, T]]:
        """Yield lines paired with values mapped by legend label.

        Args:
            property (dict[str, T]): Mapping from line legend label text to a
                value.

        Yields:
            tuple[Line2D, T]: (line, value) for lines whose labels exist in the
            mapping.
        """
        for line in self.ax.lines:
            prop = property.get(cast(str, line.get_label()))
            if prop is not None:
                yield line, prop


class AreaYielder:
    """Yield fill_between area artists from an Axes, optionally legend-mapped."""

    def __init__(self, ax: Axes) -> None:
        """
        Args:
            ax (Axes): Axes that already contains fill_between artists.
        """
        self.ax = ax

    def standard(self) -> Iterable[FillBetweenPolyCollection]:
        """Yield all fill_between area artists on the Axes.

        Yields:
            FillBetweenPolyCollection: Each fill_between collection discovered
            in ax.collections.
        """
        for area in self.ax.collections:
            if isinstance(area, FillBetweenPolyCollection):
                yield area

    def map_legend(
        self,
        property: dict[str, T],
    ) -> Iterable[tuple[FillBetweenPolyCollection, T]]:
        """Yield areas paired with values mapped by legend label.

        Args:
            property (dict[str, T]): Mapping from legend label text to a value.

        Yields:
            tuple[FillBetweenPolyCollection, T]: (area, value) pairs for areas
            whose legend label exists in the mapping.

        Notes:
            This method attempts to read a legend label from the private
            attribute "_legend_label". This is not a stable Matplotlib API.
        """
        for area in self.ax.collections:
            if isinstance(area, FillBetweenPolyCollection):
                legend_label = getattr(area, "_legend_label", None)
                if legend_label is not None:
                    prop = property.get(legend_label)
                    if prop is not None:
                        yield area, prop
