"""Render line charts by selecting single- vs. multi-series drawers.

Line charts can represent either a single series (no legend dimension)
or multiple series (one line per legend category). While the low-level
line drawing is handled by the standard line drawer module, chart code
benefits from a small orchestration layer that decides which variant to
render based on the pivoted input shape. This module provides that
selection logic and exposes a simple renderer facade that draws onto a
provided Matplotlib Axes.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd
from matplotlib.axes import Axes

from ._standard import (
    StandardLineDrawerSelector,
    StandardLineProperties,
    StandardMultiLineData,
    StandardSingleLineData,
)


@dataclass(frozen=True)
class LineProperties:
    """Store configuration for line chart rendering.

    Attributes:
        width (float): Line width passed to Axes.plot by the drawer.
        area (bool): If True, fill the area under the line(s).
        label (str | None): Optional label used for the single-line case.
            For multi-line charts, pivot column labels are used instead.
    """

    width: float
    area: bool
    label: str | None


class LineDrawerBase(ABC):
    """Define the interface for line chart drawers."""

    def __init__(
        self,
        ax: Axes,
        pivot: pd.DataFrame,
        properties: LineProperties,
    ) -> None:
        """
        Args:
            ax (Axes): Target axes to draw on (no figure creation).
            pivot (pd.DataFrame): Pivoted data used for rendering.
            properties (LineProperties): Line rendering configuration.
        """
        self.ax = ax
        self.pivot = pivot
        self.properties = properties

    @abstractmethod
    def draw(self) -> None:
        """Draw the line chart on the provided axes."""
        ...


class StandardLineDrawer(LineDrawerBase):
    """Draw a standard line chart (single or multi-series)."""

    def draw(self) -> None:
        """Render either a single-series or multi-series line chart."""
        column_count = len(self.pivot.columns)

        if column_count <= 1:
            select = "single"
            data = StandardSingleLineData.from_pivot(pivot=self.pivot)
        else:
            select = "multi"
            data = StandardMultiLineData.from_pivot(pivot=self.pivot)

        properties = StandardLineProperties(
            ax=self.ax,
            data=data,
            width=self.properties.width,
            label=self.properties.label,
            area=self.properties.area,
        )

        drawer = StandardLineDrawerSelector(properties=properties).select(select=select)
        drawer.draw()


class LineRenderer:
    """Render a line chart onto a provided Matplotlib Axes."""

    def __init__(
        self,
        ax: Axes,
        pivot: pd.DataFrame,
        properties: LineProperties,
    ) -> None:
        """
        Args:
            ax (Axes): Target axes to draw on (no figure creation).
            pivot (pd.DataFrame): Pivoted data to render.
            properties (LineProperties): Line rendering configuration.
        """
        self.ax = ax
        self.pivot = pivot
        self.properties = properties

    def render(self) -> None:
        """Render the line chart onto the configured axes."""
        StandardLineDrawer(
            ax=self.ax,
            pivot=self.pivot,
            properties=self.properties,
        ).draw()
