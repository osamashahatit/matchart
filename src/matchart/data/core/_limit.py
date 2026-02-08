"""Limit pivoted data to the top N or bottom N.

Many chart types are driven by pivoted pandas DataFrames. In real
datasets, pivots can include many categories, making charts crowded and
less readable. This module provides a tiny helper to limit a pivot to
the "top N" or "bottom N" rows based on each row's total.
"""

from typing import Literal

import pandas as pd

type LimitSpec = tuple[Literal["top", "bottom"], int]


class PivotLimiter:
    """Limit pivot DataFrame rows based on row-wise totals."""

    def __init__(self, pivot: pd.DataFrame) -> None:
        """
        Args:
            pivot (pd.DataFrame): Pivoted data where each row represents a
                category and columns represent values to be summed.
        """
        self.pivot = pivot

    def limit(self, limit: LimitSpec) -> pd.DataFrame:
        """Limit the pivot to the top N or bottom N rows by row sum.

        Args:
            limit (LimitSpec): A tuple of (limit_by, limit_n) where
                limit_by is "top" or "bottom" and limit_n is the number of
                rows to keep.

        Returns:
            pd.DataFrame: A DataFrame containing only the selected rows,
            preserving the original columns.

        Raises:
            ValueError: If limit_n is not greater that 1.
            ValueError: If limit_by is not "top" or "bottom".
        """
        limit_by, limit_n = limit
        row_sums = self.pivot.sum(axis=1)

        if limit_n < 1:
            raise ValueError("limit_n must be greater than 0")

        if limit_by == "top":
            return self.pivot.loc[row_sums.nlargest(limit_n).index]

        if limit_by == "bottom":
            return self.pivot.loc[row_sums.nsmallest(limit_n).index]

        raise ValueError("limit_by must be either 'top' or 'bottom'")
