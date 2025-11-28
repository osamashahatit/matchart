import pandas as pd
from typing import Literal
from dataclasses import dataclass
from abc import ABC, abstractmethod


type SortMethod = Literal["asc", "desc"]
type SortBy = Literal["label", "value"]
type SortOn = Literal["index", "columns"]
type SortTuple = tuple[SortMethod, SortBy]
type SortList = list[str | int]
type SortType = SortList | SortTuple


@dataclass(frozen=True)
class SortConfiguration:
    """Configuration for sorting operations."""

    order: SortList | None = None
    method: SortMethod | None = None
    sort_by: SortBy | None = None
    ascending: bool | None = None

    @classmethod
    def from_list(cls, sort: SortList) -> "SortConfiguration":
        """Create SortConfiguration from a list."""

        return cls(order=sort)

    @classmethod
    def from_tuple(cls, sort: SortTuple) -> "SortConfiguration":
        """Create SortConfiguration from a tuple."""

        method, sort_by = sort
        ascending = method == "asc"
        return cls(method=method, sort_by=sort_by, ascending=ascending)


class SortStrategyABC(ABC):
    """Abstract base class for sorting strategies."""

    def __init__(self, pivot: pd.DataFrame, sort_on: SortOn) -> None:
        self.pivot = pivot
        self.sort_on = sort_on

    @abstractmethod
    def sort(self) -> pd.DataFrame:
        """Sort the pivot DataFrame."""
        ...


class ExplicitOrderSortStrategy(SortStrategyABC):
    """Sort by explicit order of labels."""

    def __init__(self, pivot: pd.DataFrame, sort_on: SortOn, order: SortList) -> None:
        self.pivot = pivot
        self.sort_on = sort_on
        self.order = order

    def sort(self) -> pd.DataFrame:

        if self.sort_on == "index":
            return self.pivot.reindex(index=self.order)
        elif self.sort_on == "columns":
            return self.pivot.reindex(columns=self.order)
        else:
            raise ValueError("sort_on must be either 'index' or 'columns'.")


class LabelSortStrategy(SortStrategyABC):
    """Sort by index or columns labels."""

    def __init__(self, pivot: pd.DataFrame, sort_on: SortOn, ascending: bool) -> None:
        self.pivot = pivot
        self.sort_on = sort_on
        self.ascending = ascending

    def sort(self) -> pd.DataFrame:

        return self.pivot.sort_index(
            axis=0 if self.sort_on == "index" else 1, ascending=self.ascending
        )


class ValueSortStrategy(SortStrategyABC):
    """Sort by the sum of values across the opposite axis."""

    def __init__(self, pivot: pd.DataFrame, sort_on: SortOn, ascending: bool) -> None:
        self.pivot = pivot
        self.sort_on = sort_on
        self.ascending = ascending

    def sort(self) -> pd.DataFrame:

        axis = 1 if self.sort_on == "index" else 0
        totals = self.pivot.sum(axis=axis, numeric_only=True)
        sorted_index = totals.sort_values(ascending=self.ascending).index

        if self.sort_on == "index":
            return self.pivot.reindex(index=sorted_index)
        elif self.sort_on == "columns":
            return self.pivot.reindex(columns=sorted_index)
        else:
            raise ValueError("sort_on must be either 'index' or 'columns'.")


class SortStrategySelector:
    """Select sorting strategy based on configuration."""

    @staticmethod
    def get_config(sort: SortType) -> SortConfiguration:
        """Get SortConfiguration from the sort specification."""

        if isinstance(sort, list):
            return SortConfiguration.from_list(sort)
        return SortConfiguration.from_tuple(sort)

    @staticmethod
    def get_strategy(
        sort_on: SortOn,
        pivot: pd.DataFrame,
        config: SortConfiguration,
    ) -> SortStrategyABC:
        """Get SortStrategy based on SortConfiguration."""

        if config.order is not None:
            return ExplicitOrderSortStrategy(
                order=config.order,
                pivot=pivot,
                sort_on=sort_on,
            )
        if config.ascending is not None and config.sort_by is not None:
            if config.sort_by == "label":
                return LabelSortStrategy(
                    ascending=config.ascending,
                    pivot=pivot,
                    sort_on=sort_on,
                )
            if config.sort_by == "value":
                return ValueSortStrategy(
                    ascending=config.ascending,
                    pivot=pivot,
                    sort_on=sort_on,
                )
        raise ValueError("Invalid sort configuration.")


class PivotSorter:
    """Sort pivot DataFrame by index or columns using various sorting strategies."""

    def __init__(self, pivot: pd.DataFrame) -> None:
        self.pivot = pivot

    def sort_index(self, sort: SortType | None) -> pd.DataFrame:
        """Sort DataFrame index."""

        if sort is None:
            return self.pivot

        sort_selector = SortStrategySelector()
        config = sort_selector.get_config(sort=sort)
        strategy = sort_selector.get_strategy(
            sort_on="index",
            pivot=self.pivot,
            config=config,
        )
        return strategy.sort()

    def sort_columns(self, sort: SortType | None) -> pd.DataFrame:
        """Sort DataFrame columns."""

        if sort is None:
            return self.pivot

        sort_selector = SortStrategySelector()
        config = sort_selector.get_config(sort=sort)
        strategy = sort_selector.get_strategy(
            sort_on="columns",
            pivot=self.pivot,
            config=config,
        )
        return strategy.sort()
