import pandas as pd
import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractmethod
from matplotlib.axes import Axes


@dataclass(frozen=True)
class ClusteredBarData:
    """Encapsulates data model for the clustered bar chart."""

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
        """Creates ClusteredBarData from a pivot DataFrame."""

        tick_labels = pivot.index.astype(str).tolist()
        legend_labels = pivot.columns.tolist()
        legend_count = len(legend_labels)
        positions = np.arange(len(tick_labels))
        values = pivot.astype(float, errors="raise").to_numpy(float)

        total_space = bar_space * max(legend_count - 1, 0)
        available_width = cluster_width - total_space
        bar_width_adjusted = available_width / max(legend_count, 1)

        return cls(
            tick_labels=tick_labels,
            legend_labels=legend_labels,
            positions=positions,
            legend_count=legend_count,
            bar_width=bar_width_adjusted,
            bar_space=bar_space,
            values=values,
        )

    def compute_cluster_centers(self) -> np.ndarray:
        """Compute cluster centers positions."""

        total_cluster_width = self.bar_width * self.legend_count + self.bar_space * max(
            self.legend_count - 1, 0
        )
        return self.positions + total_cluster_width / 2 - self.bar_width / 2

    def compute_bar_position(self, bar_index: int) -> np.ndarray:
        """Compute position for a specific bar within clusters."""

        return self.positions + bar_index * (self.bar_width + self.bar_space)


@dataclass(frozen=True)
class ClusteredBarProperties:
    """Encapsulates properties for clustered bar drawing."""

    ax: Axes
    data: ClusteredBarData


class ClusteredBarDrawerABC(ABC):
    """Abstract base class for clustered bar types."""

    def __init__(self, properties: ClusteredBarProperties) -> None:
        self.properties = properties
        self.ax = properties.ax
        self.data = properties.data

    @abstractmethod
    def draw(self) -> None:
        """Draw clustered bars on the given axes."""
        ...

    @abstractmethod
    def set_ticks(self) -> None:
        """Set the ticks on the given axes."""
        ...


class ClusteredVerticalBarDrawer(ClusteredBarDrawerABC):
    """Draws vertical clustered bars."""

    def draw(self) -> None:
        for index, legend_label in enumerate(self.data.legend_labels):
            self.ax.bar(
                x=self.data.compute_bar_position(index),
                height=self.data.values[:, index],
                width=self.data.bar_width,
                label=str(legend_label),
            )

    def set_ticks(self) -> None:
        self.ax.set_xticks(self.data.compute_cluster_centers())
        self.ax.set_xticklabels(self.data.tick_labels)


class ClusteredHorizontalBarDrawer(ClusteredBarDrawerABC):
    """Draws horizontal clustered bars."""

    def draw(self) -> None:
        for index, legend_label in enumerate(self.data.legend_labels):
            self.ax.barh(
                y=self.data.compute_bar_position(index),
                width=self.data.values[:, index],
                height=self.data.bar_width,
                label=str(legend_label),
            )

    def set_ticks(self) -> None:
        self.ax.set_yticks(self.data.compute_cluster_centers())
        self.ax.set_yticklabels(self.data.tick_labels)


class ClusteredBarDrawerSelector:
    """Selects the appropriate clustered bar drawer orientation."""

    def __init__(self, properties: ClusteredBarProperties) -> None:
        self.properties = properties

    def get_drawer(self, horizontal: bool) -> ClusteredBarDrawerABC:
        """Get the appropriate clustered bar drawer."""

        if horizontal:
            return ClusteredHorizontalBarDrawer(properties=self.properties)
        return ClusteredVerticalBarDrawer(properties=self.properties)
