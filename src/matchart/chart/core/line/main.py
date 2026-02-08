"""Build line charts by wiring data preparation, rendering, and styling."""

from dataclasses import dataclass

import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matchart.data.core.main import DataContainer, DataProperties
from matchart.data.main import Data
from matchart.style.line.main import LineStyler

from .core.main import LineProperties, LineRenderer


@dataclass(frozen=True)
class LineContainer:
    """Bundle the objects produced when building a line chart.

    Attributes:
        ax (Axes): Target axes containing the rendered line artists.
        fig (Figure): Figure associated with the axes.
        data_container (DataContainer): Prepared/pivoted data and metadata
            used to render the lines.
        line_properties (LineProperties): Rendering configuration used by
            LineRenderer.
        line_styler (LineStyler): Styling facade bound to the rendered chart.
    """

    ax: Axes
    fig: Figure
    data_container: DataContainer
    line_properties: LineProperties
    line_styler: LineStyler


class LineFactory:
    """Orchestrate line chart modules."""

    def __init__(self, ax: Axes, fig: Figure) -> None:
        """
        Args:
            ax (Axes): Target axes that will receive line artists.
            fig (Figure): Figure associated with the axes.
        """
        self.ax = ax
        self.fig = fig

    def build(
        self,
        df: pd.DataFrame,
        data_properties: DataProperties,
        line_properties: LineProperties,
        running_total: bool,
    ) -> LineContainer:
        """Build a line chart and return a bundle of the created objects.

        This method prepares line chart data, renders lines onto the Axes, and
        constructs a LineStyler configured for follow-up styling.

        Args:
            df (pd.DataFrame): Source data used to build the chart.
            data_properties (DataProperties): Data configuration used by
                Data(...).line(...), including any legend/grouping metadata.
            line_properties (LineProperties): Rendering configuration used by
                LineRenderer.
            running_total (bool): Whether to compute a running total during
                data preparation (delegated to Data(df).line).

        Returns:
            LineContainer: Bundle containing the Axes/Figure plus the created
            DataContainer, LineProperties, and LineStyler.

        Notes:
            - This method mutates the provided Axes by adding line artists.
            - It does not return the Matplotlib artists directly; access them
              via the Axes (e.g., ax.lines).
        """
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
