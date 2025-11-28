import pandas as pd
from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matchart.data.core.main import DataContainer, DataProperties
from matchart.data.main import Data
from matchart.style.bar.main import BarStyler

from .core.main import BarProperties, BarRenderer


@dataclass(frozen=True)
class BarContainer:

    ax: Axes
    fig: Figure
    data_container: DataContainer
    bar_properties: BarProperties
    bar_styler: BarStyler


class BarFactory:
    """Orchestrates bar chart modules."""

    def __init__(self, ax: Axes, fig: Figure) -> None:
        self.ax = ax
        self.fig = fig

    def build(
        self,
        df: pd.DataFrame,
        data_properties: DataProperties,
        bar_properties: BarProperties,
    ) -> BarContainer:
        """Build bar chart with properties."""

        data_container = Data(df).bar(properties=data_properties)

        bar_styler = BarStyler(ax=self.ax, fig=self.fig)

        BarRenderer(
            ax=self.ax,
            pivot=data_container.pivot,
            properties=bar_properties,
        ).render()

        return BarContainer(
            ax=self.ax,
            fig=self.fig,
            data_container=data_container,
            bar_properties=bar_properties,
            bar_styler=bar_styler,
        )
