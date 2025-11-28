import pandas as pd
from typing import Literal

type LimitBy = Literal["top", "bottom"]
type LimitN = int
type LimitType = tuple[LimitBy, LimitN]


class PivotLimiter:
    """Handles limiting pivot DataFrame rows based on row sums."""

    def __init__(self, pivot: pd.DataFrame) -> None:
        self.pivot = pivot

    def limit(self, limit: LimitType) -> pd.DataFrame:
        """Limit DataFrame to top or bottom rows based on row sums."""

        limit_by, limit_n = limit
        row_sums = self.pivot.sum(axis=1)

        if limit_by == "top":
            return self.pivot.loc[row_sums.nlargest(limit_n).index]
        elif limit_by == "bottom":
            return self.pivot.loc[row_sums.nsmallest(limit_n).index]
        else:
            raise ValueError("limit_by must be either 'top' or 'bottom'")
