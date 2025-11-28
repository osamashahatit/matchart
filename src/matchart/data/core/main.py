import pandas as pd
from dataclasses import dataclass

from ._limit import PivotLimiter, LimitType
from ._sort import PivotSorter, SortType


@dataclass(frozen=True)
class DataProperties:

    x_axis: str
    y_axis: str
    agg_func: str
    legend: str | None
    limit: LimitType | None
    sort_axis: SortType | None
    sort_legend: SortType | None


@dataclass(frozen=True)
class DataContainer:

    pivot: pd.DataFrame
    df: pd.DataFrame
    index: str
    values: str
    columns: str | None
    agg_func: str


class DataFactory:
    """Handles pivoting and transforming DataFrame for plotting."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def build(self, properties: DataProperties) -> DataContainer:
        """Create a pivot table from a DataFrame."""

        pivot = self.df.pivot_table(
            index=properties.x_axis,
            values=properties.y_axis,
            columns=properties.legend,
            aggfunc=properties.agg_func,
            fill_value=0,
        ).round(2)

        if properties.limit:
            pivot = PivotLimiter(pivot=pivot).limit(limit=properties.limit)
        if properties.sort_axis:
            pivot = PivotSorter(pivot=pivot).sort_index(sort=properties.sort_axis)
        if properties.sort_legend:
            pivot = PivotSorter(pivot=pivot).sort_columns(sort=properties.sort_legend)

        df_filter = self.df[properties.x_axis].isin(pivot.index)
        df = self.df[df_filter].reset_index(drop=True)

        return DataContainer(
            pivot=pivot,
            df=df,
            index=properties.x_axis,
            values=properties.y_axis,
            columns=properties.legend,
            agg_func=properties.agg_func,
        )
