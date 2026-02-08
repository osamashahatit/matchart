"""Provide the main matchart entry point and chart construction facade."""

from dataclasses import dataclass

import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matchart.data.core._limit import LimitSpec
from matchart.data.core._sort import SortSpec
from matchart.data.core.main import DataContainer, DataProperties
from matchart.style.bar.main import BarStyler
from matchart.style.line.main import LineStyler

from .core.bar.core.main import BarProperties, BarType
from .core.bar.main import BarContainer, BarFactory
from .core.line.core.main import LineProperties
from .core.line.main import LineContainer, LineFactory


@dataclass
class BarChart:
    """Result wrapper for a built bar chart.

    Attributes:
        bar_container (BarContainer): Bundle produced by BarFactory.build().
    """

    bar_container: BarContainer

    @property
    def ax(self) -> Axes:
        """Return the Matplotlib Axes containing the bar artists."""
        return self.bar_container.ax

    @property
    def fig(self) -> Figure:
        """Return the Matplotlib Figure associated with the Axes."""
        return self.bar_container.fig

    @property
    def data(self) -> DataContainer:
        """Return the prepared data container used to render the chart."""
        return self.bar_container.data_container

    @property
    def props(self) -> BarProperties:
        """Return the bar rendering properties used by the renderer."""
        return self.bar_container.bar_properties

    @property
    def style(self) -> BarStyler:
        """Return the bar styling facade bound to this chart."""
        return self.bar_container.bar_styler


@dataclass
class LineChart:
    """Result wrapper for a built line chart.

    Attributes:
        line_container (LineContainer): Bundle produced by LineFactory.build().
    """

    line_container: LineContainer

    @property
    def ax(self) -> Axes:
        """Return the Matplotlib Axes containing the line artists."""
        return self.line_container.ax

    @property
    def fig(self) -> Figure:
        """Return the Matplotlib Figure associated with the Axes."""
        return self.line_container.fig

    @property
    def data(self) -> DataContainer:
        """Return the prepared data container used to render the chart."""
        return self.line_container.data_container

    @property
    def props(self) -> LineProperties:
        """Return the line rendering properties used by the renderer."""
        return self.line_container.line_properties

    @property
    def style(self) -> LineStyler:
        """Return the line styling facade bound to this chart."""
        return self.line_container.line_styler


class Chart:
    """Build matchart charts on an existing Matplotlib Axes/Figure.

    This is the main end-user entry point. It provides a simplified API that
    delegates to specialized factory/renderer modules for orchestration.
    """

    def __init__(self, ax: Axes, fig: Figure) -> None:
        """
        Args:
            ax (Axes): Target axes that will receive chart artists.
            fig (Figure): Figure associated with the axes.
        """
        self.ax = ax
        self.fig = fig

    def bar(
        self,
        df: pd.DataFrame,
        x_axis: str,
        y_axis: str,
        agg_func: str = "sum",
        type: BarType = "stacked",
        legend: str | None = None,
        width: float = 0.8,
        space: float = 0.0,
        limit: LimitSpec | None = None,
        sort_axis: SortSpec | None = None,
        sort_legend: SortSpec | None = None,
        switch_axis: bool = False,
        label: str | None = None,
    ) -> BarChart:
        """Create a bar chart from a DataFrame and return a result wrapper.

        Args:
            df (pd.DataFrame): Source DataFrame.
            x_axis (str): Column in `df` used for the x-axis categories.
            y_axis (str): Column in `df` used for the y-axis values.
            agg_func (str, optional): Aggregation function applied to `y_axis`.
                 Defaults to "sum".
            type ("clustered", "stacked", "standard", optional):
                Bar layout variant.
            legend (str | None, optional): Column in `df` used to split series
                into legend groups. Defaults to None.
            width (float, optional): Bar width. Defaults to 0.8.
            space (float, optional): Space between clustered bars or stacked
                segments. Defaults to 0.0.
            limit (tuple({"top", "bottom"}, int), optional): Top N or Bottom N.
                Defaults to None.
            sort_axis (list[str | int] | tuple({"asc", "desc"}, {"label", "value"}), optional):
                Sort the axis categories. Defaults to None.
            sort_legend (list[str | int] | tuple({"asc", "desc"}, {"label", "value"}), optional):
                Sort the legend categories. Defaults to None.
            switch_axis (bool, optional): If True, draw a horizontal bar chart
                by swapping axes. Defaults to False.
            label (str | None, optional): Identifier for the chart.
                Defaults to None.

        Returns:
            BarChart: Wrapper exposing the Axes/Figure, prepared data, render
            properties, and bar styling facade.

        Notes:
            This method mutates the provided Axes by rendering bar artists.
        """
        data_properties = DataProperties(
            x_axis=x_axis,
            y_axis=y_axis,
            agg_func=agg_func,
            legend=legend,
            limit=limit,
            sort_axis=sort_axis,
            sort_legend=sort_legend,
        )

        bar_properties = BarProperties(
            bar_type=type,
            width=width,
            space=space,
            switch_axis=switch_axis,
            label=label,
        )

        factory = BarFactory(self.ax, self.fig).build(
            df=df,
            data_properties=data_properties,
            bar_properties=bar_properties,
        )

        return BarChart(bar_container=factory)

    def line(
        self,
        df: pd.DataFrame,
        x_axis: str,
        y_axis: str,
        legend: str | None = None,
        agg_func: str = "sum",
        area: bool = False,
        width: float = 1.0,
        running_total: bool = False,
        limit: LimitSpec | None = None,
        sort_axis: SortSpec | None = None,
        sort_legend: SortSpec | None = None,
        label: str | None = None,
    ) -> LineChart:
        """Create a line chart from a DataFrame and return a result wrapper.

        Args:
            df (pd.DataFrame): Source DataFrame.
            x_axis (str): Column in `df` used for the x-axis categories.
            y_axis (str): Column in `df` used for the y-axis values.
            legend (str | None, optional): Column in `df` used to split series
                into legend groups. Defaults to None.
            agg_func (str, optional): Aggregation function applied to `y_axis`.
                Defaults to "sum".
            area (bool, optional): If True, fill the area under each line.
                Defaults to False.
            width (float, optional): Line width. Defaults to 1.0.
            running_total (bool, optional): Transform each series into a cumulative
                sum. Defaults to False.
            limit (tuple({"top", "bottom"}, int), optional): Top N or Bottom N.
                Defaults to None.
            sort_axis (list[str | int] | tuple({"asc", "desc"}, {"label", "value"}), optional):
                Sort the axis categories. Defaults to None.
            sort_legend (list[str | int] | tuple({"asc", "desc"}, {"label", "value"}), optional):
                Sort the legend categories. Defaults to None.
            label (str | None, optional): Identifier for the chart.
                Defaults to None.

        Returns:
            LineChart: Wrapper exposing the Axes/Figure, prepared data, render
            properties, and line styling facade.

        Notes:
            This method mutates the provided Axes by rendering line artists.
        """
        data_properties = DataProperties(
            x_axis=x_axis,
            y_axis=y_axis,
            agg_func=agg_func,
            legend=legend,
            limit=limit,
            sort_axis=sort_axis,
            sort_legend=sort_legend,
        )

        line_properties = LineProperties(
            width=width,
            area=area,
            label=label,
        )

        factory = LineFactory(self.ax, self.fig).build(
            df=df,
            data_properties=data_properties,
            line_properties=line_properties,
            running_total=running_total,
        )

        return LineChart(line_container=factory)
