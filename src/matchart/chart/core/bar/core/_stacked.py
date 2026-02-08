"""Compute and draw stacked bar charts from pivoted data.

Stacked bars in Matplotlib require tracking the running "bottom" (or
"left") baseline as each series is added, and spacing between stacked
segments can be tricky when negative values are present. This module
encapsulates the data access and drawing logic for stacked bar charts so
higher-level chart code can provide a pivoted DataFrame and focus on
styling, axes labels, and legends.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import pandas as pd
from matplotlib.axes import Axes


@dataclass(frozen=True)
class StackedBarData:
    """Store labels and pivot data required to render stacked bars.

    Attributes:
        tick_labels (list[str]): Category labels derived from pivot.index.
        legend_labels (list[str]): Series labels derived from pivot.columns.
        pivot (pd.DataFrame): Pivoted data used to retrieve series values.
    """

    tick_labels: list[str]
    legend_labels: list[str]
    pivot: pd.DataFrame

    @classmethod
    def from_pivot(cls, pivot: pd.DataFrame) -> "StackedBarData":
        """Create a stacked-bar data model from a pivot DataFrame.

        Args:
            pivot (pd.DataFrame): Pivoted data where index represents
                categories and columns represent legend series.

        Returns:
            StackedBarData: Data model with labels and pivot reference.
        """
        tick_labels = pivot.index.astype(str).tolist()
        legend_labels = pivot.columns.tolist()
        return cls(
            tick_labels=tick_labels,
            legend_labels=legend_labels,
            pivot=pivot,
        )

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
class StackedBarProperties:
    """Bundle Axes and properties required to draw stacked bars.

    Attributes:
        ax (Axes): Target axes to draw on (no figure creation).
        data (StackedBarData): Prepared stacked-bar data model.
        width (float): Bar thickness (width for vertical, height for horizontal).
        space (float): Spacing factor between stacked segments.
    """

    ax: Axes
    data: StackedBarData
    width: float
    space: float


class StackedBarDrawerBase(ABC):
    """Define the interface for stacked bar drawers."""

    def __init__(self, properties: StackedBarProperties) -> None:
        """
        Args:
            properties (StackedBarProperties): Drawing context including
                target axes and stacked-bar properties.
        """
        self.properties = properties

    @abstractmethod
    def draw(self) -> None:
        """Draw stacked bars on the provided axes."""
        ...


class StackedVerticalBarDrawer(StackedBarDrawerBase):
    """Draw vertical stacked bars using Axes.bar()."""

    def draw(self) -> None:
        """Draw vertical stacked bars.

        Notes:
            This maintains a running baseline per category and applies an
            additional signed spacing term between segments.
        """
        positions = np.zeros(len(self.properties.data.tick_labels))
        values = self.properties.data.pivot.to_numpy(float)

        # Scale spacing by the maximum absolute row total to keep spacing
        # proportional to the magnitude of each category stack.
        scale = np.abs(values).sum(axis=1).max()
        space = self.properties.space * scale

        for label in self.properties.data.legend_labels:
            value = self.properties.data.get_legend_values(legend_label=label)
            self.properties.ax.bar(  # type:ignore
                x=self.properties.data.tick_labels,
                height=value,
                bottom=positions,
                width=self.properties.width,
                label=str(label),
            )
            positions += value + np.sign(value) * space


class StackedHorizontalBarDrawer(StackedBarDrawerBase):
    """Draw horizontal stacked bars using Axes.barh()."""

    def draw(self) -> None:
        """Draw horizontal stacked bars.

        Notes:
            This maintains a running baseline per category and applies an
            additional signed spacing term between segments.
        """
        positions = np.zeros(len(self.properties.data.tick_labels))
        values = self.properties.data.pivot.to_numpy(float)

        # Scale spacing by the maximum absolute row total to keep spacing
        # proportional to the magnitude of each category stack.
        scale = np.abs(values).sum(axis=1).max()
        space = self.properties.space * scale

        for label in self.properties.data.legend_labels:
            value = self.properties.data.get_legend_values(legend_label=label)
            self.properties.ax.barh(  # type:ignore
                y=self.properties.data.tick_labels,
                width=value,
                left=positions,
                height=self.properties.width,
                label=str(label),
            )
            positions += value + np.sign(value) * space


class StackedBarDrawerSelector:
    """Select a stacked bar drawer based on orientation."""

    def __init__(self, properties: StackedBarProperties) -> None:
        """
        Args:
            properties (StackedBarProperties): Drawing context to pass to
                the selected drawer.
        """
        self.properties = properties

    def select(self, horizontal: bool) -> StackedBarDrawerBase:
        """Return the appropriate stacked bar drawer.

        Args:
            horizontal (bool): If True, select a horizontal drawer; else
                select a vertical drawer.

        Returns:
            StackedBarDrawerBase: Drawer instance for the chosen orientation.
        """
        if horizontal:
            return StackedHorizontalBarDrawer(properties=self.properties)
        return StackedVerticalBarDrawer(properties=self.properties)
