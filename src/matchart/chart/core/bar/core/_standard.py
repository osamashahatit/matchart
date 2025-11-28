import pandas as pd
import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractmethod
from matplotlib.axes import Axes


@dataclass(frozen=True)
class StandardBarData:
    """Encapsulates data model for the standard bar chart."""

    tick_labels: list[str]
    values: np.ndarray

    @classmethod
    def from_pivot(cls, pivot: pd.DataFrame) -> "StandardBarData":
        """Creates StandardBarData from a pivot DataFrame."""

        tick_labels = pivot.index.astype(str).tolist()
        values = pivot.iloc[:, 0].astype(float, errors="raise").to_numpy(float)
        return cls(tick_labels=tick_labels, values=values)


@dataclass(frozen=True)
class StandardBarProperties:
    """Encapsulates properties for standard bar drawing."""

    ax: Axes
    data: StandardBarData
    width: float
    label: str | None


class StandardBarDrawerABC(ABC):
    """Abstract base class for standard bar types."""

    def __init__(self, properties: StandardBarProperties) -> None:
        self.properties = properties
        self.ax = properties.ax
        self.data = properties.data

    @abstractmethod
    def draw(self) -> None:
        """Draw standard bars on a given axes."""
        ...


class StandardVerticalBarDrawer(StandardBarDrawerABC):
    """Draws vertical standard bars."""

    def draw(self) -> None:
        self.ax.bar(
            x=self.data.tick_labels,
            height=self.data.values,
            width=self.properties.width,
            label=self.properties.label,
        )


class StandardHorizontalBarDrawer(StandardBarDrawerABC):
    """Draws horizontal standard bars."""

    def draw(self) -> None:
        self.ax.barh(
            y=self.data.tick_labels,
            width=self.data.values,
            height=self.properties.width,
            label=self.properties.label,
        )


class StandardBarDrawerSelector:
    """Selects the appropriate standard bar drawer orientation."""

    def __init__(self, properties: StandardBarProperties) -> None:
        self.properties = properties

    def get_drawer(self, horizontal: bool) -> StandardBarDrawerABC:
        """Get the appropriate stacked bar drawer."""

        if horizontal:
            return StandardHorizontalBarDrawer(properties=self.properties)
        return StandardVerticalBarDrawer(properties=self.properties)
