import pandas as pd
import numpy as np
from dataclasses import dataclass

from matchart.chart.main import BarChart, LineChart

CHARTS = BarChart | LineChart


@dataclass(frozen=True)
class YoYContainer:

    pivot: pd.DataFrame
    dictionary: dict[str, float]


class YoYHelpers:

    def __init__(self, df: pd.DataFrame, date_field: str) -> None:
        self.df = df
        self.date_field = date_field

    def validate_years(self, years: list[int] | None) -> tuple[int, int]:
        """Validate and prepare year pair for YoY computation.

        Returns (earlier_year, later_year) sorted in ascending order.
        If years=None, returns the two most recent years in data.
        """

        available_years = sorted(self.df[self.date_field].dt.year.unique())
        if len(available_years) < 2:
            raise ValueError("Data must contain at least 2 different years for YoY.")
        if years is None:
            return available_years[-2], available_years[-1]
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
        """Match data periods by filtering both years to the same day-of-year.

        Filters previous_year data to include only dates up to the same day-of-year
        as the latest date available in current_year data.

        Returns concatenated DataFrame of matched periods from both years.
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
        """Compute YoY growth rates from pivot table."""

        previous: pd.Series = pivot[previous_year]
        current: pd.Series = pivot[current_year]
        yoy: pd.Series = (current - previous) / previous
        yoy = yoy.mask((previous == 0) & (current > 0), np.inf)
        yoy = yoy.fillna(0.0)
        yoy = yoy.astype(float).round(4)
        pivot["yoy"] = yoy
        return pivot


class Measures:
    """Utility class for computing various measures from chart instance."""

    def __init__(self, chart: CHARTS) -> None:
        self.chart = chart

    def yoy(self, date_field: str, years: list[int] | None = None) -> YoYContainer:
        """
        Compute year-over-year (YoY) growth rates from a chart's pivoted data.

        This method compares metrics between two calendar years, calculates the
        percentage change for matching periods, and returns both the resulting
        pivot table and a corresponding dictionary of YoY values.

        If `years` is not provided, the two most recent years present in the
        dataset are used. The method ensures both years are aligned to the same
        day-of-year to maintain comparability.

        Parameters
        ----------
        date_field : str
            The name of the datetime column used to extract years.
        years : list[int] | None. Default is None.
            Two-element list specifying the previous and current years
            (e.g., [2023, 2024]). If None, the last two years in the data
            are used automatically.

        Returns
        -------
        YoYContainer
            Dataclass containing the following fields:

            - **pivot** (`pd.DataFrame`): Pivoted data with an additional `"yoy"` column.
            - **dictionary** (`dict[str, float]`): Mapping of pivot index labels to
              YoY values.

        Examples
        --------
        >>> measures = Measures(chart)
        >>> result = measures.yoy(date_field="order_date", years=[2023, 2024])
        >>> result.pivot
        >>> result.dictionary
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
            aggfunc=agg_func,
        ).round(2)

        pivot = help.compute_yoy(pivot, previous_year, current_year)
        return YoYContainer(pivot=pivot, dictionary=pivot["yoy"].to_dict())
