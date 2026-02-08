"""Flexible sorters for pivoted chart data.

Charts built on pivoted pandas DataFrames often need consistent and
configurable ordering of rows or columns. Depending on the chart, users
may want to sort explicitly by a given label order, alphabetically by
labels, or by aggregated values. This module encapsulates those concerns
behind small, composable objects so higher-level chart code can
request sorting declaratively without embedding pandas-specific logic.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

import pandas as pd

type SortDirection = Literal["asc", "desc"]
type SortBy = Literal["label", "value"]
type SortOn = Literal["index", "columns"]
type SortTuple = tuple[SortDirection, SortBy]
type SortList = list[str | int]
type SortSpec = SortList | SortTuple


@dataclass(frozen=True)
class SortConfiguration:
    """
    This class converts user-facing sort specifications into a structured
    form that sorters can consume reliably.
    """

    sort_list: SortList | None = None
    direction: SortDirection | None = None
    sort_by: SortBy | None = None
    ascending: bool | None = None

    @classmethod
    def from_list(cls, sort_list: SortList) -> "SortConfiguration":
        """Create a sort configuration from an explicit order list.

        Args:
            sort_list (SortList): Explicit ordering of labels.

        Returns:
            SortConfiguration: Configuration with explicit order set.
        """
        return cls(sort_list=sort_list)

    @classmethod
    def from_tuple(cls, sort: SortTuple) -> "SortConfiguration":
        """Create a sort configuration from a (direction, sort_by) tuple.

        Args:
            sort (SortTuple): Tuple describing sort direction and basis.

        Returns:
            SortConfiguration: Parsed configuration with ascending flag set.

        Raises:
            ValueError: If tuple length is invalid or contains invalid values.
        """
        if len(sort) != 2:
            raise ValueError(f"Sort tuple must have exactly 2 elements, got: {sort}")

        direction, sort_by = sort

        if direction not in ("asc", "desc"):
            raise ValueError(
                f"Invalid direction: {direction}. Must be 'asc' or 'desc'."
            )

        if sort_by not in ("label", "value"):
            raise ValueError(f"Invalid sort_by: {sort_by}. Must be 'label' or 'value'.")

        ascending = direction == "asc"
        return cls(direction=direction, sort_by=sort_by, ascending=ascending)


class SorterBase(ABC):
    """Define the interface for pivot sorters."""

    def __init__(self, pivot: pd.DataFrame, sort_on: SortOn) -> None:
        """
        Args:
            pivot (pd.DataFrame): Pivoted DataFrame to sort.
            sort_on (SortOn): Whether to sort on index or columns.
        """
        self.pivot = pivot
        self.sort_on = sort_on

    @abstractmethod
    def sort(self) -> pd.DataFrame:
        """Sort the pivot DataFrame and return the result."""
        ...


class ExplicitSorter(SorterBase):
    """Sort pivot data using an explicit label order."""

    def __init__(
        self,
        pivot: pd.DataFrame,
        sort_on: SortOn,
        sort_list: SortList,
    ) -> None:
        """
        Args:
            pivot (pd.DataFrame): Pivoted DataFrame to sort.
            sort_on (SortOn): Whether to sort index or columns.
            sort_list (SortList): Explicit label order.
        """
        self.pivot = pivot
        self.sort_on = sort_on
        self.sort_list = sort_list

    def sort(self) -> pd.DataFrame:
        """Apply explicit ordering to index or columns.

        Returns:
            pd.DataFrame: Reindexed DataFrame following the given order.

        Raises:
            ValueError: If labels are not found in index or columns.
            ValueError: If sort_on is not "index" or "columns".
        """
        if self.sort_on == "index":
            missing = set(self.sort_list) - set(self.pivot.index)
            if missing:
                raise ValueError(f"Labels not found in index: {missing}")
            return self.pivot.reindex(index=self.sort_list)

        if self.sort_on == "columns":
            missing = set(self.sort_list) - set(self.pivot.columns)
            if missing:
                raise ValueError(f"Labels not found in columns: {missing}")
            return self.pivot.reindex(columns=self.sort_list)

        raise ValueError("sort_on must be either 'index' or 'columns'.")


class LabelSorter(SorterBase):
    """Sort pivot data by index or column labels."""

    def __init__(self, pivot: pd.DataFrame, sort_on: SortOn, ascending: bool) -> None:
        """
        Args:
            pivot (pd.DataFrame): Pivoted DataFrame to sort.
            sort_on (SortOn): Whether to sort index or columns.
            ascending (bool): Sort direction.
        """
        self.pivot = pivot
        self.sort_on = sort_on
        self.ascending = ascending

    def sort(self) -> pd.DataFrame:
        """Sort by labels on the specified axis.

        Returns:
            pd.DataFrame: Sorted DataFrame.
        """
        return self.pivot.sort_index(
            axis=0 if self.sort_on == "index" else 1,
            ascending=self.ascending,
        )


class ValueSorter(SorterBase):
    """Sort pivot data by aggregated values across the opposite axis."""

    def __init__(self, pivot: pd.DataFrame, sort_on: SortOn, ascending: bool) -> None:
        """
        Args:
            pivot (pd.DataFrame): Pivoted DataFrame to sort.
            sort_on (SortOn): Whether to sort index or columns.
            ascending (bool): Sort direction.
        """
        self.pivot = pivot
        self.sort_on = sort_on
        self.ascending = ascending

    def sort(self) -> pd.DataFrame:
        """Sort by row or column totals.

        Returns:
            pd.DataFrame: Sorted DataFrame.

        Raises:
            ValueError: If sort_on is not "index" or "columns".
        """
        # Sum across the opposite axis to compute totals
        axis = 1 if self.sort_on == "index" else 0
        totals = self.pivot.sum(axis=axis, numeric_only=True)
        sorted_index = totals.sort_values(ascending=self.ascending).index

        if self.sort_on == "index":
            return self.pivot.reindex(index=sorted_index)

        if self.sort_on == "columns":
            return self.pivot.reindex(columns=sorted_index)

        raise ValueError("sort_on must be either 'index' or 'columns'.")


class SorterSelector:
    """Select sorter based on sort specifications."""

    def __init__(self, pivot: pd.DataFrame, sort: SortSpec) -> None:
        """
        Args:
            pivot (pd.DataFrame): Pivoted DataFrame to sort.
            sort (SortSpec): Either an explicit order list or a tuple
                describing direction and basis.
        """
        self.pivot = pivot
        self.sort = sort

    def select(self, sort_on: SortOn) -> SorterBase:
        """Get the appropriate sorter.

        Args:
            sort_on (SortOn): Whether to sort index or columns.

        Returns:
            SorterBase.

        Raises:
            ValueError: If the configuration cannot be resolved.
        """
        # parse user-facing spec into normalized config
        config = (
            SortConfiguration.from_list(self.sort)
            if isinstance(self.sort, list)
            else SortConfiguration.from_tuple(self.sort)
        )

        if config.sort_list is not None:
            return ExplicitSorter(
                sort_list=config.sort_list,
                pivot=self.pivot,
                sort_on=sort_on,
            )

        if config.ascending is not None and config.sort_by is not None:
            if config.sort_by == "label":
                return LabelSorter(
                    ascending=config.ascending,
                    pivot=self.pivot,
                    sort_on=sort_on,
                )

            if config.sort_by == "value":
                return ValueSorter(
                    ascending=config.ascending,
                    pivot=self.pivot,
                    sort_on=sort_on,
                )

        raise ValueError("Invalid sort configuration.")


class PivotSorter:
    """Sort pivot DataFrames by index or columns."""

    def __init__(self, pivot: pd.DataFrame) -> None:
        """
        Args:
            pivot (pd.DataFrame): Pivoted DataFrame to sort.
        """
        self.pivot = pivot

    def sort_index(self, sort: SortSpec | None) -> pd.DataFrame:
        """Sort the DataFrame index.

        Args:
            sort (SortSpec | None): Sort specification or None to skip
                sorting.

        Returns:
            pd.DataFrame: Sorted or original DataFrame.
        """
        if sort is not None:
            sorter = SorterSelector(
                pivot=self.pivot,
                sort=sort,
            ).select(sort_on="index")
            return sorter.sort()
        return self.pivot

    def sort_columns(self, sort: SortSpec | None) -> pd.DataFrame:
        """Sort the DataFrame columns.

        Args:
            sort (SortSpec | None): Sort specification or None to skip
                sorting.

        Returns:
            pd.DataFrame: Sorted or original DataFrame.
        """
        if sort is not None:
            sorter = SorterSelector(
                pivot=self.pivot,
                sort=sort,
            ).select(sort_on="columns")
            return sorter.sort()
        return self.pivot
