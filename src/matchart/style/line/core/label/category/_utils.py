"""Utilities for line charts category data labels."""

from dataclasses import dataclass

import numpy as np
from matplotlib.axes import Axes


@dataclass(frozen=True)
class CDL_Line_Totals:
    """Represent an aggregated numeric total for a line-chart category.

    Attributes:
        total (float): Sum of all line values corresponding to a single
            x-tick/category.
    """

    total: float

    @classmethod
    def compute_total(
        cls,
        ax: Axes,
        tick_label: str,
    ) -> "CDL_Line_Totals":
        """Compute the total value for a given tick label across all lines.

        Args:
            ax (Axes): Matplotlib Axes containing one or more Line2D objects.
            tick_label (str): Text of the x-axis tick label identifying the
                category to aggregate.

        Returns:
            CDL_Line_Totals: An instance containing the summed total value.

        Notes:
            - Tick labels are read from ax.get_xticklabels().
            - The index of the matching tick label is used to select values
              from each line's y-data.
            - If a line does not have a value at that index, it is skipped.
            - If the tick label does not exist, the returned total is 0.0.
        """
        # Collect tick label texts in display order.
        tick_labels: list[str] = []
        for label in ax.get_xticklabels():
            tick_labels.append(label.get_text())

        total = 0.0

        # Sum y-values from all lines that correspond to the target tick.
        for line in ax.lines:
            ydata = np.asarray(line.get_ydata(), dtype=float)

            for index, label in enumerate(tick_labels):
                if label == tick_label and index < len(ydata):
                    total += float(ydata[index])

        return cls(total=total)
