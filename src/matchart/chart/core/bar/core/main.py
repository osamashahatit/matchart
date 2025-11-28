import pandas as pd
from typing import Literal
from dataclasses import dataclass
from abc import ABC, abstractmethod
from matplotlib.axes import Axes

from ._clustered import (
    ClusteredBarData,
    ClusteredBarProperties,
    ClusteredBarDrawerSelector,
)
from ._stacked import (
    StackedBarData,
    StackedBarProperties,
    StackedBarDrawerSelector,
)
from ._standard import (
    StandardBarData,
    StandardBarProperties,
    StandardBarDrawerSelector,
)

type BarType = Literal["clustered", "stacked", "standard"]


@dataclass(frozen=True)
class BarProperties:
    """Encapsulates properties for bar chart."""

    type: BarType
    width: float
    space: float
    switch_axis: bool
    label: str | None


class BarDrawerABC(ABC):
    """Abstract base class for bar chart drawers."""

    def __init__(
        self,
        ax: Axes,
        pivot: pd.DataFrame,
        properties: BarProperties,
    ) -> None:
        self.ax = ax
        self.pivot = pivot
        self.properties = properties

    @abstractmethod
    def draw(self) -> None:
        """Draw the chart on the given axes."""
        ...


class StandardBarDrawer(BarDrawerABC):
    """Draw a standard bar chart."""

    def draw(self) -> None:
        data = StandardBarData.from_pivot(pivot=self.pivot)
        properties = StandardBarProperties(
            ax=self.ax,
            data=data,
            width=self.properties.width,
            label=self.properties.label,
        )
        drawer_selector = StandardBarDrawerSelector(properties=properties)
        drawer = drawer_selector.get_drawer(horizontal=self.properties.switch_axis)
        drawer.draw()


class StackedBarDrawer(BarDrawerABC):
    """Draw a stacked bar chart."""

    def draw(self) -> None:
        data = StackedBarData.from_pivot(pivot=self.pivot)
        properties = StackedBarProperties(
            ax=self.ax,
            data=data,
            width=self.properties.width,
            space=self.properties.space,
        )
        drawer_selector = StackedBarDrawerSelector(properties=properties)
        drawer = drawer_selector.get_drawer(horizontal=self.properties.switch_axis)
        drawer.draw()


class ClusteredBarDrawer(BarDrawerABC):
    """Draw a clustered bar chart."""

    def draw(self) -> None:
        data = ClusteredBarData.from_pivot(
            pivot=self.pivot,
            cluster_width=self.properties.width,
            bar_space=self.properties.space,
        )
        properties = ClusteredBarProperties(ax=self.ax, data=data)
        drawer_selector = ClusteredBarDrawerSelector(properties=properties)
        drawer = drawer_selector.get_drawer(horizontal=self.properties.switch_axis)
        drawer.draw()
        drawer.set_ticks()


class BarDrawerSelector:
    """Select the appropriate bar drawer based on bar type."""

    def __init__(
        self,
        ax: Axes,
        pivot: pd.DataFrame,
        properties: BarProperties,
    ) -> None:
        self.ax = ax
        self.pivot = pivot
        self.properties = properties

    def create(self) -> BarDrawerABC:
        """Create the appropriate bar drawer instance."""

        column_count = len(self.pivot.columns)
        if column_count <= 1:
            return StandardBarDrawer(
                ax=self.ax,
                pivot=self.pivot,
                properties=self.properties,
            )
        if self.properties.type == "stacked":
            return StackedBarDrawer(
                ax=self.ax,
                pivot=self.pivot,
                properties=self.properties,
            )
        if self.properties.type == "clustered":
            return ClusteredBarDrawer(
                ax=self.ax,
                pivot=self.pivot,
                properties=self.properties,
            )
        raise ValueError("Unsupported bar type")


class BarRenderer:
    """Main facade for rendering bar charts."""

    def __init__(
        self,
        ax: Axes,
        pivot: pd.DataFrame,
        properties: BarProperties,
    ) -> None:
        self.ax = ax
        self.pivot = pivot
        self.properties = properties

    def render(self) -> None:
        """Render the bar chart on the given axes."""

        BarDrawerSelector(
            ax=self.ax,
            pivot=self.pivot,
            properties=self.properties,
        ).create().draw()
