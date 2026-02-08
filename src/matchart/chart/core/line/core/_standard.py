"""Compute and draw standard single- and multi-series line charts.

Matplotlib line charts are straightforward for a single series, but
multi-series lines require consistent extraction of legend series from a
pivoted DataFrame and a predictable way to apply common options (line
width, optional filled area). This module provides small data models and
drawer classes that render either a single line (no legend dimension) or
multiple lines (legend dimension) onto a provided Axes, keeping
higher-level chart code focused on chart configuration and styling.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, cast

import numpy as np
import pandas as pd
from matplotlib.axes import Axes


@dataclass(frozen=True)
class StandardSingleLineData:
    """Store tick labels and values required to render a single line.

    Attributes:
        tick_labels (list[str]): X-axis labels derived from pivot.index.
        values (np.ndarray): Y values for the single series, aligned to
            tick_labels order.
    """

    tick_labels: list[str]
    values: np.ndarray

    @classmethod
    def from_pivot(cls, pivot: pd.DataFrame) -> "StandardSingleLineData":
        """Create single-line data from a pivot DataFrame.

        Args:
            pivot (pd.DataFrame): Pivoted data where index represents
                x-axis categories and the first column contains values.

        Returns:
            StandardSingleLineData: Data model with tick labels and values.
        Raises:
            ValueError: If pivot doesn't have exactly one column.
        """
        if pivot.shape[1] != 1:
            raise ValueError(
                f"Single-line charts require exactly one series, but pivot "
                f"has {pivot.shape[1]} columns. "
                f"For multi-series data, use StandardMultiLineData.from_pivot() "
                f"or pass a single-column pivot."
            )

        if len(pivot) == 0:
            raise ValueError(
                "Cannot create line chart from empty pivot (no data points)."
            )

        tick_labels = pivot.index.astype(str).tolist()
        values = pivot.iloc[:, 0].astype(float, errors="raise").to_numpy(float)
        return cls(tick_labels=tick_labels, values=values)


@dataclass(frozen=True)
class StandardMultiLineData:
    """Store labels and pivot data required to render multiple lines.

    Attributes:
        tick_labels (list[str]): X-axis labels derived from pivot.index.
        legend_labels (list[str]): Series labels derived from pivot.columns.
        pivot (pd.DataFrame): Pivoted data used to retrieve series values.
    """

    tick_labels: list[str]
    legend_labels: list[str]
    pivot: pd.DataFrame

    @classmethod
    def from_pivot(cls, pivot: pd.DataFrame) -> "StandardMultiLineData":
        """Create multi-line data from a pivot DataFrame.

        Args:
            pivot (pd.DataFrame): Pivoted data where index represents
                x-axis categories and columns represent legend series.

        Returns:
            StandardMultiLineData: Data model with labels and pivot reference.
        """
        tick_labels = pivot.index.astype(str).tolist()
        legend_labels = pivot.columns.tolist()
        return cls(tick_labels=tick_labels, legend_labels=legend_labels, pivot=pivot)

    def get_legend_values(self, legend_label: str) -> np.ndarray:
        """Return a legend series as a float numpy array.

        Args:
            legend_label (str): Column label in the pivot DataFrame.

        Returns:
            np.ndarray: Float values for the specified series, aligned to
            tick_labels order.
        """
        return self.pivot[legend_label].astype(float, errors="raise").to_numpy(float)


@dataclass(frozen=True)
class StandardLineProperties:
    """Bundle Axes and properties required to draw standard lines.

    Attributes:
        ax (Axes): Target axes to draw on (no figure creation).
        data (StandardSingleLineData | StandardMultiLineData): Prepared
            line-chart data model for the chosen drawer.
        width (float): Line width passed to Axes.plot.
        area (bool): If True, fill the area under each line.
        label (str | None): Optional label used for the single-line case.
    """

    ax: Axes
    data: StandardSingleLineData | StandardMultiLineData
    width: float
    area: bool
    label: str | None


class StandardLineDrawerBase(ABC):
    """Define the interface for standard line drawers."""

    def __init__(self, properties: StandardLineProperties) -> None:
        """
        Args:
            properties (StandardLineProperties): Drawing context including
                target axes and line rendering configuration.
        """
        self.properties = properties

    @abstractmethod
    def draw(self) -> None:
        """Draw the line chart on the provided axes."""
        ...


class StandardSingleLineDrawer(StandardLineDrawerBase):
    """Draw a single-series line chart using Axes.plot()."""

    def draw(self) -> None:
        """Draw a single line and optional area fill."""
        data = cast(StandardSingleLineData, self.properties.data)
        self.properties.ax.plot(  # type:ignore
            data.tick_labels,
            data.values,
            linewidth=self.properties.width,
            label=self.properties.label,
        )

        if self.properties.area:
            self.properties.ax.fill_between(  # type:ignore
                data.tick_labels,
                data.values,
                alpha=0.1,
            )


class StandardMultiLineDrawer(StandardLineDrawerBase):
    """Draw a multi-series line chart (one line per pivot column)."""

    def draw(self) -> None:
        """Draw multiple lines and optional area fills."""
        data = cast(StandardMultiLineData, self.properties.data)
        for label in data.legend_labels:
            value = data.get_legend_values(legend_label=label)
            self.properties.ax.plot(  # type:ignore
                data.tick_labels,
                value,
                linewidth=self.properties.width,
                label=str(label),
            )

            if self.properties.area:
                area = self.properties.ax.fill_between(  # type:ignore
                    data.tick_labels,
                    value,
                    alpha=0.1,
                )
                # Downstream legend handling may rely on this label marker.
                setattr(area, "_legend_label", str(label))


class StandardLineDrawerSelector:
    """Select a standard line drawer for single vs. multi-series pivots."""

    def __init__(self, properties: StandardLineProperties) -> None:
        """
        Args:
            properties (StandardLineProperties): Drawing context to pass to
                the selected drawer.
        """
        self.properties = properties

    def select(self, select: Literal["single", "multi"]) -> StandardLineDrawerBase:
        """Return the appropriate standard line drawer.

        Args:
            select (Literal["single", "multi"]): Which variant to draw.

        Returns:
            StandardLineDrawerBase: Drawer instance for the chosen variant.
        """
        if select == "multi":
            return StandardMultiLineDrawer(properties=self.properties)
        return StandardSingleLineDrawer(properties=self.properties)
