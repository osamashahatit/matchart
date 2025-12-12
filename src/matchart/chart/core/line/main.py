import pandas as pd
from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matchart.data.core.main import DataContainer, DataProperties
from matchart.data.main import Data
from matchart.style.line.main import LineStyler

from .core.main import LineProperties, LineRenderer


@dataclass(frozen=True)
class LineContainer:

    ax: Axes
    fig: Figure
    data_container: DataContainer
    line_properties: LineProperties
    line_styler: LineStyler


class LineFactory:
    """Orchestrates line chart modules."""

    def __init__(self, ax: Axes, fig: Figure) -> None:
        self.ax = ax
        self.fig = fig

    def build(
        self,
        df: pd.DataFrame,
        data_properties: DataProperties,
        line_properties: LineProperties,
        running_total: bool,
    ) -> LineContainer:
        """Build line chart with properties."""

        data_container = Data(df).line(
            properties=data_properties,
            running_total=running_total,
        )

        line_styler = LineStyler(
            ax=self.ax,
            fig=self.fig,
            legend=data_properties.legend,
        )

        LineRenderer(
            ax=self.ax,
            pivot=data_container.pivot,
            properties=line_properties,
        ).render()

        return LineContainer(
            ax=self.ax,
            fig=self.fig,
            data_container=data_container,
            line_properties=line_properties,
            line_styler=line_styler,
        )
