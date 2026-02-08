"""Expose high-level chart specific data builders.

This module provides a simple orchestration layer that presents per-chart
entry points, keeping chart implementations free of repeated boilerplate
and centralizing chart-specific data tweaks.
"""

import pandas as pd

from .core.main import DataContainer, DataFactory, DataProperties


class Data:
    """Orchestrate data preparation for different chart types."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Args:
            df (pd.DataFrame): Source DataFrame.
        """
        self.df = df

    def bar(self, properties: DataProperties) -> DataContainer:
        """Prepare data for bar charts.

        Args:
            properties (DataProperties): Pivot and transformation settings.

        Returns:
            DataContainer: Prepared chart pivot and metadata.
        """
        return DataFactory(self.df).build(properties=properties)

    def line(self, properties: DataProperties, running_total: bool) -> DataContainer:
        """Prepare data for line charts.

        If running_total is True, this converts the pivot values to a
        cumulative sum over the index (top-to-bottom), which is commonly
        used for cumulative line charts.

        Args:
            properties (DataProperties): Pivot and transformation settings.
            running_total (bool): Whether to convert the pivot to a running
                total using DataFrame.cumsum().

        Returns:
            DataContainer: Prepared chart pivot and metadata.
        """
        data = DataFactory(self.df).build(properties=properties)

        if running_total:
            # Keep metadata and aligned raw df, but replace the pivot with
            # its cumulative sum for cumulative line charts.
            data = DataContainer(
                pivot=data.pivot.cumsum(),
                df=data.df,
                index=data.index,
                values=data.values,
                columns=data.columns,
                agg_func=data.agg_func,
            )
        return data
