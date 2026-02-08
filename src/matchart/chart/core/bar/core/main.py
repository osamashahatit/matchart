"""Render bar charts based on the selected bar type.

Bar charts share a common high-level interface (draw bars on an Axes),
but their implementation differs based on whether the data has one
series (standard) or multiple series rendered as stacked or clustered
bars. This module provides a small orchestration layer that chooses the
correct bar drawer based on the pivoted input data and user-selected bar
type, delegating the drawing details to specialized modules.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

import pandas as pd
from matplotlib.axes import Axes

from ._clustered import (
    ClusteredBarData,
    ClusteredBarDrawerSelector,
    ClusteredBarProperties,
)
from ._stacked import (
    StackedBarData,
    StackedBarDrawerSelector,
    StackedBarProperties,
)
from ._standard import (
    StandardBarData,
    StandardBarDrawerSelector,
    StandardBarProperties,
)

type BarType = Literal["clustered", "stacked", "standard"]


@dataclass(frozen=True)
class BarProperties:
    """Store configuration for bar chart rendering.

    Attributes:
        bar_type (BarType): Bar chart variant to render.
        width (float): Bar thickness (or cluster width for clustered bars).
        space (float): Spacing between bars (used by clustered/stacked bars).
        switch_axis (bool): If True, draw horizontally; otherwise vertically.
        label (str | None): Optional label used for standard bar legends.
    """

    bar_type: BarType
    width: float
    space: float
    switch_axis: bool
    label: str | None


class BarDrawerBase(ABC):
    """Define the interface for bar chart drawers."""

    def __init__(
        self,
        ax: Axes,
        pivot: pd.DataFrame,
        properties: BarProperties,
    ) -> None:
        """
        Args:
            ax (Axes): Target axes to draw on.
            pivot (pd.DataFrame): Pivoted data used for rendering.
            properties (BarProperties): Bar rendering configuration.
        """
        self.ax = ax
        self.pivot = pivot
        self.properties = properties

    @abstractmethod
    def draw(self) -> None:
        """Draw the bar chart on the provided axes."""
        ...


class StandardBarDrawer(BarDrawerBase):
    """Draw a standard (single-series) bar chart."""

    def draw(self) -> None:
        """Render a standard bar chart using the standard drawer module."""
        data = StandardBarData.from_pivot(pivot=self.pivot)
        properties = StandardBarProperties(
            ax=self.ax,
            data=data,
            width=self.properties.width,
            label=self.properties.label,
        )
        drawer = StandardBarDrawerSelector(properties=properties).select(
            horizontal=self.properties.switch_axis
        )
        drawer.draw()


class StackedBarDrawer(BarDrawerBase):
    """Draw a stacked (multi-series) bar chart."""

    def draw(self) -> None:
        """Render a stacked bar chart using the stacked drawer module."""
        data = StackedBarData.from_pivot(pivot=self.pivot)
        properties = StackedBarProperties(
            ax=self.ax,
            data=data,
            width=self.properties.width,
            space=self.properties.space,
        )
        drawer = StackedBarDrawerSelector(properties=properties).select(
            horizontal=self.properties.switch_axis
        )
        drawer.draw()


class ClusteredBarDrawer(BarDrawerBase):
    """Draw a clustered (multi-series) bar chart."""

    def draw(self) -> None:
        """Render a clustered bar chart using the clustered drawer module."""
        data = ClusteredBarData.from_pivot(
            pivot=self.pivot,
            cluster_width=self.properties.width,
            bar_space=self.properties.space,
        )
        properties = ClusteredBarProperties(ax=self.ax, data=data)

        drawer = ClusteredBarDrawerSelector(properties=properties).select(
            horizontal=self.properties.switch_axis
        )
        drawer.draw()
        drawer.set_ticks()


class BarDrawerSelector:
    """Select the appropriate bar drawer based on pivot shape and bar type."""

    def __init__(
        self,
        ax: Axes,
        pivot: pd.DataFrame,
        properties: BarProperties,
    ) -> None:
        """
        Args:
            ax (Axes): Target axes to draw on.
            pivot (pd.DataFrame): Pivoted data used for rendering.
            properties (BarProperties): Bar rendering configuration.
        """
        self.ax = ax
        self.pivot = pivot
        self.properties = properties

    def select(self) -> BarDrawerBase:
        """Select the correct bar drawer for the pivot and configuration.

        Selection logic:
            - Single-column pivots (≤1 column): Always use StandardBarDrawer,
                regardless of bar_type setting. Stacked/clustered require multiple series.
            - Multi-column pivots: Respect bar_type; reject "standard" with clear error.

        Returns:
            BarDrawerBase: Drawer instance appropriate for the pivot shape
            and requested bar type.

        Raises:
            ValueError: If bar_type is "standard" for multi-column pivots.
        """
        column_count = len(self.pivot.columns)

        # Standard bars are always selected for single-series pivots.
        if column_count <= 1:
            return StandardBarDrawer(
                ax=self.ax,
                pivot=self.pivot,
                properties=self.properties,
            )

        if self.properties.bar_type == "standard":
            raise ValueError(
                f"Bar type 'standard' requires a single-series pivot, "
                f"but pivot has {column_count} columns. "
                f"Use 'stacked' or 'clustered' for multi-series data."
            )

        if self.properties.bar_type == "stacked":
            return StackedBarDrawer(
                ax=self.ax,
                pivot=self.pivot,
                properties=self.properties,
            )

        if self.properties.bar_type == "clustered":
            return ClusteredBarDrawer(
                ax=self.ax,
                pivot=self.pivot,
                properties=self.properties,
            )

        raise ValueError(
            f"Unsupported bar type: {self.properties.bar_type}. "
            f"Expected 'standard', 'stacked', or 'clustered'."
        )


class BarRenderer:
    """Render a bar chart onto a provided Matplotlib Axes."""

    def __init__(
        self,
        ax: Axes,
        pivot: pd.DataFrame,
        properties: BarProperties,
    ) -> None:
        """
        Args:
            ax (Axes): Target axes to draw on.
            pivot (pd.DataFrame): Pivoted data to render.
            properties (BarProperties): Bar rendering configuration.
        """
        self.ax = ax
        self.pivot = pivot
        self.properties = properties

    def render(self) -> None:
        """Render the bar chart onto the configured axes."""
        BarDrawerSelector(
            ax=self.ax,
            pivot=self.pivot,
            properties=self.properties,
        ).select().draw()
