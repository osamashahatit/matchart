"""Compute and draw clustered bar charts from pivoted data.

Matplotlib's bar/barh primitives are low-level and require manual
calculation of bar positions when rendering clustered bars (multiple
series per category). This module encapsulates the geometry and drawing
responsibilities for clustered bar charts so higher-level chart code can
supply a pivoted DataFrame and focus on styling, labels, and layout.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import pandas as pd
from matplotlib.axes import Axes


@dataclass(frozen=True)
class ClusteredBarData:
    """Store geometry and values required to render clustered bars.

    Attributes:
        tick_labels (list[str]): Category labels derived from pivot.index.
        legend_labels (list[str]): Series labels derived from pivot.columns.
        legend_count (int): Number of legend series (len(legend_labels)).
        positions (np.ndarray): Base positions for each category.
        values (np.ndarray): Values array of shape (n_categories, n_series).
        bar_width (float): Computed bar width for each series in a cluster.
        bar_space (float): Spacing between bars within a cluster.
    """

    tick_labels: list[str]
    legend_labels: list[str]
    legend_count: int
    positions: np.ndarray
    values: np.ndarray
    bar_width: float
    bar_space: float

    @classmethod
    def from_pivot(
        cls,
        pivot: pd.DataFrame,
        cluster_width: float,
        bar_space: float,
    ) -> "ClusteredBarData":
        """Create clustered-bar geometry from a pivot DataFrame.

        Args:
            pivot (pd.DataFrame): Pivoted data where index represents
                categories and columns represent legend series.
            cluster_width (float): Total width allocated to the full
                cluster (all series) for each category.
            bar_space (float): Spacing between bars within each cluster.

        Returns:
            ClusteredBarData: Derived geometry and values.

        Raises:
            ValueError: If cluster_width <= 0 or bar_space is invalid.
        """

        # Validate parameters
        if cluster_width <= 0:
            raise ValueError(f"cluster_width must be positive, got {cluster_width}")

        if bar_space < 0:
            raise ValueError(f"bar_space must be non-negative, got {bar_space}")

        legend_count = len(pivot.columns)

        # Calculate minimum space needed
        min_space_needed = bar_space * max(legend_count - 1, 0)

        if bar_space >= cluster_width:
            raise ValueError(
                f"bar_space ({bar_space}) must be less than cluster_width "
                f"({cluster_width})"
            )

        if min_space_needed >= cluster_width:
            raise ValueError(
                f"cluster_width ({cluster_width}) is too small for {legend_count} "
                f"series with bar_space={bar_space}. Minimum required: "
                f"{min_space_needed + 0.1:.2f}"
            )

        tick_labels = pivot.index.astype(str).tolist()
        legend_labels = pivot.columns.tolist()

        # Use unit-spaced positions for category groups on the categorical axis.
        positions = np.arange(len(tick_labels))

        # Ensure values are numeric for Matplotlib bar plotting.
        values = pivot.astype(float, errors="raise").to_numpy(float)

        # Compute bar width by subtracting intra-cluster spacing from the
        # available cluster width.
        total_space = bar_space * max(legend_count - 1, 0)
        available_width = cluster_width - total_space
        bar_width = available_width / max(legend_count, 1)

        # bar_width should be positive
        if bar_width <= 0:
            raise ValueError(
                f"Computed bar_width is non-positive ({bar_width:.4f}). "
                f"Check cluster_width and bar_space values."
            )

        return cls(
            tick_labels=tick_labels,
            legend_labels=legend_labels,
            positions=positions,
            legend_count=legend_count,
            bar_width=bar_width,
            bar_space=bar_space,
            values=values,
        )

    def compute_cluster_centers(self) -> np.ndarray:
        """Compute tick positions at the center of each cluster.

        Returns:
            np.ndarray: Center positions for clusters along the categorical axis.
        """
        total_cluster_width = self.bar_width * self.legend_count + self.bar_space * max(
            self.legend_count - 1, 0
        )
        return self.positions + total_cluster_width / 2 - self.bar_width / 2

    def compute_bar_position(self, bar_index: int) -> np.ndarray:
        """Compute bar positions for a given series within each cluster.

        Args:
            bar_index (int): Zero-based index of the series within the
                legend series list.

        Returns:
            np.ndarray: Positions for the specified series bars.
        """
        return self.positions + bar_index * (self.bar_width + self.bar_space)


@dataclass(frozen=True)
class ClusteredBarProperties:
    """Bundle Axes and properties required to draw clustered bars.

    Attributes:
        ax (Axes): Target axes to draw on (no figure creation).
        data (ClusteredBarData): Precomputed clustered bar geometry/values.
    """

    ax: Axes
    data: ClusteredBarData


class ClusteredBarDrawerBase(ABC):
    """Define the interface for clustered bar drawers."""

    def __init__(self, properties: ClusteredBarProperties) -> None:
        """
        Args:
            properties (ClusteredBarProperties): Drawing context including
                target axes and prepared clustered-bar data.
        """
        self.properties = properties

    @abstractmethod
    def draw(self) -> None:
        """Draw clustered bars on the provided axes."""
        ...

    @abstractmethod
    def set_ticks(self) -> None:
        """Set tick positions and labels on the categorical axis."""
        ...


class ClusteredVerticalBarDrawer(ClusteredBarDrawerBase):
    """Draw vertical clustered bars using Axes.bar()."""

    def draw(self) -> None:
        """Draw vertical clustered bars.

        Notes:
            This draws bar artists but does not configure legends or axis
            labels beyond bar labels.
        """
        for index, legend_label in enumerate(self.properties.data.legend_labels):
            self.properties.ax.bar(  # type:ignore
                x=self.properties.data.compute_bar_position(index),
                height=self.properties.data.values[:, index],
                width=self.properties.data.bar_width,
                label=str(legend_label),
            )

    def set_ticks(self) -> None:
        """Set x-axis ticks/labels at cluster centers."""
        self.properties.ax.set_xticks(self.properties.data.compute_cluster_centers())  # type:ignore
        self.properties.ax.set_xticklabels(self.properties.data.tick_labels)  # type:ignore


class ClusteredHorizontalBarDrawer(ClusteredBarDrawerBase):
    """Draw horizontal clustered bars using Axes.barh()."""

    def draw(self) -> None:
        """Draw horizontal clustered bars.

        Notes:
            This draws bar artists but does not configure legends or axis
            labels beyond bar labels.
        """
        for index, legend_label in enumerate(self.properties.data.legend_labels):
            self.properties.ax.barh(  # type:ignore
                y=self.properties.data.compute_bar_position(index),
                width=self.properties.data.values[:, index],
                height=self.properties.data.bar_width,
                label=str(legend_label),
            )

    def set_ticks(self) -> None:
        """Set y-axis ticks/labels at cluster centers."""
        self.properties.ax.set_yticks(self.properties.data.compute_cluster_centers())  # type:ignore
        self.properties.ax.set_yticklabels(self.properties.data.tick_labels)  # type:ignore


class ClusteredBarDrawerSelector:
    """Select a clustered bar drawer based on orientation."""

    def __init__(self, properties: ClusteredBarProperties) -> None:
        """
        Args:
            properties (ClusteredBarProperties): Drawing context to pass to
                the selected drawer.
        """
        self.properties = properties

    def select(self, horizontal: bool) -> ClusteredBarDrawerBase:
        """Return the appropriate clustered bar drawer.

        Args:
            horizontal (bool): If True, select a horizontal drawer; else
                select a vertical drawer.

        Returns:
            ClusteredBarDrawerBase: Drawer instance for the chosen orientation.
        """
        if horizontal:
            return ClusteredHorizontalBarDrawer(properties=self.properties)
        return ClusteredVerticalBarDrawer(properties=self.properties)
