"""Build bar charts by wiring data preparation, rendering, and styling."""

from dataclasses import dataclass

import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matchart.data.core.main import DataContainer, DataProperties
from matchart.data.main import Data
from matchart.style.bar.main import BarStyler

from .core.main import BarProperties, BarRenderer


@dataclass(frozen=True)
class BarContainer:
    """Bundle the objects produced when building a bar chart.

    Attributes:
        ax (Axes): Target axes containing the rendered bar artists.
        fig (Figure): Figure associated with the axes.
        data_container (DataContainer): Prepared/pivoted data and metadata
            used to render the bars.
        bar_properties (BarProperties): Rendering configuration used by
            BarRenderer.
        bar_styler (BarStyler): Styling facade bound to the rendered chart.
    """

    ax: Axes
    fig: Figure
    data_container: DataContainer
    bar_properties: BarProperties
    bar_styler: BarStyler


class BarFactory:
    """Orchestrate bar chart modules."""

    def __init__(self, ax: Axes, fig: Figure) -> None:
        """
        Args:
            ax (Axes): Target axes that will receive bar artists.
            fig (Figure): Figure associated with the axes.
        """
        self.ax = ax
        self.fig = fig

    def build(
        self,
        df: pd.DataFrame,
        data_properties: DataProperties,
        bar_properties: BarProperties,
    ) -> BarContainer:
        """Build a bar chart and return a bundle of the created objects.

        This method prepares bar chart data, renders bars onto the Axes, and
        constructs a BarStyler configured for follow-up styling.

        Args:
            df (pd.DataFrame): Source data used to build the chart.
            data_properties (DataProperties): Data configuration used by
                Data(...).bar(...), including any legend/grouping metadata.
            bar_properties (BarProperties): Rendering configuration used by
                BarRenderer.

        Returns:
            BarContainer: Bundle containing the Axes/Figure plus the created
            DataContainer, BarProperties, and BarStyler.

        Notes:
            - This method mutates the provided Axes by adding bar artists.
            - It does not return the Matplotlib artists directly; access them
              via the Axes (e.g., ax.containers / ax.patches).
        """
        data_container = Data(df).bar(properties=data_properties)

        bar_styler = BarStyler(
            ax=self.ax,
            fig=self.fig,
            horizontal=bar_properties.switch_axis,
            legend=data_properties.legend,
        )

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
