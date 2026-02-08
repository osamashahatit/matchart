"""Compute and draw standard (single-series) bar charts from pivoted data.

Many bar charts are single-series (no legend grouping) and can be drawn
directly from a simple pivot table. Even so, chart code often repeats
the same steps: extracting tick labels, converting values to floats, and
choosing between vertical vs. horizontal orientation. This module
centralizes those responsibilities behind a small data model and drawer
classes, keeping higher-level chart builders focused on styling and
layout rather than Matplotlib mechanics.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import pandas as pd
from matplotlib.axes import Axes


@dataclass(frozen=True)
class StandardBarData:
    """Store labels and values required to render a standard bar chart.

    Attributes:
        tick_labels (list[str]): Category labels derived from pivot.index.
        values (np.ndarray): Values for the single series, aligned to
            tick_labels order.
    """

    tick_labels: list[str]
    values: np.ndarray

    @classmethod
    def from_pivot(cls, pivot: pd.DataFrame) -> "StandardBarData":
        """Create standard-bar data from a single-series pivot DataFrame.

        Args:
            pivot (pd.DataFrame): Pivoted data with exactly ONE column.
                Index represents categories, single column contains values.

        Returns:
            StandardBarData: Data model with tick labels and values.

        Raises:
            ValueError: If pivot doesn't have exactly one column.
        """
        if pivot.shape[1] != 1:
            raise ValueError(
                f"Standard bar charts (no legend) require exactly one column, "
                f"but pivot has {pivot.shape[1]} columns. "
                f"For multi-series data, select a different bar chart type "
                f"or pass a single-column pivot."
            )

        if len(pivot) == 0:
            raise ValueError(
                "Cannot create bar chart from empty pivot (no categories)."
            )

        tick_labels = pivot.index.astype(str).tolist()
        values = pivot.iloc[:, 0].astype(float, errors="raise").to_numpy(float)
        return cls(tick_labels=tick_labels, values=values)


@dataclass(frozen=True)
class StandardBarProperties:
    """Bundle Axes and properties required to draw standard bars.

    Attributes:
        ax (Axes): Target axes to draw on (no figure creation).
        data (StandardBarData): Prepared standard-bar data model.
        width (float): Bar thickness (width for vertical, height for horizontal).
        label (str | None): Optional label used for legends.
    """

    ax: Axes
    data: StandardBarData
    width: float
    label: str | None


class StandardBarDrawerBase(ABC):
    """Define the interface for standard bar drawers."""

    def __init__(self, properties: StandardBarProperties) -> None:
        """
        Args:
            properties (StandardBarProperties): Drawing context including
                target axes and standard-bar properties.
        """
        self.properties = properties

    @abstractmethod
    def draw(self) -> None:
        """Draw standard bars on the provided axes."""
        ...


class StandardVerticalBarDrawer(StandardBarDrawerBase):
    """Draw vertical standard bars using Axes.bar()."""

    def draw(self) -> None:
        """Draw vertical standard bars."""
        self.properties.ax.bar(  # type:ignore
            x=self.properties.data.tick_labels,
            height=self.properties.data.values,
            width=self.properties.width,
            label=self.properties.label,
        )


class StandardHorizontalBarDrawer(StandardBarDrawerBase):
    """Draw horizontal standard bars using Axes.barh()."""

    def draw(self) -> None:
        """Draw horizontal standard bars."""
        self.properties.ax.barh(  # type:ignore
            y=self.properties.data.tick_labels,
            width=self.properties.data.values,
            height=self.properties.width,
            label=self.properties.label,
        )


class StandardBarDrawerSelector:
    """Select a standard bar drawer based on orientation."""

    def __init__(self, properties: StandardBarProperties) -> None:
        """
        Args:
            properties (StandardBarProperties): Drawing context to pass to
                the selected drawer.
        """
        self.properties = properties

    def select(self, horizontal: bool) -> StandardBarDrawerBase:
        """Return the appropriate standard bar drawer.

        Args:
            horizontal (bool): If True, select a horizontal drawer; else
                select a vertical drawer.

        Returns:
            StandardBarDrawerBase: Drawer instance for the chosen orientation.
        """
        if horizontal:
            return StandardHorizontalBarDrawer(properties=self.properties)
        return StandardVerticalBarDrawer(properties=self.properties)
