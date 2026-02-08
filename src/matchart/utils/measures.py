"""Compute derived measures from matchart chart results.

matchart charts (e.g., bar and line) expose a prepared `DataContainer` with
the original DataFrame and the pivot configuration used for rendering. Users
often want secondary analytics from that same prepared data (e.g., YoY change)
without rebuilding the pivot logic themselves. This module provides a small
"measures" layer that reads the chart's data container and computes reusable
metrics.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from matchart.chart.main import BarChart, LineChart

CHARTS = BarChart | LineChart


@dataclass(frozen=True)
class YoYContainer:
    """Return value for year-over-year computations.

    Attributes:
        pivot (pd.DataFrame): Pivot table that includes a "yoy" column with the
            computed year-over-year rates.
        dictionary (dict[str, float]): Mapping from pivot index labels to yoy
            values.
    """

    pivot: pd.DataFrame
    dictionary: dict[str, float]


class YoYHelpers:
    """Helper utilities for year-over-year calculations."""

    def __init__(self, df: pd.DataFrame, date_field: str) -> None:
        """
        Args:
            df (pd.DataFrame): Source DataFrame used for YoY computation.
            date_field (str): Name of the datetime-like column used to extract
                year and day-of-year.
        """
        self.df = df
        self.date_field = date_field

    def validate_years(self, years: list[int] | None) -> tuple[int, int]:
        """Validate and normalize the year pair used for YoY.

        If `years` is None, the two most recent years present in the data are
        used.

        Args:
            years (list[int] | None): Two-element list of years, or None to use
                the last two available years.

        Returns:
            tuple[int, int]: (previous_year, current_year) in ascending order.

        Raises:
            ValueError: If fewer than two years exist in the data, if `years`
                does not contain exactly two different entries, or if requested
                years are not present in the data.
        """
        available_years = sorted(self.df[self.date_field].dt.year.unique())
        if len(available_years) < 2:
            raise ValueError("Data must contain at least 2 different years for YoY.")

        if years is None:
            return int(available_years[-2]), int(available_years[-1])

        if len(years) != 2:
            raise ValueError("Exactly two years must be specified.")
        if years[0] == years[1]:
            raise ValueError("The two years must be different.")

        missing = [year for year in years if year not in available_years]
        if missing:
            raise ValueError(
                f"Years {missing} not found. Available years: {available_years}"
            )

        years = sorted(years)
        return int(years[0]), int(years[1])

    def match_periods(self, previous_year: int, current_year: int) -> pd.DataFrame:
        """Match year periods by aligning previous_year to current_year progress.

        This filters previous_year data to include only dates up to the same
        day-of-year as the latest date available in current_year data.

        Args:
            previous_year (int): Earlier year.
            current_year (int): Later year used to determine the cutoff.

        Returns:
            pd.DataFrame: Concatenated DataFrame containing the matched periods
            from both years.

        Raises:
            ValueError: If either year has no rows in the input data.
        """
        current_data: pd.DataFrame = self.df.loc[
            self.df[self.date_field].dt.year == current_year
        ]
        if current_data.empty:
            raise ValueError(f"No data found for year {current_year}")

        current_max_day: int = current_data[self.date_field].max().dayofyear

        previous_data: pd.DataFrame = self.df.loc[
            self.df[self.date_field].dt.year == previous_year
        ]
        if previous_data.empty:
            raise ValueError(f"No data found for year {previous_year}")

        previous_matched: pd.DataFrame = previous_data.loc[
            previous_data[self.date_field].dt.dayofyear <= current_max_day
        ]

        dataframes: list[pd.DataFrame] = [previous_matched, current_data]
        return pd.concat(dataframes, ignore_index=True)

    @staticmethod
    def compute_yoy(
        pivot: pd.DataFrame,
        previous_year: int,
        current_year: int,
    ) -> pd.DataFrame:
        """Compute YoY growth rates from a pivot table and add a "yoy" column.

        Args:
            pivot (pd.DataFrame): Pivot table containing columns for both years.
            previous_year (int): Baseline year column name in `pivot`.
            current_year (int): Comparison year column name in `pivot`.

        Returns:
            pd.DataFrame: The same pivot object with an added "yoy" column.

        Notes:
            - YoY is computed as (current - previous) / previous.
            - previous == 0 and current > 0 is mapped to +inf.
            - NaNs are replaced with 0.0, and values are rounded to 4 decimals.
        """
        previous: pd.Series = pivot[previous_year]
        current: pd.Series = pivot[current_year]

        yoy: pd.Series = (current - previous) / previous
        yoy = yoy.mask((previous == 0) & (current > 0), np.inf)
        yoy = yoy.fillna(0.0)
        yoy = yoy.astype(float).round(4)

        pivot["yoy"] = yoy
        return pivot


class Measures:
    """Compute derived measures from a matchart chart instance."""

    def __init__(self, chart: CHARTS) -> None:
        """
        Args:
            chart (CHARTS): A built matchart chart wrapper (BarChart or
                LineChart) exposing a `data` container.
        """
        self.chart = chart

    def yoy(self, date_field: str, years: list[int] | None = None) -> YoYContainer:
        """Compute year-over-year values from the chart's prepared data.

        This method rebuilds a pivot table using the chart's `DataContainer`
        settings (index/values/columns/agg_func), aligns the year periods for
        fair comparison, computes YoY rates, and returns both the pivot table
        and a label->value mapping.

        Args:
            date_field (str): Name of the datetime-like column used to extract
                years and day-of-year.
            years (list[int] | None, optional): Two-element list specifying the
                previous and current years. If None, the two most recent years
                in the data are used.

        Returns:
            YoYContainer: Container holding:
            - pivot (pd.DataFrame): Pivot with a "yoy" column.
            - dictionary (dict[str, float]): Mapping of pivot index labels to
              YoY values.

        Raises:
            ValueError: If years are invalid or either year has no matching
                rows after filtering.
        """
        df = self.chart.data.df
        index = self.chart.data.index
        values = self.chart.data.values
        columns = self.chart.data.columns
        agg_func = self.chart.data.agg_func

        help = YoYHelpers(df=df, date_field=date_field)

        previous_year, current_year = help.validate_years(years)
        matched_periods = help.match_periods(previous_year, current_year)

        pivot = matched_periods.pivot_table(
            index=index,
            values=values,
            columns=columns,
            aggfunc=agg_func,  # type: ignore
        ).round(2)

        pivot = help.compute_yoy(pivot, previous_year, current_year)

        yoy_dict: dict[str, float] = {}
        for key, value in pivot["yoy"].items():
            yoy_dict[str(key)] = float(value)

        return YoYContainer(pivot=pivot, dictionary=yoy_dict)
