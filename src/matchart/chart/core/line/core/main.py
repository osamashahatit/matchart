import pandas as pd
from dataclasses import dataclass
from abc import ABC, abstractmethod
from matplotlib.axes import Axes

from ._standard import (
    StandardLineProperties,
    StandardSingleLineData,
    StandardMultiLineData,
    StandardLineDrawerSelector,
)


@dataclass(frozen=True)
class LineProperties:
    """Encapsulates properties for line chart."""

    width: float
    area: bool
    label: str | None


class LineDrawerABC(ABC):
    """Abstract base class for line chart drawers."""

    def __init__(
        self,
        ax: Axes,
        pivot: pd.DataFrame,
        properties: LineProperties,
    ) -> None:
        self.ax = ax
        self.pivot = pivot
        self.properties = properties

    @abstractmethod
    def draw(self) -> None:
        """Draw the chart on the given axes."""
        ...


class StandardLineDrawer(LineDrawerABC):
    """Draw a standard line chart."""

    def draw(self) -> None:
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
        drawer_selector = StandardLineDrawerSelector(properties=properties)
        drawer = drawer_selector.get_drawer(select=select)
        drawer.draw()


class LineRenderer:
    """Main facade for rendering line charts."""

    def __init__(
        self,
        ax: Axes,
        pivot: pd.DataFrame,
        properties: LineProperties,
    ) -> None:
        self.ax = ax
        self.pivot = pivot
        self.properties = properties

    def render(self) -> None:
        """Render the line chart on the given axes."""

        StandardLineDrawer(
            ax=self.ax,
            pivot=self.pivot,
            properties=self.properties,
        ).draw()
