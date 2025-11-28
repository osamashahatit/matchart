import pandas as pd
from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matchart.data.core._limit import LimitType
from matchart.data.core._sort import SortType
from matchart.data.core.main import DataProperties, DataContainer

from .core.bar.core.main import BarType, BarProperties
from .core.bar.main import BarContainer, BarFactory
from .core.line.core.main import LineProperties
from .core.line.main import LineContainer, LineFactory

from matchart.style.bar.main import BarStyler
from matchart.style.line.main import LineStyler


@dataclass
class BarChart:
    bar_container: BarContainer

    @property
    def ax(self) -> Axes:
        return self.bar_container.ax

    @property
    def fig(self) -> Figure:
        return self.bar_container.fig

    @property
    def data(self) -> DataContainer:
        return self.bar_container.data_container

    @property
    def props(self) -> BarProperties:
        return self.bar_container.bar_properties

    @property
    def style(self) -> BarStyler:
        return self.bar_container.bar_styler


@dataclass
class LineChart:
    line_container: LineContainer

    @property
    def ax(self) -> Axes:
        return self.line_container.ax

    @property
    def fig(self) -> Figure:
        return self.line_container.fig

    @property
    def data(self) -> DataContainer:
        return self.line_container.data_container

    @property
    def props(self) -> LineProperties:
        return self.line_container.line_properties

    @property
    def style(self) -> LineStyler:
        return self.line_container.line_styler


class Chart:
    """
    Main entry point for creating and styling charts.

    This class provides a simplified interface that delegates to
    specialized builder classes for orchestration.
    """

    def __init__(self, ax: Axes, fig: Figure) -> None:
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
        limit: LimitType | None = None,
        sort_axis: SortType | None = None,
        sort_legend: SortType | None = None,
        switch_axis: bool = False,
        label: str | None = None,
    ) -> BarChart:
        """Create a bar chart and return its container.

        Parameters
        ----------
        df : pandas.DataFrame
            Source DataFrame.
        x_axis : str
            Column from source DataFrame to use for the chart x axis.
        y_axis : str
            Column from source DataFrame to use for the chart y axis.
        agg_func : str. Default is "sum"
            Aggregation function applied to `y_axis`.
        type : {"clustered", "stacked", "standard"}. Default is "stacked"
            Bar layout variants.
        legend : str | None. Default is None.
            Column from source DataFrame to use for splitting series.
        width : float. Default is 0.8
            Width of the bars.
        space : float. Default is 0.0
            Space between bars within a cluster or between stacked segments.
        limit : tuple({"top", "bottom"}, int) | None. Default is None.
            Limiting configuration for top-N.
            The first element specifies the direction ("top" or "bottom"),
            and the second element specifies the number of items to include.
        sort_axis : list[str | int] | tuple({"asc", "desc"}, {"label", "value"}) | None. Default is None.
            Sort the axis categories.
        sort_legend : list[str | int] | tuple({"asc", "desc"}, {"label", "value"}) | None. Default is None.
            Sort the legend categories.
        switch_axis : bool. Default = False
            If True, draws a horizontal bar chart by swapping axes.
        label : str | None. Default is None.
            Identifier for the chart.

        Returns
        -------
        BarChart
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
            type=type,
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
        limit: LimitType | None = None,
        sort_axis: SortType | None = None,
        sort_legend: SortType | None = None,
        label: str | None = None,
    ) -> LineChart:
        """Create a line chart and return its container.

        Parameters
        ----------
        df : pandas.DataFrame
            Source DataFrame.
        x_axis : str
            Column from source DataFrame to use for the chart x axis.
        y_axis : str
            Column from source DataFrame to use for the chart y axis.
        legend : str | None. Default is None.
            Column used to split series.
        agg_func : str. Default = "sum"
            Aggregation function applied to `y_axis`.
        area : bool. Default = False
            If True, fills the area under each line.
        width : float. Default = 1.0
            Width of the lines.
        running_total : bool. Default = False
            If True, transforms each series into a cumulative sum.
        limit : tuple({"top", "bottom"}, int) | None. Default is None.
            Limiting configuration for top-N.
            The first element specifies the direction ("top" or "bottom"),
            and the second element specifies the number of items to include.
        sort_axis : list[str | int] | tuple({"asc", "desc"}, {"label", "value"}) | None. Default is None.
            Sort the axis categories.
        sort_legend : list[str | int] | tuple({"asc", "desc"}, {"label", "value"}) | None. Default is None.
            Sort the legend categories.
        label : str | None. Default is None.
            Identifier for the chart.

        Returns
        -------
        LineChart
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
