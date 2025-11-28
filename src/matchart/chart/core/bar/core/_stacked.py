import pandas as pd
import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractmethod
from matplotlib.axes import Axes


@dataclass(frozen=True)
class StackedBarData:
    """Encapsulates data model for the stacked bar chart."""

    tick_labels: list[str]
    legend_labels: list[str]
    pivot: pd.DataFrame

    @classmethod
    def from_pivot(cls, pivot: pd.DataFrame) -> "StackedBarData":
        """Creates StackedBarData from a pivot DataFrame."""

        tick_labels = pivot.index.astype(str).tolist()
        legend_labels = pivot.columns.tolist()
        return cls(
            tick_labels=tick_labels,
            legend_labels=legend_labels,
            pivot=pivot,
        )

    def get_legend_value(self, legend_label: str) -> np.ndarray:
        """Get numeric value for a specific legend label."""

        return self.pivot[legend_label].astype(float, errors="raise").to_numpy(float)


@dataclass(frozen=True)
class StackedBarProperties:
    """Encapsulates properties for stacked bar drawing."""

    ax: Axes
    data: StackedBarData
    width: float
    space: float


class StackedBarDrawerABC(ABC):
    """Abstract base class for stacked bar types."""

    def __init__(self, properties: StackedBarProperties) -> None:
        self.properties = properties
        self.ax = properties.ax
        self.data = properties.data

    @abstractmethod
    def draw(self) -> None:
        """Draw stacked bars on a given axes."""
        ...


class StackedVerticalBarDrawer(StackedBarDrawerABC):
    """Draws vertical stacked bars."""

    def draw(self) -> None:
        positions = np.zeros(len(self.data.tick_labels))
        values = self.data.pivot.to_numpy(float)
        range = np.abs(values).sum(axis=1).max()
        space = self.properties.space * range
        for label in self.data.legend_labels:
            value = self.data.get_legend_value(legend_label=label)
            self.ax.bar(
                x=self.data.tick_labels,
                height=value,
                bottom=positions,
                width=self.properties.width,
                label=str(label),
            )
            positions += value + np.sign(value) * space


class StackedHorizontalBarDrawer(StackedBarDrawerABC):
    """Draws horizontal stacked bars."""

    def draw(self) -> None:
        positions = np.zeros(len(self.data.tick_labels))
        values = self.data.pivot.to_numpy(float)
        range = np.abs(values).sum(axis=1).max()
        space = self.properties.space * range
        for label in self.data.legend_labels:
            value = self.data.get_legend_value(legend_label=label)
            self.ax.barh(
                y=self.data.tick_labels,
                width=value,
                left=positions,
                height=self.properties.width,
                label=str(label),
            )
            positions += value + np.sign(value) * space


class StackedBarDrawerSelector:
    """Selects the appropriate stacked bar drawer orientation."""

    def __init__(self, properties: StackedBarProperties) -> None:
        self.properties = properties

    def get_drawer(self, horizontal: bool) -> StackedBarDrawerABC:
        """Get the appropriate stacked bar drawer."""

        if horizontal:
            return StackedHorizontalBarDrawer(properties=self.properties)
        return StackedVerticalBarDrawer(properties=self.properties)
