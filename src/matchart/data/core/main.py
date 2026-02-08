"""Build normalized chart pivot.

This module provides a factory for transforming raw DataFrames into chart-ready
pivot tables. Most charts require a consistent structure: an index for x-axis
categories, values for the y-axis, and optionally a legend dimension represented
by columns. The factory centralizes common data preparation steps including
pivoting, aggregation, limiting, and sorting.
"""

from dataclasses import dataclass

import pandas as pd

from ._limit import LimitSpec, PivotLimiter
from ._sort import PivotSorter, SortSpec


@dataclass(frozen=True)
class DataProperties:
    """
    This class defines all parameters needed to transform a raw DataFrame into
    a pivoted, aggregated, and optionally filtered/sorted dataset suitable for
    charting.
    """

    x_axis: str
    y_axis: str
    agg_func: str
    legend: str | None
    limit: LimitSpec | None
    sort_axis: SortSpec | None
    sort_legend: SortSpec | None


@dataclass(frozen=True)
class DataContainer:
    """Container for prepared pivot data and associated metadata."""

    pivot: pd.DataFrame
    df: pd.DataFrame
    index: str
    values: str
    columns: str | None
    agg_func: str


class DataFactory:
    """Factory for creating chart-ready pivot datasets."""

    def __init__(self, df: pd.DataFrame):
        """
        Args:
            df (pd.DataFrame): The source DataFrame containing raw data
                to be pivoted and transformed.
        """
        self.df = df

    def build(self, properties: DataProperties) -> DataContainer:
        """Build the DataContainer based on the defined DataProperties.

        Args:
            properties (DataProperties): Complete specification defining
                how to pivot, aggregate, limit, and sort the source DataFrame.

        Returns:
            A DataContainer holding the prepared pivot table, aligned raw data
            subset, and metadata about the transformation (column names and
            aggregation function used).

        Raises:
            ValueError: If any column specified in properties (x_axis, y_axis,
                legend) does not exist in the source DataFrame.
            ValueError: If the specified agg_func is not a valid pandas
                aggregation function.
        """
        # Validate columns exist
        required_cols = [properties.x_axis, properties.y_axis]
        if properties.legend:
            required_cols.append(properties.legend)
        missing = [col for col in required_cols if col not in self.df.columns]
        if missing:
            raise ValueError(f"Columns not found in DataFrame: {missing}")

        # Validate agg_func
        valid_agg_funcs = [
            "sum",
            "mean",
            "count",
            "min",
            "max",
            "std",
            "median",
            "nunique",
        ]
        if properties.agg_func not in valid_agg_funcs:
            raise ValueError(f"Invalid aggregation function: {properties.agg_func}")

        pivot = self.df.pivot_table(
            index=properties.x_axis,
            values=properties.y_axis,
            columns=properties.legend,
            aggfunc=properties.agg_func,  # type:ignore
            fill_value=0,
        )

        if properties.limit:
            pivot = PivotLimiter(pivot=pivot).limit(limit=properties.limit)
        if properties.sort_axis:
            pivot = PivotSorter(pivot=pivot).sort_index(sort=properties.sort_axis)
        if properties.sort_legend:
            pivot = PivotSorter(pivot=pivot).sort_columns(sort=properties.sort_legend)

        mask = self.df[properties.x_axis].isin(pivot.index)
        df = self.df[mask].reset_index(drop=True)

        return DataContainer(
            pivot=pivot,
            df=df,
            index=properties.x_axis,
            values=properties.y_axis,
            columns=properties.legend,
            agg_func=properties.agg_func,
        )
