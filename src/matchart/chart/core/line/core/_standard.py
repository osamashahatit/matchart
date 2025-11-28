import pandas as pd
import numpy as np
from typing import Literal
from dataclasses import dataclass
from abc import ABC, abstractmethod
from matplotlib.axes import Axes


@dataclass(frozen=True)
class StandardSingleLineData:
    """Encapsulates data model for the standard line chart."""

    tick_labels: list[str]
    values: np.ndarray

    @classmethod
    def from_pivot(cls, pivot: pd.DataFrame) -> "StandardSingleLineData":
        """Creates StandardSingleLineData from a pivot DataFrame."""

        tick_labels = pivot.index.astype(str).tolist()
        values = pivot.iloc[:, 0].astype(float, errors="raise").to_numpy(float)
        return cls(tick_labels=tick_labels, values=values)


@dataclass(frozen=True)
class StandardMultiLineData:
    """Encapsulates data model for the standard multi-line chart."""

    tick_labels: list[str]
    legend_labels: list[str]
    pivot: pd.DataFrame

    @classmethod
    def from_pivot(cls, pivot: pd.DataFrame) -> "StandardMultiLineData":
        """Creates StandardMultiLineData from a pivot DataFrame."""

        tick_labels = pivot.index.astype(str).tolist()
        legend_labels = pivot.columns.tolist()
        return cls(tick_labels=tick_labels, legend_labels=legend_labels, pivot=pivot)

    def get_legend_value(self, legend_label: str) -> np.ndarray:
        """Get numeric value for a specific legend label."""

        return self.pivot[legend_label].astype(float, errors="raise").to_numpy(float)


@dataclass(frozen=True)
class StandardLineProperties:
    """Encapsulates properties for standard line drawing."""

    ax: Axes
    data: StandardSingleLineData | StandardMultiLineData
    width: float
    area: bool
    label: str | None


class StandardLineDrawerABC(ABC):
    """Abstract base class for standard line types."""

    def __init__(self, properties: StandardLineProperties) -> None:
        self.properties = properties
        self.ax = properties.ax
        self.data = properties.data

    @abstractmethod
    def draw(self) -> None:
        """Draw standard lines on a given axes."""
        ...


class StandardSingleLineDrawer(StandardLineDrawerABC):
    """Draws a standard line without legend."""

    def draw(self) -> None:
        self.data: StandardSingleLineData
        self.ax.plot(
            self.data.tick_labels,
            self.data.values,
            linewidth=self.properties.width,
            label=self.properties.label,
        )
        if self.properties.area:
            self.ax.fill_between(
                self.data.tick_labels,
                self.data.values,
                alpha=0.3,
            )


class StandardMultiLineDrawer(StandardLineDrawerABC):
    """Draws a standard line with legend."""

    def draw(self) -> None:
        self.data: StandardMultiLineData
        for label in self.data.legend_labels:
            value = self.data.get_legend_value(legend_label=label)
            self.ax.plot(
                self.data.tick_labels,
                value,
                linewidth=self.properties.width,
                label=str(label),
            )
            if self.properties.area:
                self.ax.fill_between(
                    self.data.tick_labels,
                    value,
                    alpha=0.3,
                )


class StandardLineDrawerSelector:
    """Selects the appropriate standard line drawer."""

    def __init__(self, properties: StandardLineProperties) -> None:
        self.properties = properties

    def get_drawer(self, select: Literal["single", "multi"]) -> StandardLineDrawerABC:
        """Get the appropriate standard line drawer."""

        if select == "multi":
            return StandardMultiLineDrawer(properties=self.properties)
        return StandardSingleLineDrawer(properties=self.properties)
